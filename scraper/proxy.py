import urllib2
import urllib
from bs4 import BeautifulSoup
import RandomAgent
import os
import socket


#function used to get IP, port and type of proxies from website, stored in file named prxy_ip.txt
def getProxyFile():
	url = "https://hidemy.name/en/proxy-list"
	#temp = "'User-Agent':"+'\''+RandomAgent.Agent()+'\''
	#print temp
	hdr = {}
	#use randomized user-agent
	User_Agent = RandomAgent.Agent()
	hdr['User-Agent'] = User_Agent
	req = urllib2.Request(url,headers=hdr)
	#if file has exist, delete and recreate
	if os.path.isfile('proxy_ip.txt'): 
		os.remove('proxy_ip.txt')
	ip_file = open('proxy_ip.txt','w')
	#try:
	page = urllib2.urlopen(req).read()
	#except urllib2.HTTPError,e:
	#	print e.code
	#print page.read()
	soup = BeautifulSoup(page,'html.parser')
	#extract proxies from source html file
	proxies = soup.findAll('tr')
	ip = ''
	port = ''
	host = ''
	for ips in proxies:
		cnt = 0
		for temp in ips.findAll('td'):
			if cnt == 0:		#IP is in the forth td tag
				ip = temp.text
			elif cnt == 1:		#port is in the forth td tag
				port = temp.text
			elif cnt == 4: 		#type is in the forth td tag
				host = temp.text
			cnt+=1
		cnt == 0
		#combine ip, port and type to a string and write it into file
		ip_temp = ip+'\t'+port+'\t'+host+'\n'
		ip_file.write(ip_temp)
	ip_file.close()

'''
function used to delete timeout IP from record file
there is no function in python to delete specific line, so we rewrite the whole file without the line we want to delete
'''
def delete(ip):
	f = open('proxy_ip.txt','r')
	lines = f.readlines()
	f.close()
	f = open('proxy_ip.txt','w')
	for line1 in lines:
		if ip not in line1:
  			f.write(line1)
  	f.close()

#function used to test the proxies from website and delete the timeout proxies from file
def viability():
	socket.setdefaulttimeout(1)
	f = open('proxy_ip.txt','r')
	lines = f.readlines()
	f.close()
	proxys = []
	#This is the url used to test proxies
	url = 'http://ip.chinaz.com/getip.aspx'
	proxies_useful = []
	#test all the proxies
	for i in range(0,len(lines)):
		ip = lines[i].strip('\n').split('\t')
		#print ip
		#value passed into proxies should be a dictionary
		proxy_host = ip[2].lower()+"://"+ip[0]+":"+ip[1]
		proxy_temp = {ip[2].lower():proxy_host}
		try:
			res = urllib.urlopen(url,proxies = proxy_temp).read()
		except Exception,e:
			delete(ip[0])
			print "IP with problem : "+str(proxy_temp)
			print e
			continue
		except socket.error, e:
			pass
	#print str(len(lines))
	#print "test finish"

def getProxy():
	f = open('proxy_ip.txt','r')
	#if proxy pool size less than 5, get new list
	if os.path.getsize(proxy_ip.txt) == 5:
		f.close()
		getProxyFile()
		viability()
	lines = f.readlines()
	f.close()
	ip = random.choice(lines).strip('\n').split('\t')
	proxy_host = ip[0]+":"+ip[1]
	delete(ip[0])
	return proxy_host


