"""
Makes a new csv file that contains all of the information contained in the original high school csv
as well as new columns containing the Latitude and Longitude of the high school. This information is
found by looking through the location column in the high school data from NYC's Open Data Portal.

Author: Nicholas Hagans
Version: 3/26/15
"""
import pandas as pd

# read in the high school csv file as Pandas DataFrame
highschools = pd.read_csv('highschools.csv')

# empty lists for the Latitude and Longitude
lat = []
lon = []

# loop through all rows of high school Dataframe
for x in range(0, len(highschools)):
	# get entire location string from DataFrame and pull the Latitude and Longitude from the string
    loc = highschools.get_value(x, 'Location 1')
    lat.append((float(loc[loc.find('(') + 1:loc.find(',', loc.find('(')) - 1])))
    lon.append((float(loc[loc.find(',', loc.find('(')) + 2:loc.find(')') - 1])))
    
# add Latitude and Longitude to DataFrame
highschools['Latitude'] = lat
highschools['Longitude'] = lon

# save DataFrame as new csv file
highschools.to_csv('newHighSchools.csv')