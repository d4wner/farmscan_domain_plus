#coding=utf-8

import requests

from bs4 import BeautifulSoup
import re
from lxml import etree
import datetime


def domain_find(root_domain):
    try:
        url = 'http://www.' + root_domain
        html = requests.get(url, timeout=5).content
        print '[+]Get content url...'
    except:
        try:
            url2 = 'http://www.' + root_domain
            html = requests.get(url2, timeout=5).text
            print '[+]Get text url...'
        except Exception, e:
            print e
    try:
        domains = re.findall(r'[\w+\-\w+\.]{1,}'+ root_domain , html)
        ips = re.findall(r'(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))' , html)
        return list(set(domains)) + list(set(ips))

    except Exception, e:
        print e
    #return list(set(subdomains))



def exploit(root_domain):
    multi_domains  = domain_find(root_domain)
    print multi_domains
    return multi_domains


    
if __name__ == '__main__':
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#开始时间
    exploit('baidu.com')
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#结束时间