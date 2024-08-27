import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')
df = df.drop('Label', axis=1)