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
import time

def page(url):
    #if not _page:
    try:
        r = requests.get(url,  headers = global_header ,timeout=10)
    except Exception,e:
        print e
        return
    r.encoding = 'utf-8'
    _page = Pq(r.text)
    return _page



def baiduURLs(url):
    try:
        return [site.attr('href') for site in page(url)('div.result.c-container  h3.t  a').items()]
    except Exception,e:
        print e
        return
    

def bingURLs(url):
    try:
        return [site.attr('href') for site in page(url)('li.b_algo  a').items()]
    except Exception,e:
        print e
        return


def qihu360URLs(url):
    try:
        return [site.attr('href') for site in page(url)('h3.res-title a').items()]
    except Exception,e:
        print e
        return
        

def sogouURLs(url):
    try:
        return  [site.attr('href') for site in page(url)('a[cacheStrategy="qcr:-1"]').items()]
    except Exception,e:
        print e
        return




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

    keyword1 = 'site:'+ root_domain
    keyword2 = '@'+ root_domain

    baidu_page1 = "http://www.baidu.com/baidu?wd=%s" % keyword1
    bing_page1 = "https://cn.bing.com/search?q=%s" % keyword1
    qihu360_page1 = "https://www.so.com/s?q=%s" % keyword1
    sogou_page1 = "https://www.sogou.com/web?query=%s" % keyword1

    baidu_page2 = "http://www.baidu.com/baidu?wd=%s" % keyword2
    bing_page2 = "https://cn.bing.com/search?q=%s" % keyword2
    qihu360_page2 = "https://www.so.com/s?q=%s" % keyword2
    sogou_page2 = "https://www.sogou.com/web?query=%s" % keyword2

    originalURLs = []
    tmpURLs = []

    #max_page_items = 1000

    max_page_items = count#定义下默认的最大页数10
    tmpURLs = []
    #tmpURLs.append(baiduURLs)
    #_page = 'all'
    #百度url提取
    print '[+]Start site_baidu_url extract....'
    for x in range(0,1000,10):
        #此处检验是否已经超过了最大页面
        current_page = (x+10)/10
        print "[+]We've reached the site_baidu_page %s" % str(current_page)
        baidu_url = baidu_page1 + '&pn=' +str(x)
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

    time.sleep(3)

    print '[+]Start @_baidu_url extract....'
    for x in range(0,1000,10):
        #此处检验是否已经超过了最大页面
        current_page = (x+10)/10
        print "[+]We've reached the @_baidu_page %s" % str(current_page)
        baidu_url = baidu_page2 + '&pn=' +str(x)
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
    print '[+]Start site_bing_url extract....'
    init_page = 0
    bing_url_comparison_item = []
    while(1):
        bing_url = bing_page1 + '&first=' +str(init_page)
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
    
    time.sleep(3)

    print '[+]Start @_bing_url extract....'
    init_page = 0
    bing_url_comparison_item = []
    while(1):
        bing_url = bing_page2 + '&first=' +str(init_page)
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
    print '[+]Start site_360so_url extract....'
    init_page = 1
    qihu360_url_comparison_item = []
    while(1):
        qihu360_url = qihu360_page1 + '&pn=' +str(init_page)
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

    time.sleep(3)

    print '[+]Start @_360so_url extract....'
    init_page = 1
    qihu360_url_comparison_item = []
    while(1):
        qihu360_url = qihu360_page2 + '&pn=' +str(init_page)
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
    print '[+]Start site_sogou_url extract....'
    init_page = 1
    sogou_url_comparison_item = []
    while(1):
        sogou_url = sogou_page1 + '&page=' +str(init_page)
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

    time.sleep(3)

    print '[+]Start @_sogou_url extract....'
    init_page = 1
    sogou_url_comparison_item = []
    while(1):
        sogou_url = sogou_page2 + '&page=' +str(init_page)
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
        get_email(orignal_resp)
        #email_list.extend(emails)
        get_domain(orignal_resp)
        #domain_list.extend(domains)
        #print email_list,domain_list
    except Exception,e:
        pass
        #print e



def get_email(orignal_resp):
    resp = orignal_resp.text
    #email_list = []
    try:
        #m1 = re.search(r'[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*@(?:[A-Za-z0-9]+[-.])+[A-Za-z0-9]+', resp)
        #if not m1:
        #    return
        m = re.findall(r'[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*@(?:[A-Za-z0-9]+[-.])+[A-Za-z0-9]+',resp)
        if len(m) > 0:
            for m_item in m:
                if root_domain in m_item:
                    email_list.append(m_item)
        #return email_list
    except Exception,e:
        pass
        #print e

def get_domain(orignal_resp):
    resp = orignal_resp.text
    #domain_list = []
    try:
        #m1 = re.search(r'[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.(?:[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.)+[a-zA-Z0-9][-a-zA-Z0-9]{1,62}', resp)
        #if not m1:
        #    return
        m = re.findall(r'[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.(?:[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.)+[a-zA-Z0-9][-a-zA-Z0-9]{1,62}', resp)
        if len(m) > 0:
            for m_item in m:
                if '.'+root_domain in m_item:
                    domain_list.append(m_item)
        #return domain_list
    except Exception,e:
        pass
        #print e


if __name__ == '__main__':
    #无需mode，传入root_domain即可
    #global root_domain
    root_domain = 'baidu.com'
    exploit(root_domain)

