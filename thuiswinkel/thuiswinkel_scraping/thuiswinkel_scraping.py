import sys
#from helpers import get_all_urls_from_page
reload(sys)
sys.setdefaultencoding("utf-8")

from  BeautifulSoup import BeautifulSoup
import urllib2, time, json, ast, pyparsing, itertools
import collections
import os.path
import math
import string

global step1 #Get categories
global step2 #Get subdomains + nb of urls
global step3 #Get all the urls per subdomain
global step4 #Write all urls in unique file

step1 = True
step2 = False


def get_all_results_from_page(url, file):
    response = urllib2.urlopen(url).read()
    soup = BeautifulSoup(response)
    list = soup.find('div',{"data-equalizeheights" : "container"})
    try:
        blocks = list.findAll('div',{"data-equalizeheights":"content"})
        for b in blocks:
            link = b.a.get("href")
            file.write(link + '\n')
            print link
    except Exception,e:
            print str(e)    

if step1:
    for letter in list(string.ascii_uppercase):
        url = "https://www.thuiswinkel.org/ledenlijst/?itemsperpage=50&firstletter=" + letter
        output_file = 'thuiswinkel/thuiswinkel' + letter + '.txt'
        print output_file
        file = open(output_file, 'w')
        response = BeautifulSoup(urllib2.urlopen(url).read())
        nb_results = int(response.find('div', {'class':'col-sm-6 col-md-8'}).div.div.h3.string.split(' ')[0])
        print nb_results
        nb_page = int(math.ceil(float(nb_results)/50))
        print nb_page
        get_all_results_from_page(url, file)
        if nb_page > 1:
            for i in range(1,nb_page):
                print i
                url = "https://www.thuiswinkel.org/ledenlijst/?itemsperpage=50&firstletter=" + letter + "&page=" + str(i+1)
                get_all_results_from_page(url, file)

#if step2:
    #dir = 'thuiswinkel/'
    #json_output = open('thuiswinkel_urls_json.txt','w')
    #list_output = open('thuiswinkel_urls_list.txt','w')
    #list_urls = ""
    #dict_urls = dict()
    #for filename in os.listdir(dir):
    #    with open(dir + filename) as f:
    #         list_urls += f.read()
    #title = "https://www.thuiswinkel.org/ledenlijst/"
    #dict_urls[title] = list_urls.split('\n')
    #count_urls = len(dict_urls[title])
    
    
    #d = collections.OrderedDict(sorted(dict_urls.items()))
    #json_output.write(json.dumps(d,indent=2))
    #list_output.writelines(list_urls)
  
    #print "We have " + str(count_urls) + " urls for thuiswinkel"