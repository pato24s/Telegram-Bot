import pandas as pd
from haversine import haversine



def getAllFromADataframeWithBankingNetwork(aDataFrame, aBankingNetwork):
	return aDataFrame.loc[(aDataFrame.RED==aBankingNetwork)]


def getNearestAtms(aLocation, aBankingNetwork):
	user_lat = aLocation.latitude
	user_lon = aLocation.longitude

	# for testing
	# user_lat = -34.5702815
	# user_lon = -58.4440812

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

	atms_lats = final_df['LAT'].tolist()

	atms_lons = final_df['LNG'].tolist()

	msg = ""

	url= "https://static-maps.yandex.ru/1.x/?lang=en_US&ll="+str(user_lon)+","+str(user_lat)+"&size=650,450&z=17&l=map&pt="+str(user_lon)+","+str(user_lat)+",home"


	for idx in range(0,len(atms_banks)):
		msg = msg + str(idx+1) + ". " + atms_banks[idx] + " - " + atms_addresses[idx] + "\n"
		url = url +"~"+ str(atms_lons[idx]) + "," + str(atms_lats[idx]) + ",pm2gnl"+ str(idx+1)



	return (msg, url)
