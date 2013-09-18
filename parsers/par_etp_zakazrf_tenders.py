import urllib.request
from bs4 import BeautifulSoup
from utils import normalUtf
from datetime import datetime

baseurl = "etp.zakazrf.ru/"

def inf_from_table(table:'BeautifulSoup',f:'_io.TextIOWrapper'):
    rows=table.find_all('tr',class_='RowsTable_Default')
    rows2=table.find_all('tr',class_='RowsTable_Default_')
    rows=rows+rows2
    for row in rows:
        str=''
        row_data=row.find_all('td')
        #<notice_number>
        str=str+row_data[1].get_text()+';'
        #</notice_number>
        #<subject>
        str=str+row_data[2].get_text()+';'
        #</subject>
        #<price>
        str=str+row_data[3].get_text()+';'
        #</price>
        #<organizer>
        str=str+row_data[4].get_text()+';'
        #</organizer>
        #<publication_date_time>
        str=str+row_data[5].get_text()+';'
        #</publication_date_time>
        #<start_date>
        str=str+row_data[6].get_text()+';'
        #</start_date>
        #<start_time>
        str=str+row_data[7].get_text()+';'
        #</start_time>
        #<state>
        str=str+row_data[8].get_text()+';'
        #</state>
        #<url>
        link = row_data[0].find('a');
        if not (link is None):
            #print(link['href'])
            str=str+link['href'].replace('\n', '')+';'
        #</url>
        str=normalUtf(str)
        f.write(str)
        f.flush()
        
        #begin full info about zakaz
        get_sub_content(link['href'], f)
        #end full info about zakaz
        return link['href']

def get_content(url):
    req=urllib.request.Request(url)
    req.add_header('Host','etp.zakazrf.ru')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0')
    req.add_header('Accept','ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3')
    #req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Connection','keep-alive')
    #req.add_header('Connection','close')
    req.add_header('X-MicrosoftAjax','Delta=true')
    req.add_header('Cache-Control','no-cache, no-cache')
    req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('Referer','http://etp.zakazrf.ru/Reductions.aspx?stage=2')
    req.add_header('Cookie','CurrentLanguageCode=')
    req.add_header('Pragma','no-cache')
    
    step = 10
    while step > 0:
        try:
            content = urllib.request.urlopen(req)
        except:
            print(step)
            step -= 1
        else:
            step = 0
    return (req, content)


def get_sub_content(link, f:'_io.TextIOWrapper'):
    #print("http://"+baseurl[0:-1]+link)
    (req, ans) = get_content("http://"+baseurl+link)
    soup=BeautifulSoup(ans,from_encoding="utf-8")
    content = soup.find(class_='CardView')
    content = content.find_all('table')
    result = ''
    for table in content[0:2]:
        for td in table.find_all('td')[1::2]:
            result+=td.get_text()+';'
    result += content[2].find_all('td')[4].get_text()+';'
    result = result.replace('\t',  '').replace('\n',  '').replace('\x0D',  '')
    result = normalUtf(result)
    f.write(result+'\n')
    f.flush()

(req, ans) = get_content("http://"+baseurl+"Reductions.aspx?stage=2")
soup=BeautifulSoup(ans,from_encoding="utf-8")
elem=soup.find("input",id="__EVENTARGUMENT")
event_arg=elem.get('value')
elem=soup.find("input",id="__VIEWSTATE")
viewst=elem.get('value')
elem=soup.find("input",id="__EVENTVALIDATION")
eventval=elem.get('value')

def determine_viewstate(s):
    pos=s.find('__VIEWSTATE|')
    if pos==(-1):
        return ''
    res=''
    i=pos+12
    while s[i] != '|':
        res=res+s[i]
        i=i+1
    return res

def determine_eventvalidation(s):
    pos=s.find('__EVENTVALIDATION|')
    if pos==(-1):
        return ''
    res=''
    i=pos+18
    while s[i] != '|':
        res=res+s[i]
        i=i+1
    return res

wr_to_f=open("./"+ baseurl + str(datetime.now()) + "_etp_zakazrf_auctions.txt","w")

row_in_page = 10

