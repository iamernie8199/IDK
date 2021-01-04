import pandas as pd
import datetime

df = pd.read_csv('data/TWF.FITX HOT 1 Minute.txt')
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d').apply(lambda x: x.strftime('%Y-%m-%d'))
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

stat = df[df.Time <= datetime.time(9, 30)][['Date', 'Close']].groupby('Date').last()[1:]
stat['l_Dc'] = df[['Date', 'Close']].groupby('Date').last().shift(1)

# 930時收益率
stat['r0930'] = stat['Close'] / stat['l_Dc'] - 1
# 加權開盤前30分鐘最大獲益(多/空)
stat['0930_b_h'] = df[df.Time <= datetime.time(9, 30)][['Date', 'High']].groupby('Date').max()
stat['r0930_b_h'] = stat['0930_b_h'] / stat['l_Dc'] - 1
stat['0930_b_l'] = df[df.Time <= datetime.time(9, 30)][['Date', 'Low']].groupby('Date').min()
stat['r0930_b_l'] = stat['0930_b_l'] / stat['l_Dc'] - 1
# 930後最大獲益(多/空)
stat['0930_a_h'] = df[df.Time > datetime.time(9, 30)][['Date', 'High']].groupby('Date').max()
stat['r0930_a_h'] = stat['0930_a_h'] / stat['l_Dc'] - 1
stat['0930_a_l'] = df[df.Time > datetime.time(9, 30)][['Date', 'Low']].groupby('Date').min()
stat['r0930_a_l'] = stat['0930_a_l'] / stat['l_Dc'] - 1
# 當天收益率
stat['Dc'] = df[['Date', 'Close']].groupby('Date').last()
stat['rDc'] = stat['Dc'] / stat['l_Dc'] - 1
# 當天最大獲益
stat['Dh'] = df[['Date', 'High']].groupby('Date').max()
stat['rDh'] = stat['Dh'] / stat['l_Dc'] - 1
stat['Dl'] = df[['Date', 'Low']].groupby('Date').min()
stat['rDl'] = stat['Dl'] / stat['l_Dc'] - 1

stat = stat[['r0930','r0930_b_h','r0930_b_l','r0930_a_h','r0930_a_l','rDc','rDh','rDl']]

print(f"r0930 < rDc: {round((stat['r0930']<stat['rDc']).sum()/len(stat),4)*100}%")
print(f"r0930_b_h < rDh: {round((stat['r0930_b_h']<stat['rDh']).sum()/len(stat),4)*100}%")

