#coding=utf-8
import requests
import re
import time
from bs4 import BeautifulSoup

def exploit(root_domain):
    '''start exploit'''
    session = requests.Session()
    url1 = "https://github.com/login"
    rep1 = session.get(url1)
    #pattern = re.compile(r'<input name="authenticity_token" type="hidden" value="(.*)" />')
    pattern = re.compile(r'<input type="hidden" name="authenticity_token" value="(.*)" />')
    a_token = pattern.findall(rep1.text)[0]

    url2 = "https://github.com/session"
    data2 = {
        'commit':'Sign+in',
        'utf8':'%E2%9C%93',
        'authenticity_token':a_token,
        'login':'sresult',
        'password':'s4n-test@g1t'
    }
    rep2 = session.post(url2,data=data2)

    url3 = "https://github.com/search?&q="+root_domain+"&type=Code"
    rep3 = session.get(url3)
    print "get total page num..."
    page_num = find_count(rep3.text)
    print "get total num done!!!"
    print "send each request..."
    t = 0
    the_domain = []
    #the_sensitive_item = {}
    the_email = []
    #for i in range(1,page_num+1):
    for i in range(1,5):
        target = 'https://github.com/search?p='+str(i)+'&q='+root_domain+'&ref=searchresults&type=Code'
        print target
        time.sleep(1)
        thehtml = session.get(target)
        html = thehtml.text
        if html is not None:

            the_domain.extend(find_domain(html,root_domain))
            #the_sensitive_item =  dict(the_sensitive_item.items() + find_sensitive_item(html).items())
            the_email.extend(find_email(html,root_domain))
        else:
            print "No."+str(i)+" is None!!!"
    the_domain_list =  list(set(the_domain))
    the_email_list =  list(set(the_email))
    print the_domain_list
    print the_email_list
    #return the_domain_list,the_email_list
    return the_domain_list + the_email_list 



    print "[+]Git leak finish spider!!!"


def find_count(s):
    m = re.search(r'">(\d+?)</a> <a class="next_page" rel="next"',s)
    if m:
        count = int(m.group(1))
        print "count = " + m.group(1)
    else:
        count = 0
        print "no count!!!"
    return count

def find_email(s,root_domain):
    email_list = []
    soup = BeautifulSoup(s)
    tables = soup.find_all("table", attrs={"class": "highlight"})
    for table in tables:
        if root_domain in table.text:
            m = re.findall(r'[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*@(?:[A-Za-z0-9]+[-.])+[A-Za-z0-9]+',table.text)
            print m
            if len(m) > 0:
                for m_item in m:
                    if root_domain in m_item:
                        email_list.append(m_item)
            else:
                print 'Email get error!'
    return email_list

def find_domain(s,root_domain):
    domain_list = []
    soup = BeautifulSoup(s)
    tables = soup.find_all("table", attrs={"class": "highlight"})
    for table in tables:
        if root_domain in table.text:
            #m = re.findall(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?', table.text)
            #print m
            m = re.findall(r'[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.(?:[a-zA-Z0-9][-a-zA-Z0-9]{1,62}\.)+[a-zA-Z0-9][-a-zA-Z0-9]{1,62}',table.text)
            if len(m) > 0:
                for m_item in m:
                    if root_domain in m_item:
                        domain_list.append(m_item)
            else:
                print 'domain get error!'
    return domain_list

if __name__ == '__main__':
    #无需mode，传入root_domain即可
    global root_domain
    root_domain = 'venustech.com.cn'
    exploit(root_domain)


