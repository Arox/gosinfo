__author__ = 'pavel'
from parserBase import ParserBase
import globals

#purchaseUrl = "http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html" \
#              "?purchaseId=612198&&purchaseMethodType=ep"


class Purchase(ParserBase):
    def __init__(self, purchaseParams):
        ParserBase.__init__(self, 'purchase', purchaseParams)

    def checkIfProtokolsExists(self):
        urlForProtocol = "%s%s?%s" % (globals.urlBase, globals.urlPaths['protocols'], self.params)
        res = len(self.geturltext(url=urlForProtocol, showErrorMessage=False)) != 0
        if __debug__:
            print(res)
        return res


    def purchaseInfo(self):
        purchaseDict = {}
        for table in self.soup.find('div', {'class': 'tablet'}).findAll('table'):
            nodeName = table.caption.text.strip()
            if __debug__:
                print(nodeName)
            purchaseDict[nodeName] = {}
            for tr in table.findAll('tr'):
                (key, value) = tr.findAll('td')[:2]
                purchaseDict[nodeName][key.text.strip()] = value.text.strip()
                if __debug__:
                    print("\t[%s - %s]" % (key.text.strip(), value.text.strip()))
        return purchaseDict


p = Purchase("purchaseMethodType=ep&purchaseId=626328")
p.purchaseInfo()
p.checkIfProtokolsExists()

#RSS
#http://zakupki.gov.ru/223/purchase/public/notice-rss.html?purchaseMethodType=ep&purchaseId=626328
