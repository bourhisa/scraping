import os
from BeautifulSoup import BeautifulSoup
import urllib2,json,itertools, os, collections, random
from time import sleep
import signal
import re
import time

def set_folders():
    global folders
    folders = dict()
    folders['dir'] = {'thuiswinkel': 'C:/Fastr/Fastr_scraping/thuiswinkel/thuiswinkel_scraping/', 'alexa': "C:/Fastr/Fastr_scraping/alexa/"}
    folders['lists_urls'] = {'list': {'alexa': 'alexa_urls_list.txt', 'thuiswinkel': "thuiswinkel_urls_list.txt"},
                             'json': {'alexa': 'alexa_urls_json.txt', 'thuiswinkel': "thuiswinkel_urls_json.txt"}}
    folders['subs'] = {'completed': folders['dir']['alexa'] + "alexa_subs_completed.txt",
                       'todo': folders['dir']['alexa'] + "alexa_subs_todo.txt"}
    folders['all_urls'] = {"json": "all_urls_json.txt", "list": "all_urls_list.txt"}
    folders['parsed'] = {'positive': 'positive_urls.txt', 'parsed': 'all_parsed.txt'}
    return folders

def get_dict(filename):
    try:
        t = json.load(open(filename))
    except Exception, (e):
        t = dict()
        print filename, e
    return t

def get_all_completed_subs(completed_subs_file):
    list_keys_completed = ["https://www.thuiswinkel.org/ledenlijst/"] ######## BY HAND FOR THUISWINKEL SINCE ONLY ONE SUB
    with open(completed_subs_file) as completed_subs: ########## GET LIST OF ALL COMPLETED SUBDOMAINS FOR ALEXA
        for s in completed_subs:
            sub = s.replace('+','/',15).replace('\n','')
            json_key = 'www.alexa.com' + sub
            list_keys_completed.append(json_key)
    return list_keys_completed

#def count_urls_of_folder(folders):
#    dir = folders['dir']['alexa']
#    count_alexa = 0
#    all_subs = open(dir + "alexa_subs.txt",'r').read().split('\n')
#    for s in all_subs:
#        nb_theoric = int(s.split('|')[1])
#        filename = s.split('|')[0].replace('/','+') + '.txt'
#        with open(dir + "alexa_urls/www.alexa.com" + filename) as f:
#            lines = f.read()
#            l = lines.split('\n')
#            nb_real = int(len(l) - 1)
#            if (nb_real - nb_theoric) > .02*nb_theoric:
#                print "Mistake for " + filename + ":" + str(nb_real) + "vs" + str(nb_theoric)
#            count_alexa += nb_real
#            f.close()
#    return count_alexa

def gather_alexa(folders):
    dir = folders['dir']['alexa'] + 'alexa_urls/'
    json_output = open(folders['lists_urls']['json']['alexa'], 'w')
    list_output = open(folders['lists_urls']['list']['alexa'], 'w')
    count_urls = 0
    list_urls = []
    dict_urls = dict()

    for filename in os.listdir(dir):
            with open(dir + filename) as f:
                content = f.read()
                lines = content.split('\n')
                count_urls += len(lines)
                file_path = filename.replace('+','/').replace('.txt','')
                dict_urls[file_path] = lines
                list_urls += content

    d = collections.OrderedDict(sorted(dict_urls.items()))
    json_output.write(json.dumps(d,indent=2))
    list_output.writelines(list_urls)  
    print "We have " + str(count_urls) + " urls for alexa"
    sleep(2)

def gather_thuiswinkel(folders):
    dir = folders['dir']['thuiswinkel'] + "thuiswinkel/"
    json_output = open(folders['lists_urls']['json']['thuiswinkel'],'w')
    list_output = open(folders['lists_urls']['list']['thuiswinkel'],'w')
    list_urls = ""
    dict_urls = dict()
    for filename in os.listdir(dir):
        with open(dir + filename) as f:
            print filename
            list_urls += f.read()
    title = "https://www.thuiswinkel.org/ledenlijst/"
    dict_urls[title] = list_urls.split('\n')
    count_urls = len(dict_urls[title])
    
    d = collections.OrderedDict(sorted(dict_urls.items()))
    json_output.write(json.dumps(d,indent=2))
    list_output.writelines(list_urls)
    print "We have " + str(count_urls) + " urls for thuiswinkel"

#def key_already_parsed(key, folders):
#    already_parsed = open(folders['parsed']['parsed_files'],'r').read()
#    return key in already_parsed

#def refresh_parsed(folders):
#    try:
#        positive_urls = json.load(open(folders['parsed']['positive']))
#        already_parsed_list = positive_urls.keys()
#        print len(already_parsed_list)

#        all_completed = get_all_completed_subs(folders['subs']['completed'])
#        all_completed_string = ''.join(all_completed).decode('utf-8')

#        for i in already_parsed_list:
#            j = i.split('|')[0].replace("www.alexa.com",'').encode('utf-8')
#            if j not in all_completed_string:
#                print "Deleted:" + j + " in parsed_list"
#                already_parsed_list.pop(already_parsed_list.index(i))
#                del positive_urls[i]

#        p = open(folders['parsed']['positive'],'w')
#        ordered = collections.OrderedDict(sorted(positive_urls.items()))
#        p.write(json.dumps(ordered,indent=2))
#        p.close()

#        file_parsed = open(folders['parsed']['parsed_files'],'w')
#        file_parsed.write('\n'.join(sorted(already_parsed_list)))
#        file_parsed.close()
#    except:
#        pass

