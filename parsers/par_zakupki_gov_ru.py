# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup

#from utils import normalUtf
#from datetime import datetime

ans ='' 

with open('example-gov.txt', 'r') as f:
    ans = f.read()
f.closed


baseurl = "zakupki.gov.ru/"
fullurl = "http://zakupki.gov.ru/pgz/public/action/search/simple/result?index=1&sortField=lastEventDate&descending=true&tabName=AP&lotView=false&ext=0585e4ac3cd30b3f065d1981c5fdab82&pageX=&pageY="

def get_content(url):
    req=urllib.request.Request(url,headers={'User-Agent' : "Magic Browser"})
    req.add_header('Pragma','no-cache')
    
    step = 5
    content = None
    while step > 0:
        try:
            content = urllib.request.urlopen(req,timeout=10).read()
        except urllib.error.URLError as e:
            print(e.reason)
            print(step)
            step -= 1
        else:
            step = 0
    return (req, content)

first_part_url = "http://zakupki.gov.ru/pgz/public/action/search/simple/result?index="
second_part_url = "&sortField=lastEventDate&descending=true&tabName=AP&lotView=false&ext=0585e4ac3cd30b3f065d1981c5fdab82&pageX=&pageY="
'''
Получаем пометки (Новое, Изменения, Для малого бизнеса и ссылки если они есть через :
'''
def get_markt(table , file):
    result = []
    for td in table.find_all('td'):
        a = td.find('a')
        if a == None:
            span1 = td.find('span')
            if span1 != None:
                span2 = span1.find('span')
                if span2 != None:
                    result .append(span2.get_text())
        else:
            span = td.find('span')
            result.append('{0}:{1}'.format( span.get_text(),  a['href']))
    return result

def get_short_content(table,  file):
    i = 0
    result = []
    for a in table.find_all('a'):
        if i == 2:
            pass
        elif i == 1:
            result.append((a.get_text(),  a['href']))
        else:
            span = a.find('span')
            result.append((span.get_text(),  a['href']))
        i+=1    
    return result

def get_full_table_content(url):
    result = ''
    '''with open('example-subgov.txt', 'r') as f:
        result = f.read()
    f.closed
    '''
    file = open(r'example-subgov.txt',  encoding='cp1251')
    result = file.read()
    file.close()
    return result
    
    
    '''
    ---Заказ---
    номер извещения
    краткое наименование аукциона
    способ размещения заказа
    адрес аукциона в интернете
    ---Заказчик---
    Наименование
    Место нахождения
    Почтовый адрес
    ---Контактная информация---
    Почтовый адрес
    Адрес электронной почты
    Телефон
    Факс
    Контактное лицо
    Дополнительная информация
    ---Предмет контракта---
    Полное наименование аукциона
    Начальная цена(максимальная) контракта
    Классификация товаров, работ, услуг
    Количество постовляемого товара (объем услуг)
    ---Место и срок поставки---
    Место
    Срок
    ---Обеспечение заявки---
    Размер обеспечения
    ---Обеспечение исполнения контракта---
    Обеспечение исполнения контракта
    ---Информация о документации об аукционе---
    Сайт где азмещена информация
    Дата и время окончания срока подачи заявок
    Дата окончания срока рассмотрения заявок
    Дата проведения открытого аукциона в электронной форме
    ---Дата публикации---
    Опубликовано
    '''
    
