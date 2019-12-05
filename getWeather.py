import requests
import json
from influxdb import InfluxDBClient


#pull data from config file
config_file = open("config.json", "r")
config_json = json.load(config_file)


#--------------------------------------------------------
#Get weather information from openweather
#--------------------------------------------------------
zip = "60564"
print("Getting zip " + zip)

url = "https://api.openweathermap.org/data/2.5/weather?zip="+zip+"&APPID="+config_json['openweathermap_appid']+"&units=imperial"
response = requests.request("GET", url)
json_data = json.loads(response.text)

print("Got this data back:")
print(json_data)

#--------------------------------------------------------
#post data to influxdb
#--------------------------------------------------------
json_body = [
    {
        "measurement": "main",
        "tags": {
            "zip": zip,
            "timezone":json_data["timezone"],
            "name":json_data["name"]
        },
        "fields": json_data["main"]
    }
]

client = InfluxDBClient(host='192.168.103.40', port=8086, username=config_json['influxdb_user'], password=config_json['influxdb_pass'],database='weather')
response = client.write_points(json_body)

print(response)




