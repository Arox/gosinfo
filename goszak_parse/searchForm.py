__author__ = 'pavel'
from bs4 import BeautifulSoup

import globals

#purchaseStages=PLACEMENT_COMPLETE" \
#"&purchaseStages=APPLICATION_FILING" \
#"&purchaseStages=COMMISSION_ACTIVITIES" \

class searchForm:
    u"""class for parsing purchase urls from search form"""
    def __init__(self):
        self.siteBase = "http://zakupki.gov.ru"
        self.searchUrl = self.siteBase + "/223/purchase/public/notification/search.html?d-3771889-p=%i&purchaseStages=%s"
        self.soup = BeautifulSoup(globals.geturltext(self.searchUrlFor()))

    def allPlacementFor(self, purchaseStage = "APPLICATION_FILING", pagelimit = 0):
        self.soup = BeautifulSoup(globals.geturltext(self.searchUrlFor(1, purchaseStage)))
        limit =pagelimit
        if pagelimit == 0:
            limit = self.totalPagesCount()
        for page in range(1, limit + 1, 1):
            #yield from self.allPurchasesFromPage(self.searchUrlFor(page, purchaseStage))
            for x in self.allPurchasesFromPage(self.searchUrlFor(page, purchaseStage)):
                yield x



    def searchUrlFor(self, page = 1, purchaseStage = "APPLICATION_FILING"):
        return self.searchUrl % (page, purchaseStage)
    
    def allPurchasesFromPage(self, pageUrl = "None"):
        if len(pageUrl) != 0:
            for tr in self.soup.findAll(True, 'maintable')[0].tbody.findAll('tr'):
                yield list(set(a['href'] for a in tr.findAll('a') if a['href'].find(globals.urlPaths['purchase']) != -1))[0]

    def totalPagesCount(self):
        pageContainer = [x.split("=")[1] for x in self.soup.find(True, 'arrow')['href'].split("?")[1].split("&") if x.split("=")[0] == "d-3771889-p"]
        if len(pageContainer) != 1:
            return 0
        return int(pageContainer[0])



def main():
    purchasseStage = "PLACEMENT_COMPLETE"
    pageLimit = 1
    searcher = searchForm()
    pages = searcher.allPlacementFor(purchasseStage, pageLimit)
    print(searcher.totalPagesCount())
    for x in pages:
        print(searcher.siteBase + x)

main()

# stdout
#3967
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612232&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612215&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612206&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612205&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612204&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612119&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612201&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612199&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612198&&purchaseMethodType=ep
#http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?purchaseId=612197&&purchaseMethodType=ep