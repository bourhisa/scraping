from datetime import time
from pymongo import MongoClient
import schema_helpers
from time import sleep
import urllib2,json,itertools, os, collections, random, time
# from pysitemap import Sitemap
import re 

def main():

    gathering_alexa = False
    gathering_thuiswinkel = False
    step_1 = False # GLOBAL GATHERING
    step_2 = True # TESTING FOR SCHEMA.ORG
    counting = False

    
    client = MongoClient()
    db = client.Fastr

    global folders, steps, dict_all, dict_pos, dict_parsed
    folders = schema_helpers.set_folders()
    steps = ['detect_schema', 'begin_exploration', 'get_links', 'get_still_to_parse', 'get_interesting_url']
    dict_all = schema_helpers.get_dict(folders['all_urls']['json'])
    dict_pos = schema_helpers.get_dict(folders['parsed']['positive'])
    dict_parsed = schema_helpers.get_dict(folders['parsed']['parsed'])

    if gathering_alexa:
        schema_helpers.gather_alexa(folders)

    if gathering_thuiswinkel:
        schema_helpers.gather_thuiswinkel(folders)

    if step_1:
        total_json = []
        json_completed = dict()
        completed_subs_file = folders['dir']["alexa"] + "alexa_subs_completed.txt"
        list_keys_completed = sorted(schema_helpers.get_all_completed_subs(completed_subs_file))
        print str(len(list_keys_completed)) + " completed subdomains"
        nb_total_urls = 0
        for json_index in folders['lists_urls']['json']:  ############### FOR EACH JSON FILE (alexa & thuiswinkel), CHECK BY KEY IF COMPLETED, AND ADD TO DICT
            file = folders['lists_urls']['json'][json_index]
            f = open(file)
            data = json.load(f)
            list_completed = ''.join(list_keys_completed)
            for key in sorted(data.keys()):
                if key in list_completed.decode('utf-8'):
                    try:
                        stack = [x.encode('utf-8') for x in data[key][:-1]]
                        nb = len(stack)
                        nb_total_urls += nb
                        json_completed[key] = sorted(stack)
                    except Exception,e:
                        print e
        json_urls = open(folders['all_urls']['json'] ,'w') 
        json_completed_sorted = collections.OrderedDict(sorted(json_completed.items()))
        json.dump(json_completed_sorted, json_urls,indent=2)
        print "We have " + str(nb_total_urls) + " from completed subdomains"
        sleep(3)

        # UNSORTED LIST
        total_list = []
        for list_index in folders['lists_urls']['list']:
            f = open(folders['lists_urls']['list'][list_index]).read()
            total_list += f.split('\n')

        lst = sorted(total_list)
        i = len(lst) - 1
        while i > 0:  # Get rid of doubles
            if lst[i] == lst[i - 1]:
                lst.pop(i)
            i -= 1

        final_list = []
        for x in lst:
            if '\x00' not in x and x != '':
                final_list.append(x + '\n')
        all_urls = open(folders['all_urls']['list'],'w')
        all_urls.write(''.join(final_list))
        sleep(2)

    if step_2:
        keys = sorted(dict_all.keys())
        for key in keys:
            o = schema_helpers.SubDomain(key)
            if len(o.list_to_parse) != 0:
                print "Looking for: " + key, 'Parsed: ' + str(len(o.list_parsed)) + ", to parse: ", len(o.list_to_parse), ", positives: ", len(o.list_positive)
                o.build_list_positive()


    # COUNTING

    if counting:

        count_alexa = sum(len(i) for i in schema_helpers.get_dict(folders['lists_urls']['json']['alexa']).values())
        total_alexa = sum(int(li.split('|')[1]) for li in open(folders['dir']['alexa'] + "alexa_subs.txt").read().split('\n'))

        count_thuiswinkel = sum(len(i) for i in schema_helpers.get_dict(folders['lists_urls']['json']['thuiswinkel']).values())

        total_distinct = len((open(folders['all_urls']['list']).read()).split('\n'))
        total_count = count_alexa + count_thuiswinkel

        count_tested = sum(len(i) for i in schema_helpers.get_dict(folders['parsed']['parsed']).values())
        count_positive = sum(len(i) for i in schema_helpers.get_dict(folders['parsed']['positive']).values())

        
        print "Scraped for Alexa: {} out of {} ({}%)".format(count_alexa, total_alexa, (float(count_alexa)/float(total_alexa))*100)
        print "Scraped for Thuiswinkel: {}(100%)".format(count_thuiswinkel)
        print "Total scraped: {} urls ({} distinct) out of {} ({}%)".format(total_count, total_distinct, total_alexa + count_thuiswinkel, (float(total_count)/float(total_alexa+count_thuiswinkel))*100)
        print "Number of positive URLs for schema.org: {} out of {}, ({}%)".format(count_positive, count_tested, (float(count_positive)/float(count_tested))*100)



    # url = "https://www.bol.com/nl/index.html"
    #
    # global time_records
    # time_records = map(list, [[]] * len(steps))
    # start = time.time()
    # print schema_helpers.track_positive(url, url, [], [], False)
    # print_time_stats(start)





if __name__ == "__main__":
    main()
