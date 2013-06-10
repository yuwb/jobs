from urllib import urlopen
import re
import csv

#111234234
tbody_re=re.compile(r'<tbody>(.*)</tbody>',re.S)
trs_re=re.compile(r'<tr .*?>(.*?)</tr>',re.S)
tds_re=re.compile(r'<td .*?>(.*?)</td>',re.S)
date_re=re.compile(r'date=(.*?)&')
usrurl_re=re.compile(r'href="(.*?)"')
usename_re=re.compile(r'>(.*)<')
playstr_re=re.compile(r'\bJoey Votto\b(.*?)\bout\b',re.S)
lorR_re=re.compile(r'<strong>Bats/Throws:</strong>(.*?)<br',re.S)



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



