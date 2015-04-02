"""
Finds the walking distance and duration from every* subway station in NYC to every undergraduate CUNY school
and saves information to csv file.

*broken into three subsections due to API limitations (2,500 elements per day)

Example call: python Cuny.py <START_INDEX> <END_INDEX> <GOOGLE_API_KEY> <SAVE_FILE>.csv

Author: Nicholas Hagans and Kelly Binder
Version: 04/02/15
"""

import googlemaps
import pandas as pd
from sys import argv
import csv
from os import path

#grabs start and end index, api key, and filename to save to from command line
script, start, end, key, filename = argv
start = int(start)
end = int(end)

#google map api
gmaps = googlemaps.Client(key=key)

#read in data about CUNY schools and subway stations
schools = pd.read_csv('CUNY.csv')
subway = pd.read_csv('subway_stations.csv')

#create dictionary to hold data from api call
final_dict = {}

#subway index loop
for i in range(start,end):
    #set waypoint to subway station coordinate
    waypoint2 = str(subway.get_value(i, 'Y')) + "," + str(subway.get_value(i,'X'))
    #CUNY school index loop
    for j in range(0,len(schools)):
        #set waypoint to school coordinate
        waypoint1 = str(schools.get_value(j, 'Latitude')) + "," + str(schools.get_value(j,'Longitude'))

        #gets json object from google using distance_matrix
        route = gmaps.distance_matrix(origins = [waypoint2],
									destinations = [waypoint1],
                                    mode="transit",
                                    language="English",
                                    units="imperial")

        #obtain distance and duration information from JSON
        distance = route["rows"][0]["elements"][0]["distance"]["value"]
        duration = route["rows"][0]["elements"][0]["duration"]["value"]

	#set dictionary key to subway name/coordinates and school name/coordinates and value to list of distance and duration
	final_dict[subway.get_value(i, 'NAME'),subway.get_value(i, 'Y'),subway.get_value(i, 'X'),schools.get_value(j, 'institution name'),schools.get_value(j, 'Latitude'),schools.get_value(j, 'Longitude') ] = [distance,duration]

#look for file to save to
filepath = path.dirname(path.realpath(argv[0])) + '\\' + filename

#if file exists, append dictionary to file
if path.exists(filepath) and path.isfile(filepath):
    with open(filename, 'ab') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in final_dict.keys():
            spamwriter.writerow([i[0],i[1],i[2],i[3],i[4],i[5],final_dict[i][0], final_dict[i][1]])
#else create file with column titles and write dictionary to file
else:
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Subway','Subway lat', 'Subway Lng','School','School Lat', 'School Lng','Distance', 'Time'])
        for i in final_dict.keys():
            spamwriter.writerow([i[0],i[1],i[2],i[3],i[4],i[5],final_dict[i][0], final_dict[i][1]])
