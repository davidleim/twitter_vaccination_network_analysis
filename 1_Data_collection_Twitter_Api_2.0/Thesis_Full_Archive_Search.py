#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 10:14:18 2020

@author: David
"""

import requests
import pandas as pd
from datetime import datetime
import time

filename = 'twitter_'+ datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
bearer_token = "XXXXXXXXX"

search_url = "https://api.twitter.com/2/tweets/search/all"

query_params = {'query': '(impfen OR impfpflicht OR impfe OR impfquote OR vakzin OR impfzentrum OR impfstoff OR impf OR impfgegner OR impfpass OR impfstoff OR pfizer OR biontech OR moderna OR Astrazeneca) (lang:de)',
                'tweet.fields': 'author_id,in_reply_to_user_id,referenced_tweets,created_at,entities,lang,conversation_id,id,text,geo,public_metrics',
                'max_results' : '100',
                'start_time' : '2019-09-01T00:00:00Z',
                'end_time' : '2020-01-29T11:18:20.00Z',
                'next_token' : None
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


def main():
    count = 0
    results = []
    max_results = 9000000
    headers = create_headers(bearer_token)
    global json_response
    json_response = connect_to_endpoint(search_url, headers, query_params)
    while count < max_results:
        result_count = json_response["meta"]["result_count"]
        if "next_token" in json_response["meta"]:
            #Looks like this works
            global next_token
            next_token = json_response["meta"]['next_token']
            f = open( 'lastnextvalue.txt', 'w' )
            f.write( 'str = ' +next_token + '\n' )
            if result_count is not None and result_count > 0:
                for tweet in json_response["data"]:
                    print(tweet["id"])
                    results.append(tweet)
                count += result_count
                print("Currently retrieved results:", count)
                if result_count % 10 == 0:
                    df = pd.DataFrame(results)
                    df.to_csv(filename + ".csv")
                    print("saved")
                time.sleep(4)
                query_params['next_token'] = json_response["meta"]["next_token"]
                json_response = connect_to_endpoint(search_url, headers, query_params)
        else:
            break
    print("Total: {}".format(count))
    return(results)


if __name__ == "__main__":
   results = main()
   
#%% Export Data

df = pd.DataFrame(results)
df.to_csv('twitter_da_'+ datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.csv')    