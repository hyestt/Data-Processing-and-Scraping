import requests
import lxml.html
from lxml import etree
import urllib.request
import re
import csv

# extract the html file from the website "http://search.books.com.tw/search/query/key/python/cat/all"
urllib.request.urlretrieve("http://search.books.com.tw/search/query/key/python/cat/all", "bookstore.html")

infile = open('bookstore.html', 'rb')
bookstore_html = infile.read()
infile.close()

# for html need to use lxml.html.fromstring
tree = lxml.html.fromstring(bookstore_html)

#extract the title of top 20 html book (in order to rename the download html file)
def get_titles():
    titles = tree.xpath('//ul[@class="searchbook"]//li/h3/a')
    out = []
    for title in titles:
        #clean the output data (remove \t and \n)
        clean_title = "".join(title.text_content().split())
        #remove / and other symbol, which would cause error when produce html file's title
        import re
        if "/" in clean_title:
            clean_title = re.sub('[!@#$/]', '', clean_title)
        out.append(clean_title)
    return out


#extract top 20 html book website url
def get_urls():
    links = tree.xpath('//ul[@class="searchbook"]//h3/a')
    out = []
    for link in links:
        # we use this if just in case some tags lack an href attribute
        if 'href' in link.attrib:
            out.append(link.attrib['href'])
    return out

#download all top 20 html page with its title
for i in range(20):
    urllib.request.urlretrieve(get_urls()[i],get_titles()[i])


def get_content(website):
    infile = open(website, 'rb')
    html = infile.read()
    infile.close()
    output = {}

    tree = lxml.html.fromstring(html)

    title_elem = tree.xpath('//div/h1')[0]
    output['Title'] = title_elem.text_content()

    auther_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li//a[1]')[2]
    output['Auther'] = auther_elem.text_content()

    #Some of books have translator, some of books do not have translator. If there is no translator
    #the test would return an empty list. with/without translator would interefere the scraping order
    #of other elements
    test = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[5]')
    if not test:
        translator_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[2]/a')[0]
        output['Translator'] = "NULL"

        publisher_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[2]/a[1]/span')[0]
        output['Publisher'] = publisher_elem.text_content()

        publishdate_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[3]')[0]
        #Use re.sub to remove the useless character
        clean_publishdate = re.sub("出版日期：","",publishdate_elem.text_content())
        output['Publish Date'] = clean_publishdate

        language_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[4]')[0]
        #Use re.sub to remove the useless character
        clean_language = re.sub("語言：","",language_elem.text_content())
        #remove the trailing space
        clean_language = clean_language.strip()
        output['Language'] = clean_language

    else:
        translator_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[2]/a')[0]
        output['Translator'] = translator_elem.text_content()

        publisher_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[3]/a[1]/span')[0]
        output['Publisher'] = publisher_elem.text_content()

        publishdate_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[4]')[0]
        #Use re.sub to remove the useless character
        clean_publishdate = re.sub("出版日期：","",publishdate_elem.text_content())
        output['Publish Date'] = clean_publishdate

        language_elem = tree.xpath('//div[@class="type02_p003 clearfix"]/ul/li[5]')[0]
        #Use re.sub to remove the useless character
        clean_language = re.sub("語言：","",language_elem.text_content())
        #remove the trailing space
        clean_language = clean_language.strip()
        output['Language'] = clean_language

    price_elem = tree.xpath('//div/ul[@class="price"]/li[1]/em')[0]
    #Change the price from NTD to USD
    price = round(int(price_elem.text_content())/30,2)
    output['Price(USD)'] = "${}".format(price)

    discount_elem = tree.xpath('//ul[@class="price"]/li[2]/strong[1]/b')[0]
    discount = 100 - int(discount_elem.text_content())
    output['Discount'] = "{}% off".format(discount)

    discountprice_elem = tree.xpath('//strong[@class="price01"]/b')[0]
    discountprice = round(int(discountprice_elem.text_content())/30,2)
    output['Discount Price(USD)'] = "${}".format(discountprice)

    content_elem = tree.xpath('//div[@class="mod_b type02_m057 clearfix"][1]/div[@class="bd"]/div[@class="content"]')[0]
    clean_introofbook = content_elem.text_content().lstrip().rstrip()
    output['Introduction of book'] = clean_introofbook

    #same, because some of books do not have introduction of author
    test2 = tree.xpath('//div[@class="mod_b type02_m057 clearfix"][2]/div[@class="bd"]/div[@class="content"]')
    if not test2:
        output['Introduction of author'] = "NULL"

    else:
        author_intro_elem = tree.xpath('//div[@class="mod_b type02_m057 clearfix"][2]/div[@class="bd"]/div[@class="content"]')[0]
        output['Introduction of author'] = author_intro_elem.text_content()

    toc_elem = tree.xpath('//div[@id="M201105_0_getProdTextInfo_P00a400020009_h2"]')[0]
    clean_toc = toc_elem.text_content().lstrip().rstrip()
    output['Table of content'] = clean_toc

    ISBN_elem = tree.xpath('//div[@class="bd"]/ul[1]/li[1]')[0]
    #Use re.sub to remove the useless character
    clean_ISBN = re.sub("ISBN：","",ISBN_elem.text_content())
    output['ISBN:'] = clean_ISBN

    sort_elem = tree.xpath('//ul[@class="sort"]/li[1]')[0]
    #Use re.sub to remove the useless character
    clean_sort = re.sub("本書分類：","",sort_elem.text_content())
    output['Sort:'] = clean_sort

    delivery_elem = tree.xpath('//li[@class="prd007_new_icon1 clearfix"]')[0]
    #Use re.sub to remove the useless character
    clean_delivery = re.sub("可配送點：","",delivery_elem.text_content())
    clean_delivery = clean_delivery.split()
    output['Delivery countries:'] = clean_delivery

    return output


# for i in range(20):
#     print(get_content(get_titles()[i]))

#export the data to csv file
#Use utf-8-sig as encoding to demonstrate Mandarin character
with open('python_book.csv', 'w', newline='',encoding='utf-8-sig') as csvfile:
    fieldnames = ['Title', 'Auther', 'Translator', 'Publisher', 'Publish Date',
'Language', 'Price(USD)', 'Discount', 'Discount Price(USD)', 'Introduction of book',
'Introduction of author', 'Table of content', 'ISBN:', 'Sort:', 'Delivery countries:']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(20):
        writer.writerow(get_content(get_titles()[i]))


