import requests
import json

url = "http://127.0.0.1:5000/v1/CreateUrl?url=www.fox.com"

payload={}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
