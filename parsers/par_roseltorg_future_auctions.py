import urllib.request
from bs4 import BeautifulSoup
from utils import normalUtf
from datetime import datetime

#определение количества страниц
baseurl = "etp.roseltorg.ru/"

def subInfo(a_url):
    v_url = "http://"+baseurl[0:-1]+a_url
    v_soup = BeautifulSoup(urllib.request.urlopen(v_url),from_encoding="utf-8")
    v_info = v_soup.find_all(class_ = "data-right")
    v_result = ''
    for v_line in v_info:
        v_data = v_line.find('p')
        if not (v_data is None):
            v_result += v_data.get_text() + ';'
    v_result = v_result.replace('<img src="/theme/images/data-add.gif" alt="" width="14" height="14" />  <a href="#" class="data-add">Добавить дату в календарь</a>', '')
    return v_result

URL="http://" + baseurl + "trade/future/?page=1&limit=100&order=pubdate&dir=desc#table"
soup=BeautifulSoup(urllib.request.urlopen(URL),from_encoding="utf-8")
link_pg=soup.find_all(class_="link_page")
links=link_pg[0].find_all("a")
final_page_link=links[len(links)-1]
fp_str=final_page_link['href']
pos=fp_str.find("page=")
pos=pos+5
i=pos
_str=''
while fp_str[i]!='&':
        _str=_str+fp_str[i]
        i=i+1;
num_of_pages=int(_str)



#получение и запись данных

inf_file=open("./" + baseurl + str(datetime.now()) +"_roseltorg_future_auctions.txt","w")
cur_page=1
while cur_page <= num_of_pages:
        print(str(cur_page) + '<=' + str(num_of_pages))
        if cur_page > 1:
                URL="http://" + baseurl + "trade/future/?page="+('%d' % cur_page)+"&limit=100&order=pubdate&dir=desc#table"
                soup=BeautifulSoup(urllib.request.urlopen(URL),from_encoding="utf-8")
        main_table=soup.find("table",class_="tbl_org tbl_org_zakon tbl_org_regedit tbl_torgs ")
        lines=main_table.find_all("tr")
        g=1
        num_ln=len(lines)
        while g < num_ln:
                _str='';
                cur_line=lines[g]
                data_in_line=cur_line.find_all("td")

                #begin get information about competition
                link = data_in_line[1].find('a')['href']
                _str+=subInfo(link)
                #end get information about competition


                #<customer>
                links_in_line=data_in_line[0].find_all('a')
                _str=_str+links_in_line[1].get_text()+';'
                #</customer>
                #<subject>
                _str=_str+data_in_line[1].get_text()+';'
                #</subject>
                #<date>
                _str=_str+data_in_line[2].get_text()+';'
                #</date>
                #<type>
                tp_pic=data_in_line[3].find_all('img')
                k=0
                for elem in tp_pic:
                        _str=_str+tp_pic[k].get('title')+'.'
                        k=k+1
                #</type>
                _str=_str+';'
                #<region_number>
                _str=_str+data_in_line[3].get_text()+';'
                #</region_number>
                sp_req=data_in_line[4].get_text()
                if len(sp_req) > 0:
                        pos=len(sp_req)-3
                        if sp_req[pos] == '%':
                                req='%'
                                pos=pos-1
                                while ((sp_req[pos]<='9' and sp_req[pos]>='0') or (sp_req[pos]=='.')) and pos > -1:
                                        req=sp_req[pos]+req
                                        pos=pos-1
                                if pos != -1:
                                        #<start_price>
                                        r=0
                                        while sp_req[r]!='.' and r < pos:
                                                _str=_str+sp_req[r]
                                                r=r+1
                                        #</start_price>
                                        _str=_str+'.;'
                                #<requirement>
                                _str=_str+req
                                _str=_str+';'
                                #</requirement>
                        else:
                                #<start_price>
                                r=0
                                sp_len=len(sp_req)
                                while sp_req[r]!='.' and r <= sp_len-3:
                                        _str=_str+sp_req[r]
                                        r=r+1
                                #</start_price>
                                _str=_str+';'
                g=g+1
                _str=normalUtf(_str)
                inf_file.write(_str)
                inf_file.write("\n")
        inf_file.flush()
        cur_page=cur_page+1
inf_file.close()
