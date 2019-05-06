#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

class User:
    def __init__(self):
        try:
            with open('config.json', 'r') as json_data_file:
                dataConfig          = json.load(json_data_file)
                self.username       = dataConfig['username']
                self.password       = dataConfig['password']
                self.refreshTime    = dataConfig['refreshTime']
                self.logged         = False
        except KeyError as e:
            return {"code":404, "message":"Key not found in config.json: " + str(e)}
        userAgent           = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.103 Chrome/73.0.3683.103 Safari/537.36"
        self.clientId       = "frontweb"
        self.grant_type     = "password"
        self.apiUrl         = "https://api.leboncoin.fr/api"
        self.requestHeaders = {
            'Accept':           'application/json',
            'Accept-Language':  'fr,en-US;q=0.9,en;q=0.8,pl;q=0.7,de;q=0.6',
            'Accept-Encoding':  'gzip, deflate, br',
            'Content-Type':     'application/x-www-form-urlencoded',
            'Origin':           'https://www.leboncoin.fr',
            'User-Agent':       userAgent
        }

    def auth(self):
        endpoint = "/oauth/v1/token"
        self.requestHeaders['Referer'] = "https://www.leboncoin.fr/"

        if self.logged:
            return {"code":200, "message":"You are already logged with user " + str(self.username)}
        requestDatas = {
            'client_id':    self.clientId,
            'grant_type':   self.grant_type,
            'password':     self.password,
            'username':     self.username
        }
        r = requests.post(self.apiUrl + endpoint, headers=self.requestHeaders, data=requestDatas, verify=True)
        ret = r.json()
        if r.status_code != 200:
            return {"code":r.status_code, "message":str(ret)}
        authToken = ret['access_token']
        self.requestHeaders['Authorization'] = "Bearer " + str(authToken)
        self.logged = True
        return {"code":r.status_code, "message":"You are logged with user " + str(self.username)}

    def me(self):
        endpoint = "/accounts/v1/accounts/me/personaldata"
        self.requestHeaders['Referer'] = "https://www.leboncoin.fr/"
        
        if not self.logged:
            return {"code":403, "message":"User not logged"}
        profile = requests.get(self.apiUrl + endpoint, headers=self.requestHeaders, verify=True)
        if profile.status_code != 200:
            return {"code":r.status_code, "message":str(ret)}
        self.myProfile = profile.json()
        return {"code":200, "message":self.myProfile}
    
    def getAds(self):
        endpoint = "/dashboard/v1/search"
        self.requestHeaders['Referer'] = "https://www.leboncoin.fr/"
        
        if not self.logged:
            return {"code":403, "message":"User not logged"}
        requestDatas = {
            'context':          "default",
            'filters':          {'owner':{"store_id":str(self.myProfile['storeId'])}},
            'limit':            10,
            'offset':           0,
            'sort_by':          "date",
            'sort_order':       "desc",
            'include_inactive': True
        }
        r = requests.post(self.apiUrl + endpoint, headers=self.requestHeaders, data=json.dumps(requestDatas), verify=True)
        ret = r.json()
        if r.status_code != 200:
            return {"code":r.status_code, "message":str(ret)}
        self.myAds = ret['ads']
        return {"code":200, "message":self.myAds}
