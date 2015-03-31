import nltk
import bs4
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import os
import sys
import StringIO
import socket
import httplib

host='http://bazaraki.com' #len = 9
shost='https://bazaraki.com' #len = 10

exist=True
loadFromFiles=False

wrote=False



readFiles=raw_input("Load from Files? Y/N - [CaseSen]")
if (str(readFiles)=='Y'):
	try:
		tmp_file_data_links=open('file_links.txt').read()
		print "File 'file_links.txt' has been import"
		loadFromFiles=True
	except IOError:
		print "Could not load: file for links"
		loadFromFiles=False
	
	if (loadFromFiles==True):
		try:
			tmp_file_data_teles=open('file_teles_stract.txt').read()
			print "File 'file_teles_stract.txt' has been import"
			loadFromFiles=True
		except IOError:
			print "Could not load: file for teles"
			loadFromFiles=False

if (loadFromFiles==True):
	
	all_links = eval(tmp_file_data_links)
	print "Links Loaded"
	
	telephones = eval(tmp_file_data_teles)
	print "Telephones Loaded"
	

else:
	telephones={}
	all_links={'http://bazaraki.com':False}






	
def scan_link(u):
	global all_links
	global exist
	
	my_links=[]
	
	reqst=urllib2.Request(u)
	reqst.add_header('User-agent','Mozilla/5.0 WinXP')
	try:
		saved=urllib2.urlopen(reqst, timeout=100).read()
	except urllib2.URLError, e:
		print "URL ERROR TU"
		print "->",u
		return None
	except socket.timeout, e:
		print type(e)
		print "Socket error"
		print "->",u
		return None
	except (IOError, httplib.HTTPException):
		print "server response not understood"
		return None
	code=BeautifulSoup(saved)
	bs4element=code.findAll("a")+code.findAll("a",attrs={'class':'paging_url'})
	
	getPhones(code,u)
	
	for j in bs4element:
		my_links.append(j.get('href'))
	
	for lnk in my_links:
		if (lnk==None): continue
		url_ready=str(filtering(lnk))
		if (url_ready=='None'): continue
		if (all_links.has_key(url_ready)==False): 
			all_links.update({url_ready: False})
			exist=True
			



def getPhones(html_code,interests):
	global telephones
	
	
	span_links=html_code.findAll("span",attrs={'class':'field_label'})
	span_texts=[]
	
	link_name=html_code.findAll("a",attrs={'class':'link'})
	
	
	
	
	
	for span_html in span_links:
		tmp_txt=nltk.clean_html(str(span_html))
		span_texts.append(tmp_txt)
	
	for strg_c in range(len(span_texts)):
		if (span_texts[strg_c]=='Telephone :'):
			
			for c in range(len(span_texts)):
				if (span_texts[c]=='Added :'):
					date_added=span_texts[c+1]
					
			for ai in link_name:
				if (ai.get('href')[:12]=='/advertiser/'):
					ad_person_name=nltk.clean_html(str(ai))
			if (telephones.has_key(span_texts[strg_c+1])):
				telephones[span_texts[strg_c+1]][0].append([interests, date_added])
			else:
				telephones[span_texts[strg_c+1]]=[[interests, date_added]],ad_person_name
			



def filtering(url):
	global host
	global shost
	
	if (len(url)==0): return 'None'
	
	indx=url.find('?')
	if (indx>-1): return 'None'
	
	indx=url.find("http", 5)
	if (indx>-1): return 'None'
	
	fndimg=url.find(".jpg")
	if(fndimg>-1): return 'None'
	
	if (url=='None'): return 'None'
	
	if (url[len(url)-1:len(url)]=='/'): url=url[:len(url)-1]
	
	if (url[0]=='/'):
		if (is_number(url[1:len(url)])): return 'None'
		return "http://bazaraki.com"+url
	
	if (url[:9]==host or url[:10]==shost): return url
	
	#print "URL UNRECOGNIZED: "+url
	return 'None'
	

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def write_files():
	if (wrote==False):
		
		print "Writing File for Links"
		fle_links=open(sys.path[0]+'/file_links.txt','w')
		fle_links.write(str(all_links))
		fle_links.close()
		print "Writing File for tel_stract"
		fle_tel_strac=open(sys.path[0]+'/file_teles_stract.txt','w')
		fle_tel_strac.write(str(telephones))
		fle_tel_strac.close()
		

try:

	while(exist):
		exist=False
		
		for link in all_links.keys():
			if (all_links[link]==False):
				
				scan_link(link)
				print link
				all_links[link]=True
				sys.stdout.flush()
				print "LINKS SO FAR: "+str(len(all_links))+" - TELS:"+str(len(telephones))
				
				if (len(telephones)>30000): 
					break;
					write_files()
					wrote=True
		write_files()
		if (len(telephones)>30000): break;

except KeyboardInterrupt:
        write_files()
        wrote=True
        

write_files()

print "Finished"


