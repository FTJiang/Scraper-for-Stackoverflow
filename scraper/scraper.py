import re
import urlparse
import platform
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import proxy
from selenium.webdriver.common.proxy import *
from queue import Queue
import urllib2
import MySQLdb as mdb

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def change_proxy():
    myProxy = proxy.getProxy()
    service_args = ['--proxy='+myProxy]
    return service_args

def db_init():
    con = mdb.connect('localhost', 'root', 'Jiangft1213', 'stackoverflow')
    cur = con.cursor()
    cur.execute("CREATE TABLE questions (title varchar(200), link varchar(1500))")

def insert_record(elements):
    for element in elements:
        url = element.get_attribute('href')
        print url
        print element.text
        query = "INSERT INTO questions(title,link) " \
        "VALUES(%s,%s)"
        args = (title, link)
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
     
            cursor = conn.cursor()
            cursor.execute(query, args)
     
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
     
            conn.commit()
        except Error as error:
            print(error)
 


if __name__=="__main__":
    link = 'http://stackoverflow.com/questions'
    #provide path of phantomjs execute file
    if platform.system() == 'Windows':
        PHANTOMJS_PATH = './phantomjs.exe'
    else:
        PHANTOMJS_PATH = './phantomjs'
    #proxy.getProxyFile()
    #proxy.viability()
    db_init()
    #use queue to recover from exception
    q = Queue()
    #driver = webdriver.PhantomJS(PHANTOMJS_PATH,service_args=service_args)
    driver = webdriver.PhantomJS(PHANTOMJS_PATH)
    driver.set_window_size(1120, 550)
    q.enqueue(link)
    cnt = 0 
    proxy_used = ''
    while cnt < 1:
        #sleep(5)
        try:
            print link
            driver.get(q.peek())
            q.dequeue()
            if proxy_used == True:
                driver = webdriver.PhantomJS(PHANTOMJS_PATH)
            cnt+=1
        except urllib2.HTTPError,e:
            if e.code == 403:
                driver = webdriver.PhantomJS(PHANTOMJS_PATH,service_args = change_proxy())
                proxy_used = False
                continue
        #extract all the question links and titles
        elements = (driver.find_elements_by_xpath('//a[@class="question-hyperlink"]'))
        insert_record(elements)
        #get url of next question page
        driver.find_element_by_xpath('//span[@class="page-numbers next"]').click()
        #driver.execute_script("document.getElementByClassName('page-numbers next').click()")
        link = driver.current_url
    driver.quit()
    cursor.close()
    conn.close()