# -*- coding: utf-8 -*-
__author__ = 'pavel'

from parserBase import ParserBase
import globals

#TODO add parsing for maximum prise
#it is in applicant list and decision page
# but how return it?
#it may be also found in lot list

class Protocol(ParserBase):
    u"""Protocol page parser"""
    def __init__(self, protocolParams):
        ParserBase.__init__(self, 'viewProtocols', protocolParams)
        self.protocolInfoID = 0
        for protocolParam in protocolParams.split("&"):
            try:
                key, val = protocolParam.split("=")[:2]
                if key == "protocolInfoId":
                    self.protocolInfoID = int(val)
                    break
            except ValueError:
                pass

    def protocolApplicantList(self):
        urlGetParam = "protocolInfoId=%i" % self.protocolInfoID
        url = "%s%s?%s" % (globals.urlBase, globals.urlPaths['protocolApplicants'], urlGetParam)
        content = self.geturltext(url=url, showErrorMessage=False)
        aplicantList = []
        if len(content) != 0:
            self.updateSoupFromContent(content)
            applicantTableIterator = self.soup.find('tr', {'class': 'expandable-row'}).table.findAll('tr')
            keys = [x.text for x in applicantTableIterator[0].findAll('td')]
            #Номер - 0
            #Участник -1
            #Дата и время получения заявки - 2
            #Предложенная цена договора -3
            if len(applicantTableIterator) == 1:
                # if result table not filled
                aplicantList.append((zip(keys, ['EMPTY'] * len(keys))))
            else:
                for aplicant in applicantTableIterator[1:]:
                    values = []
                    column = 0
                    for td in aplicant.findAll('td'):
                        if column in [0, 2, 3] and td is not None:
                            values.append(td.text.strip())
                        else:
                            # parse participant column
                            href = td.find('a')['href']
                            values.append((td.p.text.strip(), href))
                        column += 1
                    resDict = (zip(keys, values))
                    aplicantList.append(resDict)
        return aplicantList

    def protocolDecision(self):
        urlGetParam = "protocolInfoId=%i" % self.protocolInfoID
        url = "%s%s?%s" % (globals.urlBase, globals.urlPaths['protocolDesision'], urlGetParam)
        content = self.geturltext(url=url, showErrorMessage=False)
        aplicantList = []
        if len(content) != 0:
            self.updateSoupFromContent(content)
            applicantTableIterator = self.soup.find('tr', {'class': 'expandable-row'}).table.findAll('tr')
            keys = [x.text for x in applicantTableIterator[0].findAll('td')]
            if len(applicantTableIterator) == 1:
                # if result table not filled
                aplicantList.append((zip(keys, ['EMPTY'] * len(keys))))
            else:
                for aplicant in applicantTableIterator[1:]:
                    values = []
                    for td in aplicant.findAll('td'):
                        selectInColumn = td.find('select')
                        if selectInColumn is None:
                            values.append(td.text.strip())
                        else:
                            selectedOption = selectInColumn.find('option', {"selected": "selected"})
                            if selectedOption is None:
                                # if select attribute not specified
                                # select first option
                                selectedOption = selectInColumn.option
                            if len(selectedOption['value']) == 0:
                                values.append('EMPTY')
                            else:
                                values.append(selectedOption['value'])
                    resDict = (zip(keys, values))
                    aplicantList.append(resDict)
        return aplicantList

#twoapplicantprotocol = "protocolInfoId=663050&purchaseId=627472"
twoapplicantprotocol = "protocolInfoId=663050&purchaseId=627472"
noapplicantprotocol = "protocolInfoId=645636&purchaseId=625793"
p = Protocol(twoapplicantprotocol)
for x in p.protocolApplicantList():
    for y in x:
        print("%s - %s" % y)



    #On protocol page for purchase
        #http://zakupki.gov.ru/223/purchase/public/purchase/info/protocols.html
        # ?purchaseId=625793&purchaseMethodType=IS
    #we can find protocol ID
        #<p positionmarker="1" class="protocolName" protocolinfoid="645636" protocolentityid="628612" version="1" status="P">
        #</p>
    #which redirects us on protocol page
        #http://zakupki.gov.ru/223/purchase/public/purchase/protocol/ip/view-protocol.html
        # ?protocolInfoId=645636&purchaseId=625793
    #on this page we can find applications list tab
        #http://zakupki.gov.ru/223/purchase/public/purchase/protocol/ip/application/list.html
        # ?noticeInfoId=&protocolInfoId=645636&mode=view
    #and commission decision
        #http://zakupki.gov.ru/223/purchase/public/purchase/protocol/ip/application/comission-decision.html
        # ?noticeInfoId=&protocolInfoId=645636&mode=view