# -*- coding: utf-8 -*-
from urllib import urlopen
import re
import csv

date_re=re.compile(r'date=(.*?)&')
usrurl_re=re.compile(r'href="(.*?)"')
name_re=re.compile(r'<strong style="font-size:15pt;">(.*?)</strong>')
lorR_re=re.compile(r'<strong>Bats/Throws:</strong>(.*?)<br',re.S)
Home_url='http://www.fangraphs.com/'
tr_re=re.compile(r'<tr class="rg.*?Row" id=".*?Stats.*?>(.*?)</tr>',re.S)
td_re=re.compile(r'<td class="grid_line_.*?>(.*?)</td>',re.S)

default='default'
battertypes=('1','2','3','4','5','6','7','8','12','13','14','15')
battertypesbegin={'1':6,default:5 }
battertypesdelete={'1':(9,),'13':(16,15,), } 

pitchtypes=('1','2','3','4','5','6','7','10','11','12','13','14','15','16')
pitchtypesbegin={default:4 }
pitchtypesdelete={'10':(16,) }

typesdict={'batter':battertypes,'pitch':pitchtypes }
typesbegindict={'batter':battertypesbegin,'pitch':pitchtypesbegin }
typesdeletedict={'batter':battertypesdelete,'pitch':pitchtypesdelete }

playmesses=(('double play','dp'),('singled','single'),('doubled','double'),('double','double'),('tripled','triple'),('walked','walk'),('homered','homerun'),('sacrifice','sac'),('Grounder','groundout'),('Fly','flyout'),('line out','lineout'),('struck out','strikeout'),('hit by pitch','hbp'),('caught stealing','caughtStl'),('stolen','steal'),('reached','out'),)


batterGameLogHead='Player,Date,Team,Opp,AB,PA,H,2B,3B,HR,R,RBI,BB,IBB,SO,HBP,SF,SH,GDP,SB,CS,AVG,BB%,K%,BB/K,ISO,BABIP,AVG,OBP,SLG,OPS,Spd,wSB,wRC,wRAA,wOBA,wRC+,GB/FB,LD%,GB%,FB%,IFFB%,HR/FB,IFH%,BUH%,GB,FB,LD,IFFB,IFH,BU,BUH,Balls,Strikes,Pitches,WPA,nWPA,pWPA,RE24,REW,pLI,phLI,PH,WPA/LI,Clutch,FB%,FBv,SL%,SLv,CT%,CTv,CB%,CBv,CH%,CHv,SF%,SFv,KN%,KNv,XX%,wFB,wSL,wCT,wCB,wCH,wSF,wKN,wFB/C,wSL/C,wCT/C,wCB/C,wCH/C,wSF/C,wKN/C,O-Swing%,Z-Swing%,Swing%,O-Contact%,Z-Contact%,Contact%,Zone%,F-Strike%,SwStr%,FA-X,FT-X,FC-X,FS-X,FO-X,SI-X,SL-X,CU-X,KC-X,EP-X,CH-X,SC-X,KN-X,FA-Z,FT-Z,FC-Z,FS-Z,FO-Z,SI-Z,SL-Z,CU-Z,KC-Z,EP-Z,CH-Z,wFA,wFT,wFC,wFS,wFO,wSI,wSL,wCU,wKC,wEP,wCH,wSC,wKN,wFA/C,wFT/C,wFC/C,wFS/C,wFO/C,wSI/C,wSL/C,wCU/C,wKC/C,wEP/C,wCH/C,wSC/C,wKN/C'.split(',')

batterPlayLogHead='Date,Batter,BatterLR,PitcherVsLast,PitcherVsFI,PitcherLR,Inning,Outs,RunsAhd,PlayersOB,PlayersSP,Play,Rbi,LI,RE,WE,WPA,RE24'.split(',')

