# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 10:01:09 2018

@author: old pc
endpoints:
    
leagueSettings
playerInfo x
scoreboard
player/news X
recentActivity
leagueSchedules
teams x
rosterInfo x
schedule
polls
messageboard
status
teams/pendingMoveBatches X
tweets
stories
livescoring
boxscore x

"""
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd


 

class privateLeague():
    '''create an instance of a league for the current year.
    
    to change year use the setyear function'''
    
    slotvalues = {20:"BENCH", 0:'QB', 2:'RB', 4:'WR', 6:'TE', 23:'FLEX', 16:'DEF', 17:'KICKER'}
    teams = {}
      
    def __init__(self, league_id, espn_s2, swid):
        self.league_id = league_id
        self.year = datetime.datetime.now().year # should change this from calendar year to be within the typical season timeframe
        self.apipath = "http://games.espn.com/ffl/api/v2/"
        self.espn_s2 = espn_s2
        self.swid = swid
        self.parameters = {'leagueId': self.league_id, 'seasonId': self.year}
        self.cookies =  {'espn_s2': self.espn_s2, 'SWID': self.swid}
        self.scoreboard = [None] * 16
        self.rosters = {}
        self.teams = {}

    def getTeams(self,week):
        for matchup in self.getScoreboardData(week)[week]['scoreboard']['matchups']:
            teamId = matchup['teams'][0]['teamId']
            BS = self.getTeamBoxScoreData(week,teamId)
            for team in BS['boxscore']['teams']:
                print(team['team']['teamAbbrev'])
                teamAbbrev = team['team']['teamAbbrev']
                teamId = team['team']['teamId']
                teamName = team['team']['teamNickname']
                self.teams[teamAbbrev] = teams.team(teamName,teamId,teamAbbrev)
                for player in team['slots']:
                    firstname = player['player']['firstName']
                    lastname = player['player']['lastName']
                    self.teams[teamAbbrev].roster.append(firstname+' '+lastname)
        return
        

            
        
    def setYear(self, year):
        '''The reason this is a method is for future implementation of fault checking
        
        example being if the league did not exist for the year trying to be set.
        
        another example would be to clear all data within object that does not
        apply, possibly with a clean init'''
        self.year = year
        
    def getPlayerNewsData(self, week):
        '''get the player/news endpoint data
        this is empty when it comes from ESPN'''
        
        data = requests.get(self.apipath + 'player/news',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        data = data.json()
        
        return data
    

    

    def getScoreboardData(self, week):
        '''get the scoreboard endpoint data
        this is empty when it comes from ESPN'''
        
        scoreboard = requests.get(self.apipath + 'scoreboard',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        self.scoreboard[week] = scoreboard.json()
        
        return self.scoreboard





    def getBoxScoreData(self, week):
        '''get the boxscore endpoint data
        
        boxscore provides scoring stats for the week
        
        in private leagues this is the score associated 
        with the login for the instantiated ESPN Cookies'''
        
        boxscore = requests.get(self.apipath + 'boxscore',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        self.boxscore = boxscore.json()
        
        return self.boxscore

    def getTeamBoxScoreData(self, week, teamId):
        '''get the boxscore endpoint data for a specific team. 
        this will return roster information as well
        
        boxscore provides scoring stats for the week
        
        '''
        
        boxscore = requests.get(self.apipath + 'boxscore',
                            params={'leagueId': self.league_id,
                                    'matchupPeriodId': week,
                                    'seasonId': self.year,
                                    'teamId': teamId }, 
                            cookies=self.cookies)
        
        self.boxscore = boxscore.json()
        
        return self.boxscore
        
    
    def getPlayerInfoData(self, week):
        '''get the playerInfo endpoint data'''
        
        data = requests.get(self.apipath + 'playerInfo',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        data = data.json()
        
        return data
    
    def getTeamsData(self,week):
        '''get the teams endpoint data'''
        
        self.teams = requests.get(self.apipath + 'teams',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        self.teams = self.teams.json()
        
        return self.teams
    
    def printAllRosters(self, week):
       for matchup in self.getScoreboardData(week)[week]['scoreboard']['matchups']:
            teamId = matchup['teams'][0]['teamId']
            BS = self.getTeamBoxScoreData(week,teamId)
            for team in BS['boxscore']['teams']:
                print(team['team']['teamAbbrev'])
                for player in team['slots']:
                    print(player['player']['firstName'],
                          ' ',
                          player['player']['lastName'],
                          self.slotvalues[player['slotCategoryId']])
                

    def printMyRoster(self,week):
        for team in self.getRosterInfo(1)['leagueRosters']['teams']:
            print(team['team']['teamAbbrev'])
            for player in team['slots']:
                print('%s %s %s' %(player['player']['firstName'],
                                   player['player']['lastName'],
                                   self.slotvalues[player['slotCategoryId']]))


    def getRosterInfoData(self, week):
        ''' get the rosterInfo endpoint data'''
        
        data = requests.get(self.apipath + 'rosterInfo',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        data = data.json()
        
        return data 
    
    def getTeamRosterInfoData(self, week, teamId):
        ''' get the rosterInfo endpoint data'''
        
        data = requests.get(self.apipath + 'rosterInfo',
                            params={'leagueId': self.league_id,
                                    'matchupPeriodId': week,
                                    'seasonId': self.year,
                                    'teamId': teamId },  
                            cookies=self.cookies)
        
        data = data.json()
        
        return data

    def getPendingMoveBatches(self, week):
        '''get the teams/pendingMoveBatches endpoint data'''
        
        data = requests.get(self.apipath + 'teams/pendingMoveBatches',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        data = data.json()
        
        return data
    
    def getFreeAgent(self,slot):
        ''' gets the current available free agents for given slot id
        includes players on waivers'''
        freeagents = requests.get('http://games.espn.com/ffl/freeagency',
                     params={'leagueId': self.league_id, 
                             'seasonId': self.year,
                             'slotCategoryId': slot,
                             'avail': 1},
                     cookies={'SWID': self.swid, 'espn_s2': self.espn_s2})
        soup = BeautifulSoup(freeagents.content, 'html.parser')
        data = soup.find('table', class_='playerTableTable')
        freeagents = pd.read_html(str(data), header=0, skiprows=1, flavor='bs4' )[0]
        return freeagents
    
    def getFreeAgentQB(self):
        ''' gets the current available free agent QB's'''
        freeagents = self.getFreeAgent(0)
        return freeagents

    def getFreeAgentWR(self):
        ''' gets the current available free agent WR's'''
        freeagents = self.getFreeAgent(4)
        return freeagents
        
    def getFreeAgentRB(self):
        ''' gets the current available free agent RB's'''
        freeagents = self.getFreeAgent(2)
        return freeagents
    
    def getFreeAgentFlex(self):
        ''' gets the current available free agent Flex's'''
        freeagents = self.getFreeAgent(23)
        return freeagents

    def getFreeAgentDef(self):
        '''gets the current available free agent Defenses'''
        freeagents = self.getFreeAgent(16)
        return freeagents
    
    def getFreeAgentKicker(self):
        ''' gets the current available free agent RB's'''
        freeagents = self.getFreeAgent(17)
        return freeagents
    
    def getRankings(self, slot=None, avail=2):
        '''
        this function is a mess
        avail:
            2 = free agent
            
            1 = available
            
            -1 = all
        '''
        rankings = requests.get('http://games.espn.com/ffl/freeagency',
                     params={'leagueId': self.league_id, 
                             'seasonId': self.year,
                             'slotCategoryId': slot,
                             'view': 'ranks',
                             'avail': avail},
                     cookies={'SWID': self.swid, 'espn_s2': self.espn_s2})
        soup = BeautifulSoup(rankings.content, 'html.parser')
        data = soup.find('table', class_='playerTableTable')
        rankings = pd.read_html(str(data), header=0, skiprows=1, flavor='bs4' )[0]
        
        rankings[['Player' ,'team position']] = rankings['PLAYER, TEAM POS'].str.split(', ', n=1, expand=True)
        rankings['team position'].fillna('Defense',inplace=True)
        rankings[['Team','position status']] = rankings['team position'].str.split('\s+', n=1, expand=True)
        try:
            rankings[['Position','Position 2']] = rankings['position status'].str.split(', ', n=1, expand=True)
            rankings[['Position 2','Status']] = rankings['Position 2'].str.split('\s+', n=1, expand=True)
            rankings[['Position','status 2']] = rankings['Position'].str.split('\s+', n=1, expand=True)
            rankings['Status'].fillna(rankings['status 2'],inplace=True)
        except:
            rankings[['Position','Status']] = rankings['position status'].str.split('\s+', n=1, expand=True)
        try:
            rankings.drop(['PLAYER, TEAM POS','Unnamed: 1','ACTION','OPP',
                       'STATUS ET','Unnamed: 7','Unnamed: 4',
                       'team position','position status','status 2'], axis=1,inplace=True)
        except:
            rankings.drop(['Unnamed: 1','ACTION','OPP',
                       'STATUS ET','Unnamed: 7','Unnamed: 4',
                       'team position','position status'], axis=1,inplace=True)
        rankings = rankings[rankings['Status']!='IR']    
        rankings.replace('--', '51', inplace=True)
        
        cols = ['KARABELL','YATES','COCKCROFT','CLAY','BELL']

        rankings[cols] = rankings[cols].apply(pd.to_numeric, errors='coerce')
        rankings['AVERAGE'] = rankings[cols].mean(axis=1)
        rankings.sort_values('AVERAGE',ascending=True,inplace=True)
        
        
        return rankings