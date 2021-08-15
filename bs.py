# -*- coding: utf-8 -*-
"""
Created on Tue Agu 21 01:38 2020

@author: Bulend Karadag
"""
import requests
import xml.etree.ElementTree as ET
from lxml import html, etree
from urllib.parse import urlparse
import time
import os.path 
from os import path 
from validator_collection import checkers


def getCompanyName(url):
	t = urlparse(url).netloc
	return '.'.join(t.split('.')[1:2])

def getPage(url):
	if basics['cycle_link_counter']>1:
		print(str(basics['cycle_link_counter'])+' out of '+str(basics['cycle_constant'])+' links have been accessed ...')
	print('Getting the link:'+url) 
	try:
		headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
		page = requests.get(url, headers=headers)
		if page.ok:
			return html.fromstring(page.content)
		else:
			print('The given link has a problem! ...')
			print(page.status_code)
			return False
	except:
		print('Oops! there is a problem with the link ...')
		return False

def getLinks(url):
	pagina=getPage(url)
	basics['cycle_link_counter']+=1
	if pagina is not False:
		url_list=cleanLinks(pagina.xpath(basics['links'])) 
		# in the fisrt cycle of 'continue scraping', don't extract pages ... 
		if continue_scraping == 'N' or continue_scraping == 'n':
			extractToxml(url,pagina)
		return url_list
	else:
		print('The request return empty!')
		return False

def extractToxml(url,pagina):
	basics['d_counter']+=1
	tree = etree.parse("_".join(basics['company'].split())+'.xml')
	root = tree.getroot()
	doc = etree.Element('document', doc_no=str(basics['d_counter']), cycle_no=str(basics['cycle_counter']))
	etree.SubElement(doc, 'company').text = basics['company']
	etree.SubElement(doc, 'url').text = url
	results=dict()
	for x in ['title','department','text','date']:
		results[x] = ''
		for text_list in list(dict.fromkeys(pagina.xpath(basics[x]))):
			if x == 'text':
				results[x] = results[x] + cleanText(text_list)+' '
			else:
				results[x]+=str(text_list)+' '
		results[x]= " ".join(results[x].split())
		#print(results[x])
		etree.SubElement(doc, x).text = results[x]
	root.append(doc)
	tree.write("_".join(basics['company'].split())+'.xml')

def cleanText(raw_text):
	filter_keys=['className','Read more','read more','Click here','click here','assetsBaseUrl','querySelector','<iframe','selectedIndex','/www/','reCAPTCHA','eu-cookie','border-color:','JavaScript','all rights reserved','©','"timeout":','setTime','getTime','margin-left:','function()','@','<script>','<style>','document.location','cookies','privacy policy','Privacy policy','Privacy Policy','Fax:','Tel.:','Tel:','Mobile:','Java Script','ASP.NET','data.page','<![','(Phone)','(Fax)','+31','+49','+55','+33','+46']

	if all(x not in raw_text for x in filter_keys):
		raw_text= " ".join(str(raw_text).split())
		if len(raw_text)>20:
			if len(raw_text.split())>2:
				return raw_text
			else:
				return ' '
		else:
			return ' '
	else:
		return ' '

def checkLinksWorOutRoot(raw_list):
	number_links_http = []
	number_links_wHttp=[]
	for link in list(dict.fromkeys(raw_list)):
		if 'http' in link:
			number_links_http.append(link)
		else:
			number_links_wHttp.append(link)
	if len(number_links_wHttp)!=0 : 
		if len(number_links_http)/len(number_links_wHttp)>1:
			print('Most of the discovered links are WITH the root address ...  ')
			return True
		else:
			print('Most of the discovered links are WITHOUT the root address ...  ')
			return False
	else:
		return False

def cleanLinks(raw_list):
	url_list = []
	if checkLinksWorOutRoot(raw_list):
		filter_keys_wRoot = ['#','mailto','void','.aspx','@','.pdf','.PDF','jpg','JPG','jpeg','JPEG','.png','.PNG','mp3','MP3','.mp4','.MP4','.mov','.zip','.xml','.xls','.xlsx','.txt','.csv']
		for link in list(dict.fromkeys(raw_list)):
			if basics['url'] in link:
				if link.count('http')==1:
					if all(x not in link for x in filter_keys_wRoot):
						url_list.append(link)
	else:
		filter_keys_wtRoot1=[':','www','#','/de/','/fr/','/pt/','/br/','/es/','/tr/','/ca/','/se/','/no/','/be/','/dk/','/vi/','javascript','void','.aspx','@','=','.pdf','.PDF','jpg','JPG','jpeg','JPEG','.png','.PNG','mp3','MP3','.mp4','.MP4','.mov','.zip','.xml','.xls','.xlsx','.txt','.csv','/file/']
		filter_keys_wtRoot2=['','/','/home','/de/','/fr/','/pt/','/br/','/es/','/tr/','/ca/','/se/','/no/','/be/','/dk/','/vi/']
		for link in list(dict.fromkeys(raw_list)):
			if all(x not in link for x in filter_keys_wtRoot1):
				if (link not in filter_keys_wtRoot2):
					url_list.append(basics['url']+link)
	return list(set(url_list))

def update_url_list(new_url_list):
	differ = list(set(new_url_list) - set(basics['url_list']))
	if len(differ)==0:
		print('0 no-new-link is found')
		return basics['url_list']
	else:
		print(str(len(differ))+' new links are discovered ...')
		basics['url_list'] = basics['url_list'] + differ
		return basics['url_list']+differ

