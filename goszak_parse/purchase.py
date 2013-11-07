# -*- coding: utf-8 -*-
__author__ = 'pavel'

from parserBase import ParserBase
import globals

#purchaseUrl = "http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html" \
#              "?purchaseId=612198&&purchaseMethodType=ep"


#http://zakupki.gov.ru
# /223/purchase/public/purchase/info/common-info.html
# ?purchaseId=628882&purchaseMethodType=IS
#        ||       ||        ||
#       \\//     \\//      \\//
#http://zakupki.gov.ru
# /223/purchase/public/purchase/protocol/ip/view-protocol.html
# ?protocolInfoId=648522&purchaseId=628882

class Purchase(ParserBase):
    def __init__(self, purchaseParams):
        ParserBase.__init__(self, 'purchase', purchaseParams)
        self.purchaseID = 0
        for purchaseParam in purchaseParams.split("&"):
            try:
                key, val = purchaseParam.split("=")[:2]
                if key == "purchaseId":
                    self.purchaseID = int(val)
                    break
            except:
                pass

    def checkIfProtokolsExists(self):
        urlForProtocol = "%s%s?%s" % (globals.urlBase, globals.urlPaths['protocols'], self.params)
        content = self.geturltext(url=urlForProtocol, showErrorMessage=False)
        if len(content) != 0:
            self.updateSoupFromContent(content)
            #select last protocol if multiple exists
            protocol = self.soup.findAll('p', {'class': 'protocolName'})[-1]
            if protocol is not None:
                protocolIDValue = int(dict(protocol.attrs)[globals.DOMElementsKeys['purchaseProtocol'][0]])
                protocolID = "%s%s?protocolInfoId=%i&purchaseId=%i" % (globals.urlBase
                                                                   , globals.urlPaths['viewProtocols']
                                                                   , protocolIDValue
                                                                   , self.purchaseID)
                return protocolID
        return None


    def purchaseInfo(self):
        purchaseDict = {}
        for table in self.soup.find('div', {'class': 'tablet'}).findAll('table'):
            nodeName = table.caption.text.strip()
            purchaseDict[nodeName] = {}
            for tr in table.findAll('tr'):
                try:
                    #print(tr)
                    #print("******\r\n")
                    (key, value) = tr.findAll('td')[:2]
                    purchaseDict[nodeName][key.text.strip()] = value.text.strip()
                except ValueError as err:
                    pass
                    #skip lines not equal to pattern:
                    #<td>key</td><td>value</td>
        return purchaseDict

twoprotocolpurchase = "purchaseId=627472&purchaseMethodType=IS"
singleprotocolPurchase = "purchaseId=628882&purchaseMethodType=IS"
p = Purchase(twoprotocolpurchase)
p.purchaseInfo()
p.checkIfProtokolsExists()


#RSS
#http://zakupki.gov.ru/223/purchase/public/notice-rss.html?purchaseMethodType=ep&purchaseId=626328
