__author__ = 'pavel'

import urllib2

def geturltext(url):
    content = ""
    try:
        headers = {'User-Agent': 'Mozilla 5.10'}
        request = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()
    except urllib2.HTTPError, e:
        print e.code
        print e.msg
        print e.headers
        print e.fp.read()
    return content

urlBase = "http://zakupki.gov.ru"

urlPaths = {'purchase': "/223/purchase/public/purchase/info/common-info.html",
            'protocols': "/223/purchase/info/protocols.html",
            'lots': "/223//purchase/info/lot-list.html",
            'documents': "/223/purchase/info/documents.html",
            'changes': "/223/purchase/info/changes-and-clarifications.html",
            'contractInfo': "/233/purchase/info/contractInfo.html",
            'journal': "/233/purchase/info/journal.html"}



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