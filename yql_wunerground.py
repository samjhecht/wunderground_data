import yql
import os
import csv
import datetime

def rowToCSV(x):
    location = x['display_location']
    return [
               x['observation_epoch'],
               location['city'],
               location['state'],
               location['country'],
               location['zip'],
               x['weather'],
               x['temp_f'],
               x['relative_humidity'],
               x['wind_dir'],
               x['wind_degrees'],
               x['wind_mph'],
               x['wind_gust_mph'],
               x['pressure_in'],
               x['dewpoint_f'],
               x['heat_index_f'],
               x['windchill_f'],
               x['visibility_mi']
           ]


dirname, filename = os.path.split(os.path.abspath(__file__))
cities = [line.strip() for line in open(dirname + '/cities.txt').read().split('\n')]
cities = "(" + ','.join(["'" + city + "'" for city in cities]) + ")"

y = yql.Public()
query = "use 'http://www.datatables.org/wunderground/wunderground.currentobservation.xml' as wunderground.currentobservation; select * from wunderground.currentobservation where location in " + cities
result = y.execute(query)

csvfile = open(dirname + str(datetime.datetime.now()), 'wb')
writer = csv.writer(csvfile, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['Timestamp', 'City', 'State', 'Country', 'Zip'
                 'feels_like', 'Temperature', 'Relative_Humidity',
                 'Wind_Direction', 'Wind_Degrees', 'Wind_mph',
                 'Wind_gust_mph', 'Pressure', 'Dewpoint'
                 'Heat_Index', 'Windchill', 'Visibility'])

for row in result.rows:
    try:
        row = rowToCSV(row)
        writer.writerow(row)
    except AttributeError:
        print("problem parsing event")
    except UnicodeEncodeError:
        print("problem writing row")

csvfile.close()
