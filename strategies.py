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
    def apply_strategy(self, df: pd.DataFrame, params: tuple) -> pd.DataFrame:
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
            metrics = self.backtest_strategy(st_df, return_df=False)
            results.append(params + (metrics['Gain'], metrics['Sharpe'], metrics['MaxDrawdown']))

        col_names = list(self.param_names) + ['Gain', 'Sharpe', 'MaxDrawdown']
        self.results_df = pd.DataFrame(results, columns=col_names)  # Build results DataFrame
        self.find_the_best()

    def calculate_metrics(self, df, initial_cash):
        """Calculate advanced performance metrics"""
        equity = df['Equity'].values
        returns = df['Equity'].pct_change().dropna()
        
        # Total Gain
        total_gain = equity[-1] - initial_cash
        
        # Sharpe Ratio (assuming daily data, annualized)
        # Risk-free rate assumed to be 0 for simplicity
        if len(returns) > 1 and returns.std() != 0:
            sharpe = (returns.mean() / returns.std()) * np.sqrt(365)
        else:
            sharpe = 0
            
        # Maximum Drawdown
        peak = np.maximum.accumulate(equity)
        drawdown = (peak - equity) / peak
        max_drawdown = drawdown.max()
        
        # Trade Stats
        trades = df[df['Trade'].isin(['buy', 'sell'])]
        num_trades = len(trades)
        
        return {
            'Gain': total_gain,
            'Sharpe': sharpe,
            'MaxDrawdown': max_drawdown,
            'NumTrades': num_trades
        }

    def backtest_strategy(self, data, return_df=True):
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

        metrics = self.calculate_metrics(df, initial_cash)
        
        if return_df:
            return df, metrics
        return metrics

    def find_the_best(self, confidence_level=0.95):
        if self.results_df.empty:
            return False
            
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
            print(f"\n--- Best {self.name} Strategy Found ---")
            print(best_params)
            return True
        else:
            print(f"Best {self.name} result may not be statistically significant")
            return False

    def plot_results(self, x_col, y_col, z_col, x_label, y_label, z_label):
        """Plot 3D results"""
        if self.results_df.empty:
            return
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.results_df[x_col], self.results_df[y_col], self.results_df[z_col])
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        plt.title(f"{self.name} Strategy - {x_label} vs {y_label} vs {z_label}")
        plt.show()

    def plot_trading(self, data, metrics=None):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        dates = pd.to_datetime(data['Date'])
        
        # Plot 1: Price and Signals
        ax1.set_title(f"{self.name} Strategy - Trading Signals")
        ax1.plot(dates, data['Close'], label='Price', color='blue', alpha=0.6)
        
        buy_signals = data[data['Signal'] == "Buy"]
        sell_signals = data[data['Signal'] == "Sell"]
        
        ax1.scatter(pd.to_datetime(buy_signals['Date']), buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)
        ax1.scatter(pd.to_datetime(sell_signals['Date']), sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)
        ax1.set_ylabel('BTC Price')
        ax1.legend()

        # Plot 2: Equity Curve vs Benchmark
        initial_equity = data['Equity'].iloc[0]
        benchmark = (data['Close'] / data['Close'].iloc[0]) * initial_equity
        
        ax2.plot(dates, data['Equity'], label='Strategy Equity', color='purple', linewidth=2)
        ax2.plot(dates, benchmark, label='Buy & Hold Benchmark', color='gray', linestyle='--', alpha=0.7)
        ax2.set_ylabel('Equity ($)')
        ax2.set_xlabel('Date')
        ax2.legend()
        
        if metrics:
            textstr = '\n'.join((
                f"Total Gain: ${metrics['Gain']:.2f}",
                f"Sharpe Ratio: {metrics['Sharpe']:.2f}",
                f"Max Drawdown: {metrics['MaxDrawdown']*100:.2f}%",
                f"Total Trades: {metrics['NumTrades']}"
            ))
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax2.text(0.02, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)

        fig.autofmt_xdate(rotation=45)
        plt.tight_layout()
        plt.show()

class LabelStrategy(Strategy):
    def __init__(self, data_path='./data.csv'):
        super().__init__("Label", data_path)
        if 'Value' in self.base_df.columns:
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
        # Keep 'Label' for visualization or remove it if not needed
        # self.base_df = self.base_df.drop('Label', axis=1)

    def apply_strategy(self, df, params):
        """Apply label-based strategy"""
        buy, sell = params
        df['Signal'] = None
        df.loc[df['Factor'] == buy, 'Signal'] = 'Buy'
        df.loc[df['Factor'] == sell, 'Signal'] = 'Sell'
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
        # self.base_df = self.base_df.drop('Label', axis=1)
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
        # self.base_df = self.base_df.drop('Label', axis=1)
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
