#!/usr/bin/python3
# -*- encoding: utf8 -*-

'''
Created on Mar 28, 2017

@author: Jack Rausch
'''
import json
import tbapy
import numpy as np
import numpy.linalg as linalg

#the key which allows this to work, currently my(Ransom's) account
AUTH_KEY = 'Y7oKuR74PS2Nk2Z3eHfMGcLCoQBHYbHdOX3DncU7Pw2HhEnjA0VaR0PyJyUNmFFd'
tba = tbapy.TBA(AUTH_KEY)
simple = True

def get_event_teams(event_key):
    jsonified = tba.event_teams(event_key,simple,simple)
    return jsonified

"""
Supplies the least sqaures solution
to the probelm of assigning each team
a stat when they are collected per alliance
"""
def getStat(reg_key,stat):
    team_groups = get_event_teams(reg_key)
    event_matches = tba.event_matches(reg_key)
    # find the number of qualifying matches
    match_num = 0
    for e_match in event_matches:
        if e_match['comp_level'] == 'qm':
            match_num = match_num + 1

    #Set up the problem to be solved as finding a for stat_matrix*a = stat_scores
    stat_matrix = []
    stat_scores = [0] * match_num

    for team in team_groups:
        matches = tba.team_matches(team,reg_key)
        stat_col = [0] * match_num
        #filling out stat_matrix by going through each match for each team
        for match in matches:
            if match['comp_level'] == 'qm':
                alliance = 'blue'

                for member in match['alliances']['red']['team_keys']:
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
    print(getStat("2017mnmi2","totalPoints"))
# To call main function
if '__main__' == __name__: main()
