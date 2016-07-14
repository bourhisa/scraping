# from bs4 import BeautifulSoup
from  BeautifulSoup import BeautifulSoup
import urllib2
import os.path
import math
import time
import sys

def get_all_urls_from_page(url): ## FOR ONE GIVEN PAGE, RETURN THE 25 URLS MAX CONTAINED
    soup = soup_url(url)
    links = soup.findAll('li', {"class" : "site-listing"})
    list_urls = list()
    for l in links:
        b = l.a.get('href')
        r = soup_url('http://www.alexa.com' + b)
        link = r.find('a', {"class" : "offsite_overview"}).get('href')
        list_urls.append(link + '\n')
        print link
    return list_urls

def scrape_sub(s): # ORGANISES THE PARSING OF A SUBDOMAIN
    nb = int(s.split('|')[1])
    nb_base = nb_urls = get_nb_links_sub(s)

    while nb_urls-nb_base < 100: # Not to parse > 100 urls at a time to avoid forbidden access (http 403)
        print str(nb_urls) + " urls for this subdomain out of " + str(nb)
        if nb_urls >= nb:
            resort_all_subs()
            print "This sub is now completed"
            break
        else:
            try:
                sub = s.split('|')[0]
                num_page = int(math.floor(nb_urls/25)) # Get the number of the page to parse, since each page contains 25 urls, 
                if num_page == 0:
                    url_to_parse = 'http://www.alexa.com' + sub
                else:
                    short_url ='/'.join(sub.split('/')[3:])
                    url_to_parse = 'http://www.alexa.com/topsites/category;' + str(num_page) + '/' + short_url
                file_path = 'alexa_urls/www.alexa.com' + sub.replace('/','+') + '.txt'
                file = open(file_path,'r+')
                list_urls = file.readlines()
                print 'Parsing page number:' + str(num_page) + ' for ' + sub
                new_urls = get_all_urls_from_page(url_to_parse)
                nb_urls +=len(new_urls)
                file.writelines(new_urls)
            except Exception,e:
                print "Error!! -- " + str(e)
                file.writelines(new_urls)
            time.sleep(2)

def get_nb_links_sub(s): # RETURNS THE NUMBER OF URLS WE ALREADY HAVE FOR A SUBDOMAIN
    sub = s.split('|')[0]
    file_path = 'alexa_urls/www.alexa.com' + sub.replace('/','+') + '.txt'
    file = open(file_path, 'r')
    list_urls = file.readlines()
    file.close()
    nb_urls = len(list_urls)
    return nb_urls


def resort_all_subs(): # SORT THE SUBDOMAINS DEPENDING ON COMPLETION
    todo_subs_file = 'alexa_subs_to_do.txt'
    subs_file = 'alexa_subs.txt'
    completed_subs_file = 'alexa_subs_completed.txt'
    #subs_file = 'alexa_subs_test_biatch.txt'
    #todo_subs_file = 'alexa_subs_to_do_test_biatch.txt'
    #completed_subs_file = 'alexa_subs_completed_test_biatch.txt'
    
    with open(subs_file) as all_subs:
        todo_subs = ""
        completed_subs = ""
        for s in all_subs:
            nb = int(s.split('|')[1])
            nb_urls = get_nb_links_sub(s)
            if nb_urls >= nb:
                completed_subs += s
            else: 
                todo_subs += s
        completed_output = open(completed_subs_file, 'w')
        completed_output.write(completed_subs)
        time.sleep(2)
        todo_output = open(todo_subs_file,'w')
        todo_output.write(todo_subs)
        time.sleep(2)


def get_all_valid_subs_of_page(f,cat): #RECURSIVE FUNCTION TO GET A LIST OF SCRAPABLE SUBS (NUMBER OF URLS <525), GOES A STEP FURTHER IN THE BRANCHES IF CONDITION NOT RESPECTED
    print cat
    soup = soup_url('http://www.alexa.com' + cat)
    try :
        links_table = soup.body.find("div", {"class" : "categories row-fluid "}) # HTML list of all the subdomains for this category, separated in columns
        try:
            columns_of_subs = links_table.findAll('ul',{'class' : 'subcategories span3'}) # List of all the columns (case multiple columns)
        except:
            columns_of_subs = list()
            columns_of_subs.append(links_tables.find('ul',{'class' : 'subcategories span3'})) # Name of the column (case unique column)
        for col_sub in columns_of_subs:     #Search for each column
            for row in col_sub.findAll('li'): #Make list of links
                link = row.a.get("href").encode('utf-8') #Get the link of the sub
                nb = int(row.find('span',{"class":"small gray"}).string.replace(',','').encode('utf-8').strip('( )')) # get the number of urls for this sub
                if nb > 500: #if more than 500 urls (not parsable), go one step deeper
                    get_all_valid_subs_of_page(f,link) #Explore the sub and look if reduced enough
                else:
                    pseudo_link = link + '|' + str(nb) +'\n' # Format to write in the file -> link|nb_of_urls
                    f.write(pseudo_link)
                    file_path = 'alexa_urls/www.alexa.com' + link.replace('/','+',15) + '.txt' # Establish the name of the file according to the path
                    if not os.path.isfile(file_path): #If file doesnt already exist, create a blank one
                        open(file_path,'w').close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def soup_url(url):
    return BeautifulSoup(urllib2.urlopen(url).read())