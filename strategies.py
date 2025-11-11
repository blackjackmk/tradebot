import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg')
from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, name: str, data_path='./data.csv'):
        self.name = name
        self.base_df = pd.read_csv(data_path)
        self.results_df = pd.DataFrame()
        self.param_names = []

    @abstractmethod
    def apply_strategy(self, df, params) -> pd.DataFrame:
        """
        Apply strategy logic to df and return df with a 'Signal' column set.
        `params` is a tuple of values ordered according to `param_names`.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_parameters(self):
        """Generate parameter combinations to test"""
        raise NotImplementedError

    def compare_params(self):
        results = []  # Store results
        param_combinations = self.generate_parameters()
        for params in param_combinations:
            df2 = self.base_df.copy()
            st_df = self.apply_strategy(df2, params)
            gain = self.backtest_strategy(st_df)
            results.append(params + (gain,))

        col_names = list(self.param_names) + ['Gain']
        self.results_df = pd.DataFrame(results, columns=col_names)  # Build results DataFrame
        self.find_the_best()

    def backtest_strategy(self, data):
        initial_cash = 10000.0  # Starting with $10,000
        commission = 0.0005    # proportional commission per trade (0.05%)
        slippage = 0.0005      # proportional slippage per trade (0.05%)
        fraction = 1.0         # fraction of cash to use when buying

        df = data.copy().reset_index(drop=True)
        df['Position'] = 0.0   # Bitcoin units held
        df['Cash'] = 0.0
        df['Holdings'] = 0.0
        df['Equity'] = 0.0
        df['Trade'] = None     # 'buy'/'sell'/None

        cash = float(initial_cash)
        position = 0.0
        last_signal = None

        for i, row in df.iterrows():
            price = float(row['Close'])
            sig = row.get('Signal', None)

            if sig == 'Buy' and last_signal != 'Buy':
                buy_price = price * (1.0 + slippage)
                spend = cash * fraction
                units = spend / buy_price
                trade_cost = spend * commission
                # update
                position += units
                cash -= spend + trade_cost
                df.at[i, 'Trade'] = 'buy'
                last_signal = 'Buy'

            elif sig == 'Sell' and last_signal == 'Buy' and position > 0:
                # sell all position, get price - slippage
                sell_price = price * (1.0 - slippage)
                proceeds = position * sell_price
                trade_cost = proceeds * commission
                cash += proceeds - trade_cost
                df.at[i, 'Trade'] = 'sell'
                position = 0.0
                last_signal = 'Sell'

            holdings = position * price
            equity = cash + holdings
            df.at[i, 'Position'] = position
            df.at[i, 'Cash'] = cash
            df.at[i, 'Holdings'] = holdings
            df.at[i, 'Equity'] = equity

        equity_series = df['Equity'].astype(float)
        return float(equity_series.iloc[-1]) - initial_cash

    def find_the_best(self, confidence_level=0.95):
        gains = self.results_df['Gain'].values
        best_gain = gains.max()

        # Remove outliers using IQR
        Q1 = np.percentile(gains, 25)
        Q3 = np.percentile(gains, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        non_outlier_gains = gains[(gains >= lower_bound) & (gains <= upper_bound)]

        if len(non_outlier_gains) < 2:
            print("Not enough non-outlier data points for statistical testing")
            return False

        t_stat, p_value = stats.ttest_1samp(non_outlier_gains, best_gain)

        if p_value < (1 - confidence_level):
            best_params = self.results_df.loc[self.results_df['Gain'].idxmax()]
            print("Statistically significant best parameters found:")
            print(best_params)
            return True
        else:
            print("Best result may not be statistically significant")
            return False

    def plot_results(self, x_col, y_col, z_col, x_label, y_label, z_label):
        """Plot 3D results"""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.results_df[x_col], self.results_df[y_col], self.results_df[z_col])
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        plt.title(f"{self.name} Strategy - {x_label} vs {y_label} vs {z_label}")
        plt.show()

    def plot_trading(self, data):
        plt.figure(figsize=(12, 6))
        plt.title(f"{self.name} Strategy - Trading Signals")
        plt.plot(data['Date'], data['Close'], label='Price', color='blue')
        plt.scatter(data['Date'][data['Signal'] == "Buy"], data['Close'][data['Signal'] == "Buy"], marker='^', color='green')
        plt.scatter(data['Date'][data['Signal'] == "Sell"], data['Close'][data['Signal'] == "Sell"], marker='v', color='red')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def make_data(self, manual_params):
        signal_map = {'Buy': 1, 'Sell': -1}
        strategy_df = self.apply_strategy(self.base_df.copy(), manual_params)
        gain = self.backtest_strategy(strategy_df)
        print(f"Manual parameters gain: {gain}")
        self.plot_trading(strategy_df)
        strategy_df.to_csv(f'./{self.name}_trade.csv', index=False)

class LabelStrategy(Strategy):
    def __init__(self, data_path='./data.csv'):
        super().__init__("Label", data_path)
        self.base_df = self.base_df.drop('Value', axis=1)
        self.param_names = ['Buy_Label', 'Sell_Label']

        # Define label mapping
        self.label_map = {
            "Extreme Fear": -2,
            "Fear": -1,
            "Neutral": 0,
            "Greed": 1,
            "Extreme Greed": 2
        }
        self.base_df["Factor"] = self.base_df['Label'].map(self.label_map)
        self.base_df = self.base_df.drop('Label', axis=1)

    def apply_strategy(self, df, params):
        """Apply label-based strategy"""
        buy, sell = params
        df['Signal'] = None
        df.loc[df['Factor'] <= buy, 'Signal'] = 'Buy'
        df.loc[df['Factor'] >= sell, 'Signal'] = 'Sell'
        return df

    def generate_parameters(self):
        """Generate all valid parameter combinations"""
        param_combinations = []
        factors = self.base_df['Factor'].unique()
        for buy in factors:
            for sell in factors:
                if buy != sell:  # Avoid buy == sell
                    param_combinations.append((buy, sell))
        return param_combinations

    def run_optimization(self):
        """Complete optimization pipeline"""
        print("Running Label Strategy Optimization...")
        self.compare_params()
        self.plot_results(self.param_names[0], self.param_names[1], 'Gain', 'Buy', 'Sell', 'Gain')

class SharpStrategy(Strategy):
    def __init__(self, data_path='./data.csv'):
        super().__init__("Sharp", data_path)
        self.base_df = self.base_df.drop('Label', axis=1)
        self.param_names = ['MA', 'Porog', 'Buy_Threshold', 'Sell_Threshold']
        # Strategy parameters
        self.ma_list = [3, 5, 7]
        self.porog_list = [0.75, 1, 1.25, 1.5, 1.75]
        self.buy_thresholds = range(10, 50, 5)
        self.sell_thresholds = range(75, 50, -1)

    def apply_strategy(self, df, params):
        """Apply sharp ratio strategy"""
        ma, porog, buy_thresh, sell_thresh = params
        # Calculate moving average and deviation
        df[f'Index_MA{ma}'] = df['Value'].rolling(window=ma, min_periods=1).mean()
        df['Deviation'] = df['Value'] - df[f'Index_MA{ma}']
        std_dev = df['Deviation'].std(ddof=0)
        df['Jump'] = df['Deviation'].abs() > (porog * std_dev)

        # Generate signals
        df['Signal'] = None
        df.loc[df['Jump'] & (df['Value'] < buy_thresh), 'Signal'] = 'Buy'
        df.loc[df['Jump'] & (df['Value'] > sell_thresh), 'Signal'] = 'Sell'

        return df

    def generate_parameters(self):
        """Generate all parameter combinations"""
        param_combinations = []
        for ma in self.ma_list:
            for porog in self.porog_list:
                for buy in self.buy_thresholds:
                    for sell in self.sell_thresholds:
                        param_combinations.append((ma, porog, buy, sell))
        return param_combinations

    def run_optimization(self):
        """Complete optimization pipeline"""
        print("Running Sharp Strategy Optimization...")
        self.compare_params()
        self.plot_results(self.param_names[0], self.param_names[1], 'Gain', 'MA', 'Porog', 'Gain')
        self.plot_results(self.param_names[2], self.param_names[3], 'Gain', 'Buy', 'Sell', 'Gain')

class StaticStrategy(Strategy):
    def __init__(self, data_path='./data.csv'):
        super().__init__("Static", data_path)
        self.base_df = self.base_df.drop('Label', axis=1)
        self.param_names = ['Buy_Threshold', 'Sell_Threshold']
        # Strategy parameters
        self.buy_thresholds = range(5, 50, 5)
        self.sell_thresholds = range(50, 80, 5)

    def apply_strategy(self, df, params):
        """Apply static threshold strategy"""
        buy, sell = params
        df['Signal'] = None
        df.loc[df['Value'] < buy, 'Signal'] = 'Buy'
        df.loc[df['Value'] >= sell, 'Signal'] = 'Sell'
        return df

    def generate_parameters(self):
        """Generate all parameter combinations"""
        param_combinations = []
        for buy in self.buy_thresholds:
            for sell in self.sell_thresholds:
                param_combinations.append((buy, sell))
        return param_combinations

    def run_optimization(self):
        """Complete optimization pipeline"""
        print("Running Static Strategy Optimization...")
        self.compare_params()
        self.plot_results(self.param_names[0], self.param_names[1], 'Gain', 'Buy', 'Sell', 'Gain')
