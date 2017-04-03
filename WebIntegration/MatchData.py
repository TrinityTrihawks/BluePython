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
def api_is_up(): # Error when calling. Needs to be fixed if this is useful. 
    conn = http.client.HTTPConnection(URL,80)
    conn.request('GET',"/status",{HEADER_KEY : HEADER_VAL})
    response = conn.getresponse()
    return response.read()

def get_event_teams(event_key):
    tba = tbapy.TBA(HEADER_VAL)
    jsonified = tba.event_teams(event_key)
    # The next line is a condense version of line 31-34
    return [team['key'] for team in jsonified]
    #teams = []
    #for team in jsonified:
    #    teams.append(team["key"])
    #return teams

def main():
    '''
        This function is to be performed when directly run by python, otherwise it won't be performed.
    '''
    keys = [
        '2010sc', '2014mnmi',
    ]
    teamGroups = [get_event_teams(key) for key in keys]
    for teams in teamGroups:
        print(teams)
        print()

#teams = get_event_teams('2010sc')
#print(teams)

#up = api_is_up()
#print(up)

# To call main function
if '__main__' == __name__: main()