def get_full_content(url,  file):
    html_text = get_full_table_content(url)
    xml=BeautifulSoup(html_text,  from_encoding="utf-8")
    print(xml.notification.placingway.find('name').string)
    #input()
    result = {
    #----Предоставление документов----
    #место доставки
    'deliveryPlace' : xml.notification.competitivedocumentprovisioning.deliveryplace.string, 
    #Срок поставки
    'deliveryTerm' : xml.notification.competitivedocumentprovisioning.deliveryterm.string, 
    #Срок поставки 2
    'deliveryTerm2' : xml.notification.competitivedocumentprovisioning.deliveryterm2.string, 
    
    #----Дата создания----
    'create' : xml.notification.createdate.string, 
    
    #----Заголовок-----
    #Номер извещения
    'notificationNumber' : xml.notification.notificationnumber.string, 
    'orderName' : xml.notification.ordername.string, 
    'placingWayName' : xml.notification.placingway.find('name').string, 
    'placingWayTitle' : xml.notification.placingway.title.string, 
    'etp' : xml.notification.etp.address.string, 
    
    #-----Заказчик-----
    'namePartner' : xml.notification.lots.lot.customerrequirements.customerrequirement.organization.fullname.string,
    'delivePartner' : xml.notification.lots.lot.customerrequirements.customerrequirement.organization.factualaddress.fulladdress.string,
    'postPartner' : xml.notification.lots.lot.customerrequirements.customerrequirement.organization.postaladdress.string,
   
    #-----Контактная информация------ 
    #Название организации
    'orgName' : xml.notification.contactinfo.orgname.string, 
    #Краткое название
    'orgShortName' : xml.notification.contactinfo.orgshortname.string, 
    #ИНН организация
    'orgInn' : xml.notification.contactinfo.orginn.string, 
    #КПП организации
    'orgKpp' : xml.notification.contactinfo.orgkpp.string,
    #Адрес
    'address' : xml.notification.contactinfo.orgfactaddress.string,
    #Почтовый адрес
    'post' : xml.notification.contactinfo.orgpostaddress.string,
    #контакты
    'contact' : [ xml.notification.contactinfo.contactperson.lastname.string
                 ,  xml.notification.contactinfo.contactperson.firstname.string
                ,  xml.notification.contactinfo.contactperson.middlename.string ], 
    #email
    'email' : xml.notification.contactinfo.contactemail.string,
    #phone
    'phone' : xml.notification.contactinfo.contactphone.string,
    #fax
    'fax' : xml.notification.contactinfo.contactfax.string,
    
    #-----Предмет контракта----
    #Полное наименование аукциона (предмет контракта)
    'subject' : xml.notification.lots.lot.subject.string, 
    #Начальная (максимальная) цена контракта
    'maxPrice' : xml.notification.lots.lot.customerrequirements.customerrequirement.maxprice.string, 
    #Валюта
    'currencyCode' : xml.notification.lots.lot.currency.code.string, 
    'currencyName' : xml.notification.lots.lot.currency.find('name').string, 
    #Количество поставляемого товара, объем выполняемых работ, оказываемых услуг
    'count' : xml.notification.lots.lot.customerrequirements.customerrequirement.quantity.string, 
    #Классификация товаров, работ, услуг (код, название, имя группы, номер группы, входят в продукт)
    'products' : [(product.code.string,  product.find('name').string,  product.okdpgroups.groupname.string, product.okdpgroups.groupnumber.string,  product.okdpgroups.includedproducts.string ) for product in xml.notification.lots.lot.products.find_all('product')], 
    #-----Место и срок поставки товара, выполнения работ, оказания услуг----
    #Место поставки товара, выполнения работ, оказания услуг
    'deliveryPlaceInOrder' : xml.notification.lots.lot.customerrequirements.customerrequirement.deliveryplace.string, 
    #Срок поставки товара, выполнения работ, оказания услуг
    'deliveryTermInOrder' : xml.notification.lots.lot.customerrequirements.customerrequirement.deliveryterm.string, 
    
    #-----Обеспечение заявки-----
    'minAmount' : xml.notification.lots.lot.customerrequirements.customerrequirement.guaranteeapp.amount.string, 
    
    #-----Обеспечение исполнения контракта----
    #'warranty' :
   
    #-----Информация о документации об аукционе----
   'doc' :  xml.notification.competitivedocumentprovisioning.www.string,
   
    #-----Информация об аукционе----
    #Дата и время окончания срока подачи заявок на участие в открытом аукционе в электронной форме (по местному времени) 
    'endDate1' : xml.notification.notificationcommission.p1date.string, 
    #Дата окончания срока рассмотрения заявок
    'endDate2' : xml.notification.notificationcommission.p2date.string, 
    #Дата проведения открытого аукциона в электронной форме (по местному времени):
    'endDate3' : xml.notification.notificationcommission.p3date.string, 
    #Опубликовано
    'publish' : xml.notification.publishdate.string, 
    }
    print(result)
    print('\n\n\n')
    print (result['products'])
    
def get_begin_date(table,  file):
    return table.find('span').get_text()
    
def get_change_date(table,  file):
    return table.find('span').get_text()
    
def get_count_money(table,  file):
    return table.find('span').get_text()
    
for i in range(1,  2,  1):
    if ans is None:
        print ("ans is None =(")
        break
    html=BeautifulSoup(ans,from_encoding="utf-8")
    table = html.find('table',  class_='searchResultTable iceDatTbl')
    t = 0
    for row in table.find_all('tr',  class_='iceDatTblRow searchResultTableRow searchResultRow'):
        t+=1
        print(t)
        print(get_markt(row.find('td',  class_ = 'iceDatTblCol searchResultTableCol searchResultColumn').find('table') ,None))
        vShortContent = get_short_content(row.find('td',  class_ = 'iceDatTblCol searchResultTableCol searchResultColumn aLeft').find('table') ,  None)
        print(vShortContent)
        get_full_content(vShortContent[0][0],  None)
        cols = row.find_all('td',  class_ = 'iceDatTblCol searchResultTableCol searchResultColumn tableColumn70')
        print(get_begin_date(cols[0],  None))
        print(get_change_date(cols[1] ,  None))
        print(get_count_money(row.find('td',  class_ = 'iceDatTblCol searchResultTableCol searchResultColumn tableColumn105') ,  None))
        input()
    
 
