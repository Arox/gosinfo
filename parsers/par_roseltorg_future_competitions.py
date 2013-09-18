import urllib.request
from bs4 import BeautifulSoup
from utils import normalUtf
from datetime import datetime
#определение количества страниц
baseurl = 'etp.roseltorg.ru/'

def subInfo(a_url):
    v_url = "http://"+baseurl[0:-1]+a_url
    v_soup = BeautifulSoup(urllib.request.urlopen(v_url),from_encoding="utf-8")
    v_info = v_soup.find_all(class_ = "data-right")
    v_result = ''
    for v_line in v_info:
        v_data = v_line.find('p')
        if not (v_data is None):
            v_result += v_data.get_text() + ';'
    return v_result

URL="http://" + baseurl + "trade/quotes/future/?page=1&limit=100"
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
inf_file=open("./"+baseurl+str(datetime.now()) +"_roseltorg_future_competitions.txt","w")
cur_page=1
while cur_page <= num_of_pages:
            if cur_page > 1:
                        URL="http://" + baseurl + "trade/quotes/future/?page="+('%d' % cur_page)+"&limit=100"
                        soup=BeautifulSoup(urllib.request.urlopen(URL),from_encoding="utf-8")
            main_table=soup.find("table",class_="tbl_org tbl_org_zakon tbl_org_regedit tbl_torgs ")
            lines=main_table.find_all("tr")
            g=1
            num_ln=len(lines)
            while g < num_ln:
                        _str='';
                        cur_line=lines[g]
                        #begin get information about competition
                        link = cur_line['onclick']
                        url_with_full_inf = link.split("'")[1]
                        _str+=subInfo(url_with_full_inf)
                        #end get information about competition

                        data_in_line=cur_line.find_all("td")
                        #<customer>
                        _str=_str+data_in_line[0].get_text()+';'
                        #</customer>
                        #<subject>
                        _str=_str+data_in_line[1].get_text()+';'
                        #</subject>
                        #<date>
                        _str=_str+data_in_line[2].get_text()+';'
                        #</date>
                        g=g+1
                        _str = normalUtf(_str)
                        inf_file.write(_str)
                        inf_file.write("\n")
            inf_file.flush()
            cur_page=cur_page+1
inf_file.close()
