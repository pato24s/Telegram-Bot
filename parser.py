import pandas as pd
from haversine import haversine



def getAllFromADataframeWithBankingNetwork(aDataFrame, aBankingNetwork):
	return aDataFrame.loc[(aDataFrame.RED==aBankingNetwork)]


def getNearestAtms(aLocation, aBankingNetwork):
	user_lat = aLocation.latitude
	user_lon = aLocation.longitude

	user_location = (user_lat, user_lon)

	data=pd.read_csv('./data/cajeros-automaticos/cajeros-automaticos.csv', sep='	')

	df = pd.DataFrame(data)
	
	distances = []
	
	for index, row in df.iterrows():
		atm_location = (row.LAT, row.LNG)
		distances.append(haversine(atm_location, user_location)*1000)

	newCol = pd.DataFrame({'DISTANCIA':distances})

	df= df.join(newCol)

	filtered_by_network_df = getAllFromADataframeWithBankingNetwork(df,aBankingNetwork)

	sorted_by_distance_df = filtered_by_network_df.sort_values(by='DISTANCIA', ascending=True)

	final_df = sorted_by_distance_df.head(3)

	final_df = final_df.loc[final_df.DISTANCIA < 500]

	atms_banks = final_df['BANCO'].tolist()

	atms_addresses = final_df['DOM_NORMA'].tolist()

	res = ""

	for idx in range(0,len(atms_banks)):
		res = res + str(idx+1) + ". " + atms_banks[idx] + " - " + atms_addresses[idx] + "\n" 



	return res
