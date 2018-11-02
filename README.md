# ESPNFantasydata
Tool for:
1. getting data from ESPN Fantasy Football leagues
	a. data includes rankings, player info/availability, scoring, etc.
2. running analysis to make educated roster moves on many different statistics/rankings


ESPNFantasyData gets data from two locations:
1. scraping data from ESPN fantasy player pages
2. ESPN Fantasy API


Here is how to find the top 5 ranked running backs available in your league and their rankings

```python
from fftool import fftool

# bogus credentials below
leagueId=123456
year = 2018
swid = '{A221C49C-F69F-43C1-A294-9CF68FF7C10B}'
espn_s2 = 'AECWqA71p5AKpPmhkQe76i4EZLwD2nwNm8paXEgNInL3K7FrMD7PskJQf75eJFVjrakubruCWsrtAsTsLABeqrPS96eieS83l%2FfBg%2FzWbjlIDF1lPP4l6DoxHQHKsVlzT2XSYNmliypZ5njicexpaY%2FZzOmk5ltnD7Lh3u0ZiJx2B%2BSCxOSPOUWPi%2F%2BgxC7V35z4iL7hIC6LR6GubrzTDK0ahq%2BdMzw%2BQAFKX6JTrKXTASVBy3W8CNgflAv4Io6O8Q1uKNtSLumt66fmAZuyfxKf'


league = fftool.privateLeague(leagueId,espn_s2,swid)

rankings = league.getRankings(avail=1,slot=2)
print(rankings.head())

```

the output is:

```
   TYPE BERRY  KARABELL  YATES  COCKCROFT  CLAY  BELL  AVERAGE  \
12   FA    22        20     26         22    23    25     23.2   
1    FA    26        22     27         27    26    24     25.2   
6    FA    27        30     23         36    27    27     28.6   
2    FA    34        33     31         38    33    32     33.4   
5    FA    31        35     29         33    32    40     33.8   

            Player Team Position Position 2 Status  
12     Aaron Jones   GB       RB       None   None  
1     Alex Collins  Bal       RB       None      Q  
6    Peyton Barber   TB       RB       None   None  
2   Javorius Allen  Bal       RB       None   None  
5       Frank Gore  Mia       RB       None   None 
```



