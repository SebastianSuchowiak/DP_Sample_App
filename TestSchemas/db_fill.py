import requests
import json

URL_PREFIX = 'http://127.0.0.1:5000'
headers = {'content-type': 'application/json'}
r = requests.post(URL_PREFIX + '/login/login',json={'username' : 'use1', 'password' : 'pw1'})
print(r.text)

print(r.url)