pitcherGameLogHead='Player,Date,Team,Opp,GS,W,L,ERA,G,GS,CG,ShO,SV,HLD,BS,IP,TBF,H,R,ER,HR,BB,IBB,HBP,WP,BK,SO,K/9,BB/9,K/BB,HR/9,K%,BB%,AVG,WHIP,BABIP,LOB%,ERA-,FIP-,FIP,GB/FB,LD%,GB%,FB%,IFFB%,HR/FB,IFH%,BUH%,tERA,SIERA,xFIP-,xFIP,GB,FB,LD,IFFB,SO,BU,BUH,RS,Balls,Strikes,Pitches,WPA,nWPA,pWPA,RE24,REW,pLI,inLI,gmLI,exLI,Pulls,WPA/LI,Clutch,SD,MD,FB%,FBv,SL%,SLv,CT%,CTv,CB%,CBv,CH%,CHv,SF%,SFv,KN%,KNv,XX%,wFB,wSL,wCT,wCB,wCH,wSF,wKN,wFB/C,wSL/C,wCT/C,wCB/C,wCH/C,wSF/C,wKN/C,FA%,FT%,FC%,FS%,FO%,SI%,SL%,CU%,KC%,EP%,CH%,SC%,UN%,vFA,vFT,vFC,vFS,vFO,vSI,vSL,vCU,vKC,vEP,vCH,vSC,vKN,FA-X,FT-X,FC-X,FS-X,FO-X,SI-X,SL-X,CU-X,KC-X,EP-X,CH-X,SC-X,KN-X,FA-Z,FT-Z,FC-Z,FS-Z,FO-Z,SI-Z,SL-Z,CU-Z,KC-Z,EP-Z,CH-Z,SC-Z,KN-Z,wFA,wFT,wFC,wFS,wFO,wSI,wSL,wCU,wKC,wEP,wCH,wSC,wKN,wFA/C,wFT/C,wFC/C,wFS/C,wFO/C,wSI/C,wSL/C,wCU/C,wKC/C,wEP/C,wCH/C,wSC/C,wKN/C,O-Swing%,Z-Swing%,Swing%,O-Contact%,Z-Contact%,Contact%,Zone%,Pace'.split(',')

pitcherPlayLogHead='Date,Pitcher,PitcherLR,BatterVsL,BatterVsFI,BatterLR,LI,RE,WE,WPA,RE24'.split(',')

headdict={'batterGameLogHead':batterGameLogHead,'batterPlayLogHead':batterPlayLogHead,'batterPlayLogHead':batterPlayLogHead,'pitcherGameLogHead':pitcherGameLogHead }


#get messages from a url and a re pattern
def _getmessages(url,pattern):
    doc = urlopen(url).read()
    return pattern.findall(doc)

def _getfilemessages(filename,pattern):
    doc=open(filename).read()
    return pattern.findall(doc)

#1.get all teams
def _getAllTeams():
    ALL_TEAM_URL='http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2013&month=0&season1=2013&ind=0&team=0,ts&players=0'
    teamname_re=re.compile(r'<a href="(leaders.aspx\?pos=all.*?)">(.*?)</a>',re.S)
    return _getmessages(ALL_TEAM_URL,teamname_re)[20:]



#2.get all pays for a team
def _getAllPlays(teamurl,playertype):
    teamurl=Home_url+teamurl
    teamurl=teamurl.replace('bat',playertype).replace('pit',playertype)
    play_re=re.compile(r'<a href="(statss.aspx\?playerid=.*?)">(.*?)</a>')
    return _getmessages(teamurl,play_re) 

#3.get all game log messags for a player
def _getGameLogMessage(playerurl,playername,playertype):
    playerurl=playerurl.replace('statss.aspx','statsd.aspx')
    allmess={}
    types=typesdict.get(playertype)
    typesbegin=typesbegindict.get(playertype)
    typesdelete=typesdeletedict.get(playertype)


    for x in types:
        url=playerurl+'&type='+x+'&gds=&gde=&season=2013' #todo 2012 to all 
        print url
        messages=_getmessages(url,tr_re)
        #messages=_getfilemessages(playertype+'gamelog'+x+'.htm',tr_re)
        for message in messages[0:1]:
            tds=td_re.findall(message)
            tds=[n.replace('&nbsp;','') for n in tds]
            if x in typesdelete:
                deletes=typesdelete.get(x)
                for key in deletes:
                    del tds[key]
            date=_convertdate(date_re.search(tds[0]).group(1))
            start=typesbegin.get(x,typesbegin.get(default))
            if playertype=='batter':
                allmess.setdefault(date,[playername,date,tds[1],tds[2]]).extend(tds[start:])  
            elif playertype=='pitch':
                allmess.setdefault(date,[playername,date,tds[1],tds[2],tds[3]]).extend(tds[start:])  

    return allmess





#4. get all play log messages for a player
def _getPlaylogMessage(playerurl,playername,playertype):
    seasons=('2013','2012','2011',) 
    messages=[]
    
    playerurl=playerurl.replace('statss.aspx','statsp.aspx')
    for season in seasons:
        url=playerurl+'&season='+season
        doc = urlopen(url).read()
        #doc=open(playertype+'playlog'+season+'.htm').read() #todo
        lorR=_getLorR(doc,0)

        trs=tr_re.findall(doc)
        for tr in trs[0:1]:
            tds=td_re.findall(tr)
            tds=[n.replace('&nbsp;','') for n in tds]
            datestr=_convertdate( date_re.search(tds[0]).group(1))

            usr_url=usrurl_re.search(tds[1]).group(1)
            usr_url='http://www.fangraphs.com/fanpdetails.aspx'+usr_url[usr_url.find('?'):]
            #usrdoc=urlopen(usr_url).read()
            usrdoc=open('22.htm').read() #todo
            name=name_re.search(usrdoc).group(1)
            leftname,rightname=name.split()
            

            if playertype=='batter':
                pitcherlorR=_getLorR(usrdoc,-1)
                inn=tds[2].split('-')
                inning=inn[0]
                scores=map(int,tds[5].split('-'))
                if inn[1]=='T':
                    runsahd=scores[1]-scores[0]
                else:
                    runsahd=scores[0]-scores[1]

                playersob=len(filter(str.isdigit,tds[4]))
                playerssp=playersob-tds[4].count('1')

                playstr=tds[6][tds[6].find(playername)+len(playername) : tds[6].find('.',tds[6].find(playername))]
                play=' '
                for instr,rep in playmesses:
                    if playstr.find(instr)>-1:
                        play=rep
                        break
                
                if tds[6].find('double play')>-1:
                    rbi=0
                else:
                    rbi=tds[6].count('scored')+tds[6].count('homered')

                messages.append((datestr,playername,lorR,rightname,leftname,pitcherlorR,inning,tds[3],runsahd,playersob,playerssp,play,rbi,tds[7],tds[8],tds[9],tds[10],tds[11]))

            else:
                pitcherlorR=_getLorR(usrdoc,0)
                messages.append((datestr,playername,lorR,rightname,leftname,pitcherlorR,tds[7],tds[8],tds[9],tds[10],tds[11]))

    return messages

#5.get 
def _convertdate(datestr):
    date2=datestr.split('-')
    return ''.join((date2[1],date2[2],date2[0]))


def _getLorR(doc,leftOrRight):
    s1=lorR_re.search(doc).group(1)
    return s1.split()[0][leftOrRight]

def writePerPlayCsv(filename,playertype):
    #1 get all team
    allteams=_getAllTeams()
    for teamurl,teamname in allteams[0:1]:
        allplayers=_getAllPlays(teamurl,playertype[0:3])
        for playerurl,playername in allplayers[0:1]:
            messages=_getPlaylogMessage(Home_url+playerurl,playername,playertype)
   
    with open(filename,'w') as fn:
        writer=csv.writer(fn)
        writer.writerow(headdict.get(playertype+'PlayLogHead'))
        writer.writerows(messages)    
    return messages

def writePerGameCsv(filename,playertype):
    #1 get all team
    allteams=_getAllTeams()
    for teamurl,teamname in allteams[0:1]:
        allplayers=_getAllPlays(teamurl,playertype[0:3])
        for playerurl,playername in allplayers[0:1]:
            messages=_getGameLogMessage(Home_url+playerurl,playername,playertype)
   
    with open(filename,'w') as fn:
        writer=csv.writer(fn)
        writer.writerow(headdict.get(playertype+'GameLogHead'))
        writer.writerows(messages.values())    
    return messages 

def writeall():
    writePerGameCsv('BatterPerGame.csv','batter')
    writePerGameCsv('PitcherPerGame.csv','pitch')
    writePerPlayCsv('BatterVPitcher.csv','batter')
    writePerPlayCsv('PitcherVBatter.csv','pitch')

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



