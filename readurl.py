#from bs4 import BeautifulSoup
import urllib2
#import re

#def readContentFromPage(number):
#  url = "zakupki.gov.ru/pgz/public/action/search/simple/result?index="+str(number)+"&sortField=lastEventDate&descending=true&tabName=AP&lotView=false&ext=0585e4ac3cd30b3f065d1981c5fdab82&pageX=&pageY="
#  res = urllib2.urlopen(url).read()
#  print(res)
#  input()

res = urllib2.urlopen("http://zakupki.gov.ru/pgz/public/action/search/simple/run").read()
#html = BeautifulSoup(res)
#lst = html.findAll("a", {"onclick" : re.compile('paginateTab*')})
#tag = lst[-1]
#count = re.compile('\d+').findall(tag['onclick'])

#for i in range(1, int(count[0])+1, 1):
#  readContentFromPage(i)
