import requests
import json

URL_PREFIX = 'http://127.0.0.1:5000'
headers = {'content-type': 'application/json'}


def test_user(username,password):
    r = requests.post(URL_PREFIX + '/login/login',json={'username' : username, 'password' : password})
    print(r.text)
    result_tokentype = r.json()["token_type"]
    result_accesstoken = r.json()["access_token"]
    accessToken = str(result_tokentype) + " " + str(result_accesstoken)
    headers = {"Authorization": accessToken, "key1": "value1", "Content-Type": "application/json" }
    r = requests.get(URL_PREFIX + '/employee/employees' , headers= headers)
    print(r.json())
    #print(r.json)

    #r = requests.post(URL_PREFIX + '/login/logout')
    #print(r.text)

test_user('u1','p1')

