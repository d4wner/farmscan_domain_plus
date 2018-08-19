#!/usr/bin/python
#coding=utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pyquery import PyQuery as Pq
from random import choice
import re
import threadpool


def page(url):
    #if not _page:
    r = requests.get(url,  headers = global_header ,timeout=10)
    r.encoding = 'utf-8'
    _page = Pq(r.text)
    return _page



def baiduURLs(url):
    return [site.attr('href') for site in page(url)('div.result.c-container  h3.t  a').items()]
    

def bingURLs(url):
    return [site.attr('href') for site in page(url)('li.b_algo  a').items()]

def qihu360URLs(url):
    return [site.attr('href') for site in page(url)('h3.res-title a').items()]
        

def sogouURLs(url):
    return  [site.attr('href') for site in page(url)('a[cacheStrategy="qcr:-1"]').items()]




def exploit(domain):
    global email_list, domain_list, global_header,global_timeout,root_domain
    root_domain = domain
    email_list = []
    domain_list = []  
    global_timeout = 10
    global_header = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    #_page = None
    count = 1000 

    keyword = 'site:'+ root_domain

    baidu_page = "http://www.baidu.com/baidu?wd=%s" % keyword
    bing_page = "https://cn.bing.com/search?q=%s" % keyword
    qihu360_page = "https://www.so.com/s?q=%s" % keyword
    sogou_page = "https://www.sogou.com/web?query=%s" % keyword

    originalURLs = []
    tmpURLs = []

    #max_page_items = 1000

    max_page_items = count#定义下默认的最大页数10
    tmpURLs = []
    #tmpURLs.append(baiduURLs)
    #_page = 'all'
    #百度url提取
    print '[+]Start baidu_url extract....'
    for x in range(0,1000,10):
        #此处检验是否已经超过了最大页面
        current_page = (x+10)/10
        print "[+]We've reached the baidu_page %s" % str(current_page)
        baidu_url = baidu_page + '&pn=' +str(x)
        test_resp = requests.get(baidu_url,  verify=False, headers = global_header ,timeout=global_timeout ).text
        match = re.search("parseInt\(\'1\'\)",test_resp)
        if x != 0 and match:
            break
        baidu_url_results = baiduURLs(baidu_url)

        if len(baidu_url_results):
            tmpURLs.extend(baidu_url_results)
        
        if x // 10 >= max_page_items:
            break
        else:
            break
    print tmpURLs
    #Bing url提取
    print '[+]Start bing_url extract....'
    init_page = 0
    bing_url_comparison_item = []
    while(1):
        bing_url = bing_page + '&first=' +str(init_page)
        bing_url_results = bingURLs(bing_url)
        if len(set(bing_url_results).symmetric_difference(set(bing_url_comparison_item))):
            #两个数组有差异的话，继续运行，传承bing_url_comparison_item
            tmpURLs.extend(bing_url_results)
            bing_url_comparison_item = bing_url_results
            init_page = init_page + 1
        #这里可以防止tag规则改动，采集停不下来。
        elif init_page >= max_page_items:
            break
        else:
            break  
    print tmpURLs 
    #360so url提取
    print '[+]Start 360so_url extract....'
    init_page = 1
    qihu360_url_comparison_item = []
    while(1):
        qihu360_url = qihu360_page + '&pn=' +str(init_page)
        qihu360_url_results = qihu360URLs(qihu360_url)
        if len(set(qihu360_url_results).symmetric_difference(set(qihu360_url_comparison_item))):
            #两个数组有差异的话，继续运行，传承bing_url_comparison_item
            tmpURLs.extend(qihu360_url_results)
            qihu360_url_comparison_item = qihu360_url_results
            init_page = init_page + 1
        if init_page // 10 >= max_page_items:
            break
        else:
            break
    print tmpURLs
    #sogou url提取
    print '[+]Start sogou_url extract....'
    init_page = 1
    sogou_url_comparison_item = []
    while(1):
        sogou_url = sogou_page + '&page=' +str(init_page)
        sogou_url_results = sogouURLs(sogou_url)
        if len(set(sogou_url_results).symmetric_difference(set(sogou_url_comparison_item))) and len(sogou_url_results):
            #两个数组有差异的话，继续运行，传承bing_url_comparison_item
            for sogou_url_result in sogou_url_results:
                if 'http:' not in sogou_url_result:
                    sogou_url_result_new = 'http://www.baidu.com/' + sogou_url_result
                    tmpURLs.append(sogou_url_result_new)
        
            #tmpURLs.extend(sogou_url_results)
            sogou_url_comparison_item = sogou_url_results
            init_page = init_page + 1
        if init_page // 10 >= max_page_items:
            break
        else:
            break
    #aol url提取【特不稳定，暂不采用】https://search.aol.com/aol/search?q=site:baidu.com&b=61
    #google url提取【整合代理池后采用】
    originalURLs = list(set([tmpurl for tmpurl in tmpURLs]))
    print originalURLs
    #print originalURLs
    #mode不为空触发
    #if mode:
    try:
        pool = threadpool.ThreadPool(20)
        reqs = threadpool.makeRequests(spider, originalURLs)
        [pool.putRequest(req) for req in reqs]
        pool.wait()

        #if mode == 'domain':
        email_list = list(set(email_list))
        domain_list = list(set(domain_list))
        print email_list, domain_list
        #return email_list,domain_list
        return email_list + domain_list 

    except Exception,e:
        print e
    print' [+]search_engine_spider  has been end...'
    #return originalURLs
#social_spider模块组
def spider(url):
    try:
        #resp = requests.get(url, verify=False, headers ={"User-agent":choice(global_config.infos['User-Agent'])} ,timeout=global_config.infos['timeout']).text
        orignal_resp = requests.get(url, verify=False, headers = global_header ,timeout=global_timeout)
        #return resp
        #if mode == 'domain':
        emails = get_email(orignal_resp)
        email_list.extend(emails)
        domains = get_domain(orignal_resp)
        domain_list.extend(domains)
        #print email_list,domain_list
    except Exception,e:
        print e



def get_email(orignal_resp):
    resp = orignal_resp.text
    #email_list = []
    try:
        m = re.findall(r'[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*@(?:[A-Za-z0-9]+[-.])+[A-Za-z0-9]+',resp)
        if len(m) > 0:
            for m_item in m:
                if root_domain in m_item:
                    email_list.append(m_item)
        return email_list
    except Exception,e:
        print e

def get_domain(orignal_resp):
    resp = orignal_resp.text
    #domain_list = []
    try:
        m = re.findall(r'[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.(?:[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.)+[a-zA-Z0-9][-a-zA-Z0-9]{1,62}', resp)
        if len(m) > 0:
            for m_item in m:
                if root_domain in m_item:
                    domain_list.append(m_item)
        return domain_list
    except Exception,e:
        print e


if __name__ == '__main__':
    #无需mode，传入root_domain即可
    #global root_domain
    root_domain = 'baidu.com'
    exploit(root_domain)
