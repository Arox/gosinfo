__author__ = 'pavel'

from bs4 import BeautifulSoup
import urllib2

import globals

#purchaseUrl = "http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html" \
#              "?purchaseId=612198&&purchaseMethodType=ep"


class Purchase:
    def __init__(self, purchaseParams):
        self.purchaseParams = purchaseParams
        self.soup = BeautifulSoup(self.geturltext("%s%s?%s" % (globals.urlBase, globals.urlPaths['purchase'], self.purchaseParams)))

    def checkIfProtokolsExists(self):
        urlForProtocol = "%s%s?%s" % (globals.urlBase, globals.urlPaths['protocols'], self.purchaseParams)
        res = len(self.geturltext(url=urlForProtocol, showErrorMessage=False)) != 0
        if __debug__:
            print(res)
        return res


    @staticmethod
    def geturltext(url, showErrorMessage = True):
        content = ""
        if __debug__:
            print(url)
        try:
            headers = {'User-Agent': 'Mozilla 5.10'}
            request = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(request)
            content += response.read()
        except urllib2.HTTPError, e:
            if showErrorMessage:
                print("err code = %i" % e.code)
                print("message %s" % e.msg)
                print("headers %s" % e.headers)
                print("fp_read %s " % e.fp.read())
        return content

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