rec=soup.find('span',id='ctl00_Content_RecordsCountLabel')
number_of_records=int(rec.get_text())
cur_iter=1
iter_size=number_of_records/row_in_page
while cur_iter <= iter_size:
    print(str(cur_iter) + '<=' + str(iter_size))
    tbl=soup.find('table',class_="reporttable")
    inf_from_table(tbl,wr_to_f)
    page_num=2
    while page_num <= row_in_page:
        data=urllib.parse.urlencode({'ctl00$Content$ScriptManager':'ctl00$Content$UpdatePanel|ctl00$Content$Pager$Page'+('%d' % page_num)+'Button',\
        '__EVENTTARGET':'ctl00$Content$Pager$Page'+('%d' % page_num)+'Button','__EVENTARGUMENT':event_arg,\
        '__VIEWSTATE':viewst,'__EVENTVALIDATION':eventval})
        data = data.encode('utf-8')
        req.add_header('Content-Length',('%d' % len(data)))
        ans=urllib.request.urlopen(req,data)
        soup=BeautifulSoup(ans,from_encoding="utf-8")
        buf_str=soup.get_text()
        buf_str2=determine_viewstate(buf_str)
        if buf_str2 != '':
            viewst=buf_str2
        else:
            continue
        buf_str2=determine_eventvalidation(buf_str)
        if buf_str2 != '':
            eventval=buf_str2
        else:
            continue
        tbl=soup.find('table',class_="reporttable")
        link = inf_from_table(tbl,wr_to_f)
        page_num=page_num+1
    data=urllib.parse.urlencode({'ctl00$Content$ScriptManager':'ctl00$Content$UpdatePanel|ctl00$Content$Pager$NextPageButton',\
    '__EVENTTARGET':'ctl00$Content$Pager$NextPageButton','__EVENTARGUMENT':event_arg,\
    '__VIEWSTATE':viewst,'__EVENTVALIDATION':eventval})
    data = data.encode('utf-8')
    req.add_header('Content-Length',('%d' % len(data)))
    ans=urllib.request.urlopen(req,data)
    con_sz=ans.headers.get('Content-Length')
    soup=BeautifulSoup(ans,from_encoding="utf-8")
    buf_str=soup.get_text()
    buf_str2=determine_viewstate(buf_str)
    if buf_str2 != '':
        viewst=buf_str2
    else:
        continue
    buf_str2=determine_eventvalidation(buf_str)
    if buf_str2 != '':
        eventval=buf_str2
    else:
        continue
    cur_iter=cur_iter+1


if iter_size == 0:
    wr_to_f.close()
    req.add_header('Connection','close')
    req.add_header('Content-Length','0')
    urllib.request.urlopen(req)
    exit()

residue=number_of_records % row_in_page
#iter_size=(residue/row_in_page) + 1
iter_size = residue
tbl=soup.find('table',class_="reporttable")
inf_from_table(tbl,wr_to_f)
page_num=2
while page_num <= iter_size:
    data=urllib.parse.urlencode({'ctl00$Content$ScriptManager':'ctl00$Content$UpdatePanel|ctl00$Content$Pager$Page'+('%d' % page_num)+'Button',\
    '__EVENTTARGET':'ctl00$Content$Pager$Page'+('%d' % page_num)+'Button','__EVENTARGUMENT':event_arg,\
    '__VIEWSTATE':viewst,'__EVENTVALIDATION':eventval})
    data = data.encode('utf-8')
    req.add_header('Content-Length',('%d' % len(data)))
    ans=urllib.request.urlopen(req,data)
    soup=BeautifulSoup(ans,from_encoding="utf-8")
    buf_str=soup.get_text()
    buf_str2=determine_viewstate(buf_str)
    if buf_str2 != '':
        viewst=buf_str2
    else:
        continue
    buf_str2=determine_eventvalidation(buf_str)
    if buf_str2 != '':
        eventval=buf_str2
    else:
        continue
    tbl=soup.find('table',class_="reporttable")
    link = inf_from_table(tbl,wr_to_f)
    page_num=page_num+1
req.add_header('Connection','close')
req.add_header('Content-Length','0')
urllib.request.urlopen(req)
wr_to_f.close()
