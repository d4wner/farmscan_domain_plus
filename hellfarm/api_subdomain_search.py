#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
from lxml import etree

def api_subdomains_findsubdomains(url):
    subdomains = []
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    table = soup.find("table", attrs={"class": "table table-striped js-results-table"})
    links = table.find_all("a")
    for link in links:
        if '.' in link.text:
            subdomains.append(link.text.strip())
    return list(set(subdomains))

def api_subnets_findsubdomains(url):
    subnets = []
    html = requests.get(url).text
    dom_tree = etree.HTML(html)
    links = dom_tree.xpath("//li[@class='subnets-list-item js-toggle-collapse']/div[@class='ip']/text()")
    for link in links:
        if link.strip():
            subnets.append(link.strip())
    return list(set(subnets))


def exploit(root_domain):
    subdomains = []
    subnets = []
    findsubdomains_url = 'https://findsubdomains.com/subdomains-of/%s' % root_domain
    subdomains.extend(api_subnets_findsubdomains(findsubdomains_url))
    subnets.extend(api_subdomains_findsubdomains(findsubdomains_url))
    #return subdomains,subnets
    return subdomains + subnets 


    
if __name__ == '__main__':
    exploit('baidu.com')
    #print api_subnets_findsubdomains(url)
    #print api_subdomains_findsubdomains(url)
   


