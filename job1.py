# -*- coding: utf-8 -*-
from urllib import urlopen
import re
import csv

tbody_re=re.compile(r'<tbody>(.*)</tbody>',re.S)
trs_re=re.compile(r'<tr .*?>(.*?)</tr>',re.S)
tds_re=re.compile(r'<td .*?>(.*?)</td>',re.S)
date_re=re.compile(r'date=(.*?)&')
usrurl_re=re.compile(r'href="(.*?)"')
usename_re=re.compile(r'>(.*)<')
playstr_re=re.compile(r'\bJoey Votto\b(.*?)\bout\b',re.S)
lorR_re=re.compile(r'<strong>Bats/Throws:</strong>(.*?)<br',re.S)






#get messages from a url and a re pattern
def _getmessages(url,pattern):
    doc = urlopen(url).read()
    return pattern.findall(doc)


#1.get all teams
def _getAllTeams():
    ALL_TEAM_URL='http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2013&month=0&season1=2013&ind=0&team=0,ts&players=0'
    teamname_re=re.compile(r'<a href="(leaders.aspx\?pos=all.*?)">(.*?)</a>',re.S)
    return _getmessages(ALL_TEAM_URL,teamname_re)[20:]



#2.get all pays for a team
def _getAllPlays(teamurl):
    play_re=re.compile(r'<a href="(statss.aspx\?playerid=.*?">(.*?)</a>')
    return _getmessages(teamurl,play_re) 

#3.get all game log messags for a player
def _getBattingMessage(playerurl,playername):
    allmess={}
    types=('1','2','3','4','5','6','7','8','12','13','14','15')
    typesbegin={'1':6, }
    typesend={'13':2, }
    tr_re=re.compile(r'<tr class="rg.*?Row" id="DailyStats.*?>.*?</tr>',re.S)
    td_re=re.compile(r'<td class="grid_line_.*?>(.*?)</td>',re.S)
    date_re=re.compile(r'<a.*?>(.*?)</a>')
    for x in types:
        url=playerurl+'&type='+x+'&gds=&gde=&season=2012' 
        messages=_getmessages(url,tr_re)
        for message in messages:
            tds=td_re.findall(message)
            date=_convertdate(date_re.search(tds[0]).group(1))
            allmess[date]=allmess.get(date,[playername,date,tds[1],tds[2]])
            allmess[date].extend(tds[typesbegin.get(x,5):len(tds)-typesend.get(x,0)])  


    return allmess





#4. get all play log messages for a player
def _getPlaylogMessage(playerurl,playername):

    pass

#5.get 
def _convertdate(datestr):
    date2=datestr.split('-')
    return ''.join((date2[1],date2[2],date2[0]))

def _convertname(name):
    name1=name.split()
    return '.'+name1[1],name1[0]

def _getLorR(useurl):
    doc = urlopen(useurl).read()
    s1=lorR_re.search(doc).group(1)
    return s1.split()[0][-1]




def getmessage(domain,url,filename):
    r'''
    domain: the http domain like http://www.fangraphs.com/, the last / is required
    url: the current url to parse
    filename: the csv file name for save
    '''


    #1.get the page content
    doc = urlopen(url).read()
    #2.get content from <tbody>
    tbody=tbody_re.search(doc).group(1)
    #3 get trs
    trs=trs_re.findall(tbody)
    #4 all the messages
    messages=[]
    #4 iter tr
    for tr in trs:

        tds=tds_re.findall(tr)
        datestr=_convertdate( date_re.search(tds[0]).group(1) )

        useurl=usrurl_re.search(tds[1]).group(1)
        isLorR=_getLorR(domain+useurl)

        usrname=_convertname(usename_re.search(tds[1]).group(1))

        m=playstr_re.search(tds[6])
        if m is None:
            playstr='not out'
        else:
            playstr=m.group(1)
        
        messages.append((datestr,usrname[0],usrname[1],isLorR,playstr))

    with open(filename,'w') as fn:
        writer=csv.writer(fn)
        writer.writerows(messages)




if __name__ == '__main__':
    getmessage('http://www.fangraphs.com/','http://www.fangraphs.com/statsp.aspx?playerid=4314&position=1B&season=2013','data5.csv')



