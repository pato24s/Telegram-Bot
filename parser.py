import pandas as pd
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

user_lat = -34.6061137952
user_lon = -58.3711082913


def distanceXY(lat1, lon1, lat2, lon2):
	global R
	# lat1 = aPairOfCoordiantes[0]
	# lon1 = aPairOfCoordiantes[1]
	# lat2 = anotherPairOfCoordinates[0]
	# lon2 = anotherPairOfCoordinates[1]



	print(lat1)
	print(lon1)
	print(lat2)
	print(lon2)

	dlon = lon2 - lon1
	print(dlon)
	dlat = lat2 - lat1
	print(dlat)

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	print(c)
	distance = (R * c)
	print(distance)
	return distance



data=pd.read_csv('./data/cajeros-automaticos/cajeros-automaticos.csv', sep='	')
# print (data)

df = pd.DataFrame(data)

a = 34.2
# print(a)

banelco = df.loc[(df.RED=='BANELCO') & (distanceXY(df.LAT, df.LNG, user_lat, user_lon)==0)]
link = df.loc[df['RED']=='LINK']

# print(banelco)