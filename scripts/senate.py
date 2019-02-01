
import urllib, json
import locale
import schedule
import time


#fixes ssl warning
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context



def add_commas(number):#puts commas in number
    array = []
    for integer, comma in enumerate(reversed(str(number))):
        if integer and (not (integer % 3)):
            array.insert(0, ',')
        array.insert(0, comma)
    return ''.join(array)

# ===========UPDATE this each year=========================
url = "https://www.electionreturns.pa.gov/api/ElectionReturn/GetOfficeData?officeId=2&methodName=GetOfficeDetails&electionid=undefined&electiontype=undefined&isactive=undefined"

# def job():
response = urllib.urlopen(url)
rdata = json.loads(response.read())#loads json to library

def combine_party(names, parties):
    "Concatenates party at end of names"
    result = []
    for name, party in zip(names,parties):
        s = name + " (" + party[0] + ")"
        result.append(s)
    return result

def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # return value ignored
    return results


json_repr = '{"P1": "ss", "Id": 1234, "P2": {"P1": "cccc"}, "P3": [{"P1": "aaa"}]}'



# ==============PARSING JSON===================
Canidates = find_values('CandidateName', rdata) #search terms from JSON
Votes = find_values('Votes', rdata)
Percentages = find_values('Percentage', rdata)
Party = find_values('PartyName', rdata)

Votes = [int(x) for x in Votes[0:]] #convert votes to Int for comparison


# ============Parses Name to remove first name===========
sep = ','
shortname =[]
for Ca in Canidates:    
    shortname.append(Ca.split(sep, 1)[0])


# ============Builds dictionary===============
my_votes = dict(zip(shortname, Votes,))
my_percentage = dict(zip(shortname, Percentages,))

from collections import namedtuple #converts dictionary to named tuple
def convert(dictionary, name):
    return namedtuple(name, dictionary.keys())(**dictionary)


# ==========================UPDATE THIS FOR FILTERING======================================
vote = dict((key,my_votes[key]) for key in ('CASEY','BARLETTA', 'GALE', 'KERNS') if key in my_votes) # create sub dictionary
perc = dict((key,my_percentage[key]) for key in ('CASEY','BARLETTA', 'GALE', 'KERNS') if key in my_percentage)#creates perc subdirectory
names = {'CASEY': 'Bob Casey', 'BARLETTA' : 'Lou Barletta', 'GALE': 'Neal Taylor Gale', 'KERNS': 'Dale Kerns'  }# update for naming
party = {'CASEY': 'DEM', 'BARLETTA' : 'REP','GALE' : 'GRN', 'KERNS' : 'LIB'}

# ==========USE For TESTING ==========
# dem_vote ['CLARK'] = 9990
# rep_vote ['ELLSWORTH'] = 1999
# rep_vote ['WAGNER'] = 23989


# ===================SORTING=========================================
import collections
Cand = collections.namedtuple('Cand', 'vote name')

best = sorted([Cand(v,k) for (k,v) in vote.items()], reverse=True)#sorts by highest number


first = best[0]
second = best[1]
third = best[2]
fourth = best[3]

# =========================img links =================================================
first_img ='##"N:\Election_Results\candpictures\{0}\{1}.png" '.format('2018fall\Senate',str(first.name))
second_img ='##"N:\Election_Results\candpictures\{0}\{1}.png" '.format('2018fall\Senate',str(second.name))
third_img ='##"N:\Election_Results\candpictures\{0}\{1}.png" '.format('2018fall\Senate',str(third.name))
fourth_img ='##"N:\Election_Results\candpictures\{0}\{1}.png" '.format('2018fall\Senate',str(fourth.name))

# ============================Building sorted Lists========================

ordered_votes = [vote[str(first.name)], vote[str(second.name)], vote[str(third.name)], vote[str(fourth.name)]  ]
ordered_percentage = [perc[str(first.name)], perc[str(second.name)], perc[str(third.name)], perc[str(fourth.name)]  ]
ordered_picture = [first_img, second_img, third_img, fourth_img]
ordered_names = [names[str(first.name)], names[str(second.name)], names[str(third.name)], names[str(fourth.name)] ]
ordered_file_names = ['01.txt', '02.txt', '03.txt', '04.txt']
short_name_print = [first.name, second.name, third.name, fourth.name]
ordered_party_name = [party[str(first.name)], party[str(second.name)], party[str(third.name)], party[str(fourth.name)]]

ordered_names = combine_party(ordered_names, ordered_party_name)
short_name_print = combine_party(short_name_print, ordered_party_name)


#===============================Update number for each race=====================================

crawl = "RACE FOR PA U.S. SENATOR:  {0}({1}) {2},  {3}({4}) {5}, {6}({7}) {8}, {9}({10}) {11}     ".format(first.name, party[str(first.name)],  add_commas(first.vote), second.name, party[str(second.name)], add_commas(second.vote), third.name, party[str(third.name)], add_commas(third.vote), fourth.name, party[str(fourth.name)], add_commas(fourth.vote)  )


    
# =====================Write Text files==========================
os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\senate') #changes directory to N drive 


for item, filename in zip(ordered_votes,ordered_file_names): #save out votes
        with open('votes'+filename, 'w') as output:
            output.write(add_commas(item))

for item, filename in zip(ordered_percentage,ordered_file_names): #save out percentage
        with open('percentage'+filename, 'w') as output:
            output.write(item)

for item, filename in zip(ordered_picture,ordered_file_names): #save out picture link
        with open('picture'+filename, 'w') as output:
            output.write(item)

for item, filename in zip(ordered_names,ordered_file_names): #save out name
        with open('name'+filename, 'w') as output:
            output.write(item)

for item, filename in zip(short_name_print,ordered_file_names): #save out name
        with open('shor-name'+filename, 'w') as output:
            output.write(item)

for item, filename in zip(ordered_party_name, ordered_file_names): #save out name
        with open('party'+filename, 'w') as output:
            output.write(item)

os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\crawl') #Change to crawl

    
file = open("us-senate.txt", "w") #Save out text for crawl
file.write(crawl)
file.close()

os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory


# =============Return to see if it is working==================

import datetime
print "US SENATOR UPDATED First Place is " + str(first.name) + " Votes " + str(first.vote) ,datetime.datetime.time(datetime.datetime.now())


# schedule.every(10).seconds.do(job)


# while True:
#     schedule.run_pending()
#     time.sleep(1)




