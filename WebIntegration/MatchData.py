'''
Created on Mar 28, 2017

@author: Jack Rausch
'''
import http.client
import json
import ssl
#import requests

URL = 'http://www.thebluealliance.com/api/v2/'
HEADER_KEY = 'X-TBA-App-Id'
HEADER_VAL = 'frc4215:data-analysis:.1'



def get_event_teams(event_key):
    request = http.client.HTTPConnection(URL)
    #request.add_header(HEADER_KEY, HEADER_VAL)
    response = http.client.HTTPConnection(URL)
    jsonified = json.loads(response.read().decode("utf-8"))
    teams = []

    for team in jsonified:
        teams.append(team['key'])

    return teams

teams = get_event_teams("qcmo")
print(teams)
