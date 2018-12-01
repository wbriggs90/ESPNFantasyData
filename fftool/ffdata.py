# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 10:01:09 2018

@author: Will Briggs


"""
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from fftool import teams as tm

 

class privateLeague():
    '''create an instance of a league for the current year.
    
    to change year use the setyear function'''
    
    slotnames = {20:"BENCH", 0:'QB', 2:'RB', 4:'WR', 6:'TE', 23:'FLEX', 16:'DEF', 17:'KICKER'}
    slotvalues = {}
    for slotid in slotnames:
        slotvalues[slotnames[slotid]]=slotid
        
    
    #teams = {}
      
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
        self.rosterFormat = {}
        self.leaguesettings = None
        self.boxscore = None

    #%% SET VALUES
    def setYear(self, year):
        '''The reason this is a method is for future implementation of fault checking
        
        example being if the league did not exist for the year trying to be set.
        
        another example would be to clear all data within object that does not
        apply, possibly with a clean init'''
        self.year = year
        
    #%% GET DATA
    def getTeams(self,week):
        for matchup in self.getScoreboardData(week)[week]['scoreboard']['matchups']:
            teamId = matchup['teams'][0]['teamId']
            BS = self.getTeamBoxScoreData(week,teamId)
            for team in BS['boxscore']['teams']:
                print(team['team']['teamAbbrev'])
                teamAbbrev = team['team']['teamAbbrev']
                teamId = team['team']['teamId']
                teamName = team['team']['teamNickname']
                self.teams[teamAbbrev] = tm.team(teamName,teamId,teamAbbrev)
                for player in team['slots']:
                    firstname = player['player']['firstName']
                    lastname = player['player']['lastName']
                    self.teams[teamAbbrev].roster.append(firstname+' '+lastname)
        return
    
    def getPlayerNewsData(self, week):
        '''get the player/news endpoint data
        this is empty when it comes from ESPN'''
        
        data = requests.get(self.apipath + 'player/news',
                            params=self.parameters, 
                            cookies=self.cookies)        
        return data.json()
    
    def getScoreboardData(self, week):
        '''get the scoreboard endpoint data'''
        
        scoreboard = requests.get(self.apipath + 'scoreboard',
                            params=self.parameters, 
                            cookies=self.cookies)
        
        self.scoreboard[week] = scoreboard.json()
        
        return self.scoreboard

    def getLeagueSettingsData(self, week):
        '''get the scoreboard endpoint data'''
        
        leaguesettings = requests.get(self.apipath + 'leagueSettings',
                            params=self.parameters, 
                            cookies=self.cookies)
        self.leaguesettings = leaguesettings.json() 
        return self.leaguesettings

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
    
    #%% FREE AGENT STUFF
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
        return self.getFreeAgent(0)

    def getFreeAgentWR(self):
        ''' gets the current available free agent WR's'''
        return self.getFreeAgent(4)
        
    def getFreeAgentRB(self):
        ''' gets the current available free agent RB's'''
        return self.getFreeAgent(2)
    
    def getFreeAgentFlex(self):
        ''' gets the current available free agent Flex's'''
        return self.getFreeAgent(23)

    def getFreeAgentDef(self):
        '''gets the current available free agent Defenses'''
        return self.getFreeAgent(16)
    
    def getFreeAgentKicker(self):
        ''' gets the current available free agent RB's'''
        return self.getFreeAgent(17)
    #%%  RANKINGS
    def getRankings(self, slot=None, avail=1, pages=1):
        '''
        this function is a mess
        avail:
            2 = free agent
            1 = available
            -1 = all
        
        pages must be an integer value between 1 and 8
        maximum of 8 pages which will return 400 players
        
        '''
        startIndex = 0
        
        pages = int(pages)
        if pages>8:
            pages = 8
        if pages<1:
            pages = 1
            
        for i in range(pages):
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
            '''
            the below lines attempt to split up the player team pos column which contains the player team positions and status.  
            I have been unable to make this code accept all different inputs. 
            for isntance some players have multiple positions and some may not hvae a status
            
            rankings[['Player' ,'team position']] = rankings['PLAYER, TEAM POS'].str.split(', ', n=1, expand=True)
            rankings['team position'].fillna('Defense',inplace=True)
            rankings[['Team','position status']] = rankings['team position'].str.split('\s+', n=1, expand=True)
            rankings['position status'].fillna('Defense',inplace=True)
            #print(rankings)
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
            '''
            rankings.drop(['Unnamed: 1','ACTION','OPP','STATUS ET',
                           'Unnamed: 7','Unnamed: 4'], axis=1,inplace=True)
        
            rankings.replace('--', '51', inplace=True)
            
            cols = ['BERRY','KARABELL','YATES','COCKCROFT','CLAY','BELL']
    
            rankings[cols] = rankings[cols].apply(pd.to_numeric, errors='coerce')
            rankings['AVERAGE'] = rankings[cols].mean(axis=1)
            rankings.sort_values('AVERAGE',ascending=True,inplace=True)
            rankings.reset_index(drop=True,inplace=True)
            startIndex += 50 
        
        return rankings
    
    def myRankings(self):
        '''
        Returns rankings for all players on your team
        '''
        data = pd.DataFrame()
        for slotid in self.slotnames:
            slotdata = self.getRankings(slotid,avail=4)
            slotdata['slotid']= slotid
            slotdata = slotdata[slotdata['TYPE']=='BRIG']
            data = data.append(slotdata,)
        return data
    
    #%%  SCRIPTS
    def getRosterFormat(self):
        'Returns a dictionary of slot id and number of spots on the roster.  excludes bench slots'''
        data = self.getLeagueSettingsData(1)
        for slot in data['leaguesettings']['slotCategoryItems']:
            if slot['num']==0 or slot['slotCategoryId']==self.slotvalues['BENCH']:
                continue
            else:
                self.rosterFormat[slot['slotCategoryId']]=slot['num']
        print('Roster Format is:')
        for slotid in self.rosterFormat:
            print('%s %s' % (self.rosterFormat[slotid], self.slotnames[slotid]))
            
        return self.rosterFormat
    
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
                          self.slotnames[player['slotCategoryId']])
                

    def printMyRoster(self,week):
        for team in self.getRosterInfoData(1)['leagueRosters']['teams']:
            print(team['team']['teamAbbrev'])
            print(team)
            for player in team['slots']:
                print('%s %s %s' %(player['player']['firstName'],
                                   player['player']['lastName'],
                                   self.slotnames[player['slotCategoryId']]))
            
    def WWMBD(self):
        '''
        What Would Matt Berry Do?
        '''
        
        '''
        test test
        '''
        
        for slotid in self.rosterFormat:
            data = self.getRankings(slot=slotid)
            data.sort_values('BERRY',ascending=True,inplace=True)
            data.reset_index(drop=True, inplace=True)
            print(data)