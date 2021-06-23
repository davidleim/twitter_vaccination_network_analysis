#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 12:32:34 2021

@author: David
"""

import requests as requests
import pandas as pd
import time
import json


bearer_token = "XXXXXXXX"
filename = 'twitterfollowers_'+ datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")

search_url = "https://api.twitter.com/1.1/friends/ids.json"

userid = ''
cursor = - 1

query_params = {'user_id': userid,
                'count' : '5000'
                }


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code == 429:
        time.sleep(960)
        pass
    elif response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_user_followers(userid):
    headers = create_headers(bearer_token)
    global json_response
    json_response = connect_to_endpoint(search_url, headers, {'user_id': userid,'count' : '5000'})
    return(json_response)

results = {}

def main():
    global userid
    for id in unique:
        print(userid)
        try: 
            output = get_user_followers(id)
            results[id] = output['ids']
            print('succesfully added '+ id)
        except:
            print('something went wrong with ' + id)
            pass
        with open(filename+'.json', 'w') as fp:
            json.dump(results, fp)
        time.sleep(4)
        
        

if __name__ == "__main__":
   results = main()


