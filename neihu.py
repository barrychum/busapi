from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
from pprint import pprint
import os
import json

from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

app_id = os.getenv('APP_ID')
app_key = os.getenv('APP_KEY')

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    count = "top=2000"
    format = "format=JSON"
    #扶輪公園(文化三路)
    #spatial = "spatialFilter=nearby(25.07487083476023, 121.36843819824628,20)"

    #文化三路忠孝路口
    #spatial = "spatialFilter=nearby(25.073447,121.366133,20)"

    #仁寶大樓
    spatial = "spatialFilter=nearby(25.079478,121.568256,25)"

    # $top=2000&$spatialFilter=nearby(25.07403647840011%2C%20121.3666265687397%2C500)&$format=JSON"

    # ETA url
    url2 = "NearBy?$%s&$%s&$%s" % (count,format,spatial)
    url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/"
    url += url2

    response = request('get', url, headers= a.get_auth_header())
    x = json.loads(response.content)

    results = []
    for item in x:
        try:
            result = {
                "StopID": item['StopID'],
                "EstimateTime": item['EstimateTime'],
                "ETA": float(item['EstimateTime']) / 60
            }
        except:
            result = {
                "StopID": item['StopID'],
                "EstimateTime": "-1",
                "ETA": -1.0
            }
        results.append(result)

    # Stop ID url
    url2 = "NearBy?$%s&$%s&$%s" % (count,format,spatial)
    url = "https://ptx.transportdata.tw/MOTC/v2/Bus/Station/"
    url += url2

    response = request('get', url, headers= a.get_auth_header())
    x = json.loads(response.content)

    for item in x:
        lineout = "StationID:%s|StationName:%s|%s,%s,%s" % \
            (item['StationID'], item['StationName']['Zh_tw'], \
            item['Bearing'], \
            item['StationPosition']['PositionLat'],item['StationPosition']['PositionLon'] )

        print(lineout)
        temparr = []
        watchlist = ["946","946sub"]
        for stop in item['Stops']:
            if stop['RouteName']['En'] in watchlist:
                temp = "%s" % (stop['RouteName']['En'])
                temp += "|%.1f" % ([i for i in results if i['StopID']==stop['StopID']][0]['ETA'])
                temp += "|%s" % ([i for i in results if i['StopID']==stop['StopID']][0]['EstimateTime'])
                temp += "|%s" % (stop['StopID'])
                temparr.append(temp)
                print(temp)
