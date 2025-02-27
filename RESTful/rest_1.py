'''

'''
import requests
import json

headers = {"content-type": "application/json"}
payload = json.dumps({ "name": "Apple AirPods", "data": { "color": "white", "generation": "3rd", "price": 135}})
requestUrl = "https://api.restful-api.dev/objects/6"
r = requests.put(requestUrl, data=payload, headers=headers)

print(r.content)