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
import numpy as np
import numpy.linalg as linalg
#import requests

URL = "http://www.thebluealliance.com/api/v2/"
HEADER_KEY = "X-TBA-App-Id"
HEADER_VAL = 'frc4215:data-analysis:.1'
tba = tbapy.TBA(HEADER_VAL)
#I was thinking that we should turn this into a class so that we can have an instance for each regional
def api_is_up(): # Error when calling. Needs to be fixed if this is useful.
    conn = http.client.HTTPConnection(URL,80)
    conn.request('GET',"/status",{HEADER_KEY : HEADER_VAL})
    response = conn.getresponse()
    return response.read()

def get_event_teams(event_key):

    jsonified = tba.event_teams(event_key)
    # The next line is a condense version of line 31-34
    return [team['key'] for team in jsonified]
    #teams = []
    #for team in jsonified:
    #    teams.append(team["key"])
    #return teams

def statIowa():
    '''
        This function is to be performed when directly run by python, otherwise it won't be performed.
    '''
    reg_key = '2017iacf'
    # gathering data
    teamGroups = get_event_teams(reg_key)

    # Setting up to solve for gear points
    gear_matrix = []
    gear_scores = [0] * 81

    #Setting up to solve for fuel points
    fuel_matrix = []
    fuel_scores = [0]*81

    #Setting up to solve for fuel points
    auto_matrix = []
    auto_scores = [0]*81

    # setting up sort of oprs
    opr_teams = []
    opr_unsorted = tba.event_stats(reg_key)['oprs']
    for team in teamGroups:
        opr_teams.append(opr_unsorted[team[3:len(team)]])

        gear_coloumn = [0] * 81
        auto_coloumn = [0] * 81
        fuel_coloumn = [0] * 81

        matches = tba.team_matches(team,reg_key)
        for match in matches:
            if match['comp_level'] == 'qm':
                alliance = 'blue'

                for member in match['alliances']['red']['teams']:
                    if team == member:
                        alliance = 'red'
                gear_coloumn[match['match_number']-1] = 1
                auto_coloumn[match['match_number']-1] = 1
                fuel_coloumn[match['match_number']-1] = 1

                gear_scores[match['match_number']-1] = match['score_breakdown'][alliance]['teleopRotorPoints']
                fuel_scores[match['match_number']-1] = match['score_breakdown'][alliance]['teleopFuelPoints']
                auto_scores[match['match_number']-1] = match['score_breakdown'][alliance]['autoPoints']

        gear_matrix.append(gear_coloumn)
        auto_matrix.append(auto_coloumn)
        fuel_matrix.append(fuel_coloumn)

    gear_scores = np.array([gear_scores]).transpose()
    gear_matrix = np.array(gear_matrix).transpose()
    gears = linalg.lstsq(gear_matrix,gear_scores)[0]

    auto_scores = np.array([auto_scores]).transpose()
    auto_matrix = np.array(auto_matrix).transpose()
    auto = linalg.lstsq(auto_matrix,auto_scores)[0]

    fuel_scores = np.array([fuel_scores]).transpose()
    fuel_matrix = np.array(fuel_matrix).transpose()
    fuel = linalg.lstsq(fuel_matrix,fuel_scores)[0]

    opr_teams = np.array([opr_teams]).transpose()

    print(opr_teams.shape)
    print(fuel.shape)
    print(auto.shape)
    print(gears.shape)

    data = np.hstack((fuel,np.hstack((auto,np.hstack((gears,opr_teams))))))
    var = data - np.ones((54,54)).dot(data)
    print(var.transpose().dot(var))

def getOPRS(reg_key):
    # gathering data
    team_groups = get_event_teams(reg_key)
    opr_unsorted = tba.event_stats(reg_key)["oprs"]
    opr_teams = []
    for team in team_groups:
        opr_teams.append(opr_unsorted[team[3:len(team)]])
    opr_teams = np.array([opr_teams]).transpose()
    return opr_teams


def getCCWMS(reg_key):
    # gathering data
    team_groups = get_event_teams(reg_key)
    ccwms_unsorted = tba.event_stats(reg_key)["ccwms"]
    ccwms_teams = []
    for team in team_groups:
        ccwms_teams.append(ccwms_unsorted[team[3:len(team)]])
    ccwms_teams = np.array([ccwms_teams]).transpose()
    return ccwms_teams

def getStat(reg_key,stat):
    team_groups = get_event_teams(reg_key)
    event_matches = tba.event_matches(reg_key)
    match_num = 0
    for e_match in event_matches:
        if e_match['comp_level'] == 'qm':
            match_num = match_num + 1

    stat_matrix = []
    stat_scores = [0] * match_num

    for team in team_groups:
        matches = tba.team_matches(team,reg_key)
        stat_col = [0] * match_num
        for match in matches:
            if match['comp_level'] == 'qm':
                alliance = 'blue'

                for member in match['alliances']['red']['teams']:
                    if team == member:
                        alliance = 'red'

                stat_col[match['match_number']-1] = 1
                stat_scores[match['match_number']-1] = match['score_breakdown'][alliance][stat]
        stat_matrix.append(stat_col)

    stat_scores = np.array([stat_scores]).transpose()
    stat_matrix = np.array(stat_matrix).transpose()
    stats = linalg.lstsq(stat_matrix,stat_scores)[0]
    return stats

def main():
    print(getOPRS("2017mnmi2"))
# To call main function
if '__main__' == __name__: main()
