#!/usr/bin/python3
# -*- encoding: utf8 -*-

'''
Created on Mar 28, 2017

@author: Jack Rausch
'''
import http.client
import json
import ssl
import tbapy
#import requests

URL = "http://www.thebluealliance.com/api/v2/"
HEADER_KEY = "X-TBA-App-Id"
HEADER_VAL = 'frc4215:data-analysis:.1'

#I was thinking that we should turn this into a class so that we can have an instance for each regional
def api_is_up():
    conn = http.client.HTTPConnection(URL,80)
    conn.request('GET',"/status",{HEADER_KEY : HEADER_VAL})
    response = conn.getresponse()
    return response.read()

def get_event_teams(event_key):
    tba = tbapy.TBA(HEADER_VAL)
    jsonified = tba.event_teams(event_key)
    teams = []
    for team in jsonified:
        teams.append(team["key"])

    return teams

teams = get_event_teams('2010sc')
print(teams)
#up = api_is_up()
#print(up)
