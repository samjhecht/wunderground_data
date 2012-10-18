#http://www.wunderground.com/weather/api/d/docs
import urllib2
import json, csv
import pprint as pp
import random
import time
from datetime import datetime, timedelta
import os, re, sys

def convert_dataypes(x):
    try:
        return float(re.sub('[$-+]', '', x))
    except Exception, e:
        return x

def get_json(url):
    try:
        src = urllib2.urlopen(url).read()
        rsp = json.loads(src)
    except:
        rsp = {}
    return rsp

def get_hour():
    hourdict = {0: '0:00-1:00', 1: '1:00-2:00', 2: '2:00-3:00', 3: '3:00-4:00', 4: '4:00-5:00', 5: '5:00-6:00',
                6: '6:00-7:00', 7: '7:00-8:00', 8: '8:00-9:00', 9: '9:00-10:00', 10: '10:00-11:00', 11: '11:00-12:00', 
                12: '12:00-13:00', 13: '13:00-14:00', 14: '14:00-15:00', 15: '15:00-16:00', 16: '16:00-17:00', 17: '17:00-18:00', 
                18: '18:00-19:00', 19: '19:00-20:00', 20: '20:00-21:00', 21: '21:00-22:00', 22: '22:00-23:00', 23: '23:00-24:00'}
    now = datetime.now() #+ timedelta(hours=8)
    cur_hour = now.hour
    return hourdict.get(cur_hour)

dirname, filename = os.path.split(os.path.abspath(__file__))

APIKEY = '044338cd9ff00333'

base_uri = "http://api.wunderground.com/api/044338cd9ff00333/"

# define some stocks
cities = [line.strip() for line in open(dirname + '/cities.txt').read().split('\n')]
#encapsulate for the query
cities = ["" + city + "" for city in cities]

random.shuffle(cities)

cur_date = datetime.now() #+ timedelta(hours=8)
time_stamp = str(cur_date)
year = str(cur_date.year)
month = str(cur_date.month)
day = str(cur_date.day)
hour = str(cur_date.hour)
date_plug = 'y='+year+'/m='+month+'/d='+day+'/h='+hour+'/'
sammac_filename = '/Users/admin/Desktop/demo_data/weather/flatfiles/weatherdata_'+time_stamp+'.csv'
#ubuntu_filename = '/home/ubuntu/repo/flatfiles/weatherdata_'+time_stamp+'.csv'
#s3_filename = 'weatherdata/'+date_plug+'weatherdata_'+time_stamp+'.csv'

f = open(sammac_filename, 'wb')
w = csv.writer(f)
columns = [u'UV',u'dewpoint_c',u'dewpoint_f',u'dewpoint_string',u'display_location',u'estimated',u'feelslike_c',u'feelslike_f',u'feelslike_string',u'forecast_url',u'heat_index_c',u'heat_index_f',u'heat_index_string',u'history_url',u'icon',u'icon_url',u'image',u'local_epoch',u'local_time_rfc822',u'local_tz_long',u'local_tz_offset',u'local_tz_short',u'ob_url',u'observation_epoch',
		   u'observation_location',u'observation_time',u'observation_time_rfc822',u'precip_1hr_in',u'precip_1hr_metric',u'precip_1hr_string',u'precip_today_in',u'precip_today_metric',u'precip_today_string',u'pressure_in',u'pressure_mb',u'pressure_trend',u'relative_humidity',u'solarradiation',u'station_id',u'temp_c',u'temp_f',u'temperature_string',u'visibility_km',u'visibility_mi',u'weather',
		   u'wind_degrees',u'wind_dir',u'wind_gust_kph',u'wind_gust_mph',u'wind_kph',u'wind_mph',u'wind_string',u'windchill_c',u'windchill_f',u'windchill_string']
w.writerow(columns)

for block in range(0, len(cities), 100):
    cities_subset = cities[block:block+100]
    # define the parameters
    query = {
#        "q":"select * from yahoo.finance.quotes where symbol in (%s)" % ', '.join(cities_subset),
#        "env":"http://datatables.org/alltables.env",
#        "format":"json"
    }

    url = base_uri
    
for city in cities:
	url = 'http://api.wunderground.com/api/'+APIKEY+'/geolookup/conditions/q/'+city+'.json'
	rsp = get_json(url)
	stats = []
	if 'query' in rsp and \
		'results' in rsp['query']\
		and 'stat' in rsp['query']['results']['stat']

	for stat in stats:
		for col in stat:
			quote[col] = convert_dataypes(stat[col])
		pp.pprint(stat)
		w.writerow([stat.get(col) for col in columns])

	#u = urllib2.urlopen(query)
	#json_string = u.read()
	#parsed_json = json.loads(json_string)
	#location = parsed_json['location']['city']
	#temp_f = parsed_json['current_observation']['temp_f']
	#print "Current temperature in %s is: %s" % (location, temp_f)
	#u.close()





