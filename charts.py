from sklearn.preprocessing import StandardScaler
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')

df = pd.read_csv('./data.csv')

color_map = {
    "Extreme Fear": "red",
    "Fear": "orange",
    "Neutral": "blue",
    "Greed": (112/255, 224/255, 0, 1),
    "Extreme Greed": "green"
}
colors = df['Label'].map(color_map)

def price_and_index_chart():
	scale = StandardScaler()
	df_scaled = scale.fit_transform(df[['Value', 'Close']])
	df_scaled = pd.DataFrame(df_scaled, columns=['Index', 'Price'])
	df_scaled.insert(0, "Date", df['Date'], False)
	df_scaled.plot(x='Date', y = ['Index', 'Price'])
	plt.show()

def plot_trading(data):
    plt.title("Signals")
    plt.plot(data['Date'], data['Close'], label='Price', color='blue')
    plt.scatter(data['Date'][data['Signal'] == "Buy"], data['Close'][data['Signal'] == "Buy"], marker='^', color='green')
    plt.scatter(data['Date'][data['Signal'] == "Sell"], data['Close'][data['Signal'] == "Sell"], marker='v', color='red')
    plt.legend()
    plt.show()

def threedimplot(x, y, z, xlabel, ylabel, zlabel):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x, y, z)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_zlabel(zlabel)
	plt.show()


# ####SUBPLOT####
# plt.subplot(2, 1, 1)
# plt.plot(df['Date'], df['Value'])
# plt.title("Index Value over Time")
# plt.subplot(2, 1, 2)
# plt.plot(df['Date'], df['Close'])
# plt.show()


# ####HEATMAP####


# ###HISTOGRAM####
# # df['Value'].plot(kind='kde')
# df['Value'].plot(kind='hist')
# plt.show()

# ###BAR####
# order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
# labels_count = df["Label"].value_counts()
# ordered_counts = labels_count.reindex(order).fillna(0).astype(int)
# labels = ordered_counts.index.to_list()
# counts = ordered_counts.to_list()
# colors = [color_map.get(label, 'gray') for label in labels]  # fallback color if needed
# plt.bar(labels, counts, color=colors)
# plt.xticks(rotation=45, ha='right')
# plt.show()

###SCATTER#####
# df.plot(kind='scatter', x='Label', y='Close', c=colors)
# plt.show()