def update_parsed_list(key, filename):
    file = open(filename,'r')
    already_parsed_list = file.read().split('\n')
    file.close()
    already_parsed_list.append(key)
    file_parsed = open(filename,'w')
    file_parsed.write('\n'.join(sorted(already_parsed_list)))
    file_parsed.close()

#def update_pos_dict(positive_dict, filename):
#    p = open(filename,'w')
#    ordered = collections.OrderedDict(sorted(positive_dict.items()))
#    p.write(json.dumps(ordered,indent=2))
#    p.close()

def update_dict(dict, filename):
    p = open(filename,'w')
    ordered = collections.OrderedDict(sorted(dict.items()))
    p.write(json.dumps(ordered,indent=2))
    p.close()

def track_positive(base_url, current_url, list_links, parsed, interesting):
    #flag = time.time()
    schema = detect_schema(current_url)
    #flag = measure_exec(flag, 0)
    if schema == 2:
        return '|'.join([base_url,current_url])
        exit()

    nb_tries = len(parsed)
    if (interesting and nb_tries < 20) or (nb_tries < 7 ):
        if schema == 1:
            interesting = True

        #flag = measure_exec(flag, 1)
        if len(list_links) < 200:
            list_links += get_page_links(current_url, base_url , list_links)
        #flag = measure_exec(flag, 2)
        still_to_parse = list(set(list_links) - set(parsed))
        #flag = measure_exec(flag, 3)
        y = check_interesting_url(still_to_parse)
        #flag = measure_exec(flag, 4)
        parsed.append(y)
        return track_positive(base_url, y, list_links, parsed, interesting)

    else:
        print "Dropped for " + base_url + " after " + str(len(parsed)) + " links tried "
        return False
        exit()


def get_page_links(url,base_url, list_links): ######### GET ALL URLS LISTED IN A PAGE
    
    if "http" in base_url:
        short_url = base_url.split('/')[2]
        if "www" in short_url:
            short_url = short_url.split('.')[1]
    else:
        short_url = base_url
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        all_links = soup.findAll(['a','link'])
        for l in all_links:
            try:
                link = l['href']
            except Exception, e:
                pass
            if re.match("^\/\S*$", link):
                link = base_url + (link)
                # print "reconstructed link!", link
            if short_url in link:
                list_links.append(link.encode('utf8'))
    except Exception, e:
        # print e , link, base_url, short_url
        pass
    return list_links


def detect_schema(url): #### TEST IF HTML CONTAINS SCHEMA.ORG/PRODUCT
    try:
        html = urllib2.urlopen(url).read()
        if ('schema.org') in html:
            if ('http://schema.org/Product' in html):
                return 2
            else:
                return 1
        else:
            return False
    except:
        return False

def check_interesting_url(to_parse):
    ### ESTABLISH URL MOST LIKELY TO CONTAIN ARTICLES
    tags_strong = ['product', 'article']
    tags_light = ['winkel' , 'shop', 'boutique', 'buy','order']
    for u in to_parse:
        if any(tag in u for tag in tags_light) or re.match('^.*\d{5,12}\D*$', u):
            return u
            exit()
    for u in to_parse:
        if any(tag in u for tag in tags_light):
            return u
            exit()
    if to_parse:
        return random.choice(to_parse)

def print_time_stats(start):
    print time.time() - start
    text = ''
    for i in range(len(steps)):
        try:
            text += steps[i] + ":" + str(len(time_records[i])) + "  " + str(float(sum(time_records[i]))/len(time_records[i])) + "   ----    "
        except:
            pass
    print text

def measure_exec(start, category):
    end = time.time()
    time_records[category].append(end - start)
    return end

class SubDomain():

    def retrieve_positive(self):
        if self.u not in dict_pos.keys():
            dict_pos[self.u] = []
        self.list_positive = sorted(dict_pos[self.u])

    def retrieve_parsed(self):
        if self.u not in dict_parsed.keys():
            dict_parsed[self.u] = []
        self.list_parsed = sorted(dict_parsed[self.u])

    def build_list_positive(self):
        key = self.u

        for url in sorted(self.list_to_parse):
            self.list_to_parse = sorted(list(set(self.list_total) - set(self.list_parsed)))
            if len(self.list_parsed) == len(self.list_total):
                print 'Over for ' + self.u
                date_dict(dict_pos, folders['parsed']['positive'])
                update_dict(dict_parsed, folders['parsed']['parsed'])
                break
            else:
                global time_records

                time_records = map(list, [[]] * len(steps))
                start = time.time()
                result = track_positive(url, url, [], [], False)
                #print_time_stats(start)

                dict_parsed[key].append(url)
                dict_parsed[key] = sorted(dict_parsed[key])

                if result:
                    print '+++++++++++ Positive for ' + result + '  ' + str(len(self.list_positive))
                    self.list_positive.append(result)
                    dict_pos[key] = sorted(list(set(dict_pos[key] + self.list_positive)))
                    update_dict(dict_pos, folders['parsed']['positive'])
                update_dict(dict_parsed, folders['parsed']['parsed'])


    def __init__(self, url):

        global folders, steps, dict_all, dict_pos, dict_parsed
        folders = set_folders()
        steps = ['detect_schema', 'begin_exploration', 'get_links', 'get_still_to_parse', 'get_interesting_url']
        dict_all = get_dict(folders['all_urls']['json'])
        dict_pos = get_dict(folders['parsed']['positive'])
        dict_parsed = get_dict(folders['parsed']['parsed'])

        self.u = url
        self.list_total = dict_all[self.u]
        self.retrieve_parsed()
        self.retrieve_positive()
        self.list_to_parse = sorted(list(set(self.list_total) - set(self.list_parsed)))