import investpy
import matplotlib.pyplot as plt

df_btc = investpy.get_crypto_historical_data(
	crypto='bitcoin', 
	from_date='01/01/2020', to_date='09/06/2020')
df_eth = investpy.get_crypto_historical_data(
	crypto='ethereum', 
	from_date='01/01/2020', to_date='09/06/2020')
df_dow = investpy.get_index_historical_data(
	index='Dow 30', country = 'united states', 
	from_date='01/01/2020', to_date='09/06/2020')

df_merged_btc_eth = df_btc.merge(df_eth, on='Date') 
df_merged_btc_eth = df_merged_btc_eth.drop(
					['Open_x','High_x','Low_x','Volume_x',
					'Currency_x','Open_y','High_y','Low_y','Volume_y'], axis=1)
df_merged_btc_eth = df_merged_btc_eth.rename(
					columns={"Close_x":"Close_BTC","Close_y":"Close_ETH"})
df_merged_btc_eth_dow = df_merged_btc_eth.merge(df_dow, on='Date') 
df_merged_btc_eth_dow = df_merged_btc_eth_dow.drop(
					['Open','High','Low','Volume','Currency_y'], axis=1)
df_merged_btc_eth_dow = df_merged_btc_eth_dow.rename(
					columns={"Close":"Close_DOW"})
df_merged_btc_eth_dow = df_merged_btc_eth_dow.drop(['Currency'],axis=1)
df_merged_btc_eth_dow['Close_BTC'] = ((df_merged_btc_eth_dow['Close_BTC'] / \
                                     df_merged_btc_eth_dow['Close_BTC'].iloc[0])-1)*100
df_merged_btc_eth_dow['Close_ETH'] = ((df_merged_btc_eth_dow['Close_ETH'] / \
                                     df_merged_btc_eth_dow['Close_ETH'].iloc[0])-1)*100
df_merged_btc_eth_dow['Close_DOW'] = ((df_merged_btc_eth_dow['Close_DOW'] / \
                                     df_merged_btc_eth_dow['Close_DOW'].iloc[0])-1)*100

with plt.xkcd():
	df_merged_btc_eth_dow.plot()
	plt.title('Veränderung seit 1.1.2020')
	plt.xlabel('Datum')
	plt.ylabel('Veränderung in %')
	plt.show()