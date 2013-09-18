import urllib.request
from bs4 import BeautifulSoup
from utils import normalUtf
from datetime import datetime

#определение количества страниц
baseurl = "etp.roseltorg.ru/"

URL="http://" + baseurl + "trade/past/?page=1&limit=100&order=pubdate&dir=desc#table"
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

inf_file=open("./" + baseurl + str(datetime.now()) +"_roseltorg_past_auctions.txt","w")
cur_page=1
while cur_page <= num_of_pages:
        print(str(cur_page) + '<=' + str(num_of_pages))
        if cur_page > 1:
                URL="http://" + baseurl + "trade/past/?page="+('%d' % cur_page)+"&limit=100&order=pubdate&dir=desc#table"
                soup=BeautifulSoup(urllib.request.urlopen(URL),from_encoding="utf-8")
        main_table=soup.find("table",class_="tbl_org tbl_org_zakon tbl_org_regedit tbl_torgs ")
        lines=main_table.find_all("tr")
        g=1
        num_ln=len(lines)
        while g < num_ln:
                _str='';
                cur_line=lines[g]
                data_in_line=cur_line.find_all("td")

                #<customer>
                links_in_line=data_in_line[0].find_all('a')
                _str=_str+links_in_line[1].get_text()+';'
                #</customer>
                #<subject>
                _str=_str+data_in_line[1].get_text()+';'
                #</subject>
                g=g+1
                _str=normalUtf(_str)
                inf_file.write(_str)
                inf_file.write("\n")
        inf_file.flush()
        cur_page=cur_page+1
inf_file.close()
