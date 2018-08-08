import pandas as pd
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

user_lat = -34.5700474
user_lon = -58.4449395


def getAllFromADataframeWithBankingNetwork(aDataFrame, aBankingNetwork):
	return aDataFrame.loc[(aDataFrame.RED==aBankingNetwork)]





def distanceXY(lat1, lon1, lat2, lon2):
	global R
	# lat1 = aPairOfCoordiantes[0]
	# lon1 = aPairOfCoordiantes[1]
	# lat2 = anotherPairOfCoordinates[0]
	# lon2 = anotherPairOfCoordinates[1]



	# print(lat1)
	# print(lon1)
	# print(lat2)
	# print(lon2)

	dlon = lon2 - lon1
	# print(dlon)
	dlat = lat2 - lat1
	# print(dlat)

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	# print(c)
	distance = (R * c)
	# print(distance)
	return distance



data=pd.read_csv('./data/cajeros-automaticos/cajeros-automaticos.csv', sep='	')
# print (data)

df = pd.DataFrame(data)

distances = []
for index, row in df.iterrows():
	distances.append(distanceXY(user_lat, user_lon, row.LAT, row.LNG))

newCol = pd.DataFrame({'distancias':distances})

df= df.join(newCol)



banelco = getAllFromADataframeWithBankingNetwork(df,'BANELCO')

link = getAllFromADataframeWithBankingNetwork(df, 'LINK')

banelco.to_csv('banelco.csv')

link.to_csv('link.csv')