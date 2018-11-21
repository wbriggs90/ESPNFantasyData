# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 19:50:01 2018

@author: old pc
"""
import sys
sys.path.append('..')

import fftool



leagueId=607464

year = 2018

swid = '{A221949C-F68F-47C1-A194-9CF68FA7C10B}'
espn_s2 = 'AECWqA71p5AKpPmhkQe76i4EZLwD2nwNm8paXEgNInL3K7FrMD7PskJQf75eJFVjrakubruCWsrtAsTsLABeqrPS96eieS83l%2FfBg%2FzWbjlIDF1lPP4l6DoxHQHKsVlzT2XSYNmliypZ5njicexpaY%2FZzOmk5ltnD7Lh3u0ZiJx2B%2BSCxOSPOUWPi%2F%2BgxC7V35z4iL7hIC6LR6GubrzTDK0ahq%2BdMzw%2BQAFKX6JTrKXTASVBy3W8CNgflAv4Io6O8Q1uKNtSLumt66fmAZuyfxKf'

league = fftool.privateLeague(leagueId,espn_s2,swid)
league.setYear(2018)

week = 4
print(league.myRankings())





