import sys
import helpers
reload(sys)
sys.setdefaultencoding("utf-8")

from BeautifulSoup import BeautifulSoup
import collections
import pprint
import urllib2, time, json, ast, itertools
import os.path
import math


global step1 #Get categories
global step2 #Get subdomains + nb of urls
global step3 #Get all the urls per subdomain
global step4 #Write all urls in unique file

step1 = False
step2 = False
step3 = True

############# STEP 1: GET CATEGORIES FOR ALEXA ##############

if step1:

    soup = BeautifulSoup(urllib2.urlopen('http://www.alexa.com/topsites/category/Top/Shopping').read())
    links_table = soup.body.find("div", {"class" : "categories row-fluid "})
    list_cat = []
    for cat in links_table.findAll("ul", {"class" : "subcategories span3"}):
        for row in cat.findAll('li'): 
            list_cat.append(row.a.get("href").encode('utf-8')+'\n')

    print list_cat
    f = open('alexa_categories.txt','r+')
    for d in list_cat:
        f.write(d)

################# STEP 2 : GET LIST OF ALL PARSABLE SUBS #########################

if step2:
    categories = open('alexa_categories.txt','r+').read().split('\n')
    #total_subs = []
    f = open('alexa_subs.txt','w')

    for cat in categories:        
        helpers.get_all_valid_subs_of_page(f, cat)


################# STEP 3: for each subdomain, build folder & get urls ###########################

if step3:

    ## SORT SUBS
    helpers.resort_all_subs()
    todo_subs_file = 'alexa_subs_to_do.txt'
    # PARSE TODO SUBS
    with open(todo_subs_file) as all_subs:
        for s in all_subs:
            try:
                helpers.scrape_sub(s)
                print "Scraping for " + s + "finished"
                time.sleep(2)
            except Exception,e:
                print str(e)