def cycle(url_list):
	if url_list is not None:
		#updated_url_list=[]
		initial_list=basics['url_list']
		basics['cycle_counter']+=1
		basics['cycle_link_counter']=1
		basics['cycle_constant']=len(url_list)
		print(str(basics['cycle_counter'])+'th cycle is initiated ...')
		for url in url_list:
			new_url_list = getLinks(url)
			if new_url_list:
				updated_url_list = update_url_list(new_url_list)
			else:
				updated_url_list = basics['url_list']
				print('HTML response has a problem ... the page is not extracted ...')
			#time.sleep(1)
		differ = list(set(updated_url_list) - set(initial_list))
		basics['url_list'] = updated_url_list
		print(str(basics['cycle_counter'])+'st cycle is completed')
		print(str(len(initial_list)+1)+'-links are visited. '+str(len(differ))+' more new links are discovered ...')
		print(str(basics['d_counter'])+'-links were accessible to be extracted and saved to '+basics['company']+'.xml file. ')
		return differ
	else:
		print('The page does not contain html links. Cycle is not initiated')

def getAllUrlFromXML(filename):
	tree = etree.parse(filename)
	root = tree.getroot()
	mylist = root.xpath('//url/text()')
	url_list = []
	for url in mylist:
		url_list.append(url)
	print(str(len(url_list))+' links are discovered in XML file')
	basics['d_counter'] = int(root.xpath('//document/@doc_no')[-1])
	if int(basics['d_counter']) == basics['d_counter']:
		return url_list
	else:
		print('XML file has a problem, please fix it!')
		quit()

def getLastCycleURLfromXML(filename):
	tree = etree.parse(filename)
	root = tree.getroot()
	last_cycle_no=root.xpath('//document/@cycle_no')[-1]
	basics['cycle_counter']=int(last_cycle_no)-1
	mylist = root.xpath('//document[@cycle_no="'+last_cycle_no+'"]/url/text()')
	url_list = []
	for url in mylist:
		url_list.append(url)
	return url_list

def createXML():
	root = ET.Element("root", name=basics['company'])
	tree = ET.ElementTree(root)
	tree.write("_".join(basics['company'].split())+'.xml')
	print('XML file is created successfully')

def scrape(url_list, ContinueScraping):
	basics['url_list']=url_list
	if ContinueScraping:
		ListofLastCycleLinks=getLastCycleURLfromXML(basics['company']+'.xml')
		print(str(len(ListofLastCycleLinks))+'-links will be searched ...  ')
		diff=cycle(ListofLastCycleLinks)
		global continue_scraping
		continue_scraping = 'N'
	else:
		print(str(len(basics['url_list']))+'-links will be searched ...  ')
		diff=cycle(basics['url_list'])

	while True:
		print('There are more '+str(len(diff))+' links to be searched')
		inp = str(input("Would you like to continue: Y/N :  "))
		if inp == 'Y' or inp == 'y':
			diff=cycle(diff)
		elif inp == 'N' or inp == 'n':
			break
		else:
			print('Invalid input, please digit Y or N')

	for i, item in enumerate(diff, start=1):
		print(i, item)
	print('Those above are list of not-visited link ...')
	print(str(len(basics['url_list'])+1)+'-links are discovered ...  '+str(basics['d_counter'])+' links are extracted and saved ...')
	print(str(len(diff))+' links are left behind ... '+str(len(basics['url_list'])-basics['d_counter']-len(diff)+1)+' links were not accessible')
	print('Extracted information from '+str(basics['d_counter'])+'-links are saved to '+basics['company']+'.xml file. ')

########################### END of FUNCTIONS ###########################

print('This is a generic-excavator, designed to scrape an entire website.')
print('By giving a website name, you will start the first cycle of scraping.')
print('This may take a while, depending the size of the given website')
basics=dict()
#basics['url'] = 'https://www.saopaulo.sp.gov.br/ultimas-noticias'
while True:
	url  = str(input("Please provide the root address of the website : "))
	if checkers.is_url(url):
		basics['url']=url
		break
	else:
		print('Please enter a valid web address!')

basics['company']=getCompanyName(basics['url'])
basics['paginate_url'] = 'https://www.syngenta.com/company/media/syngenta-news/year/'
basics['title']='//title//text()'
basics['department']='//*[contains(@class, "breadcrumb")][1]//text()'
basics['date']='//meta[contains(@property, "date") or contains(@property, "published_time")]/@content | //meta[contains(@name, "date") or contains(@name, "Date")]/@content'
basics['text']='//div//text()[not(ancestor-or-self::*[contains(@style,"display:none") or (@aria-hidden="true") or (@hidden)])]'
basics['links']='//a/@href'
basics['paginate_links']='//p[@class="more-link"]//a/@href'
basics['url_list']=[]
basics['cycle_counter']=0
basics['cycle_link_counter']=1
basics['cycle_constant']=0
basics['d_counter']=0

if path.exists(basics['company']+'.xml'):
	print('Seems that this website has already been scraped, would like to continue scraping the same site?')
	print('if your answer is YES(Y) then the website will be scraped from where it was left')
	print('if your answer is NO(N) then the website will be scraped as of the given web-address')  
	continue_scraping = str(input("Would you like to continue: Y/N :  "))
else: 
	continue_scraping = 'N'

while True:
	if continue_scraping == 'Y' or continue_scraping == 'y':
		scrape(getAllUrlFromXML(basics['company']+'.xml'), True)
		break
	elif continue_scraping == 'N' or continue_scraping == 'n':
		createXML()
		scrape(getLinks(basics['url']), False)
		break
	else:
		print('Invalid input, please digit Y or N')


