import time
from datetime import datetime, timedelta
import os, re, sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto

#Import s3 credentials from ubuntu directory
cred_file = open('/home/ubuntu/keys/s3_creds_mmx.json')
creds = json.load(cred_file)
AWS_ACCESS_KEY_ID = creds['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = creds['aws_secret_access_key']

cur_date = datetime.now() #+ timedelta(hours=8)
time_stamp = str(cur_date)
year = str(cur_date.year)
month = str(cur_date.month)
day = str(cur_date.day)
hour = str(cur_date.hour)
date_plug = 'y='+year+'/m='+month+'/d='+day+'/h='+hour+'/'
ubuntu_filename = '/home/ubuntu/repo/flatfiles/weatherdata_'+time_stamp+'.csv'
s3_filename = 'weather_underground/'+date_plug+'weatherdata_'+time_stamp+'.csv'

#write files to s3 bucket
s3 = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
bucket = s3.get_bucket('metamx-shecht')
key = bucket.new_key(s3_filename)
key.set_contents_from_filename(ubuntu_filename)