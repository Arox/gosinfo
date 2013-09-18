import urllib.request

begin = "http://zakupki.gov.ru/pgz/public/action/search/simple/result?index="
end = "&sortField=lastEventDate&descending=true&tabName=AP&lotView=false&ext=0585e4ac3cd30b3f065d1981c5fdab82&pageX=&pageY="
for i in range(1,  20,  1):
    try:
        req= urllib.request.Request(begin+str(i)+end,headers={'User-Agent' : "Magic Browser"})
        html = urllib.request.urlopen(req).read()
    except urllib.error.URLError as e:
        print(e.reason)
    print(html)
