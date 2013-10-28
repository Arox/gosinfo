__author__ = 'pavel'

import globals

import urllib2
from bs4 import BeautifulSoup


class ParserBase:
    u"""Base class for all parsers"""
    def __init__(self, parserObjectName, params):
        self.params = params
        self.url = ""
        self.soup = None
        self.updateUrl("%s%s?%s" % (globals.urlBase, globals.urlPaths[parserObjectName], self.params))

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
        except urllib2.HTTPError as e:
            if showErrorMessage:
                print("err code = %i" % e.code)
                print("message %s" % e.msg)
                print("headers %s" % e.headers)
                print("fp_read %s " % e.fp.read())
        return content

    def updateUrl(self, url):
        self.url = url
        self.updateSoupFromContent(self.geturltext(self.url))

    def updateSoupFromContent(self, content):
        self.url = ""
        self.soup = BeautifulSoup(content)