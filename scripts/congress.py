import urllib, json
import locale
import os, ssl
import collections
import datetime
import schedule
import time


candidate_1 = 'WALLACE'
candidate_2 = 'FITZPATRICK'
race_id = '1st'


def add_commas(number):
    "puts commas in a number"
    array = []
    for integer, comma in enumerate(reversed(str(number))):
        if integer and (not (integer % 3)):
            array.insert(0, ',')
        array.insert(0, comma)
    return ''.join(array)

# ===========UPDATE this each year=========================
url = "https://www.electionreturns.pa.gov/api/ElectionReturn/GetOfficeData?officeId=11&methodName=GetOfficeDetails&electionid=undefined&electiontype=undefined&isactive=undefined"

def combine_party(names, parties):
    "Concatenates party at end of names"
    result = []
    for name, party in zip(names,parties):
        s = name + " (" + party[0] + ")"
        result.append(s)
    return result

def parse_raw_json(string):
    "parses json for specific race"
    response = urllib.urlopen(url)
    rdata = json.loads(response.read())
    parsedata = json.loads(rdata)['Election']['Representative in Congress'][0][string][0]
    rdata = json.dumps(parsedata)
    return rdata

def get_district_data(district):
    "Creates Pattern for Searching"
    districtchange = district + 72

    suffix = add_suffix(district)
   
    lookupstring = '{0}{2} Legislative District$${1}$$'.format(str(district), str(districtchange), suffix)
    print lookupstring
    rdata = parse_raw_json(lookupstring)
    return rdata

def remove_first_name(candidates):
    "removes first name from string"
    seperator = ','
    shortname =[]
    for candidate in candidates:    
        shortname.append(candidate.split(seperator, 1)[0])
    return shortname

def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # return value ignored
    return results

json_repr = '{"P1": "ss", "Id": 1234, "P2": {"P1": "cccc"}, "P3": [{"P1": "aaa"}]}'

# def convert(dictionary, name):
#     return namedtuple(name, dictionary.keys())(**dictionary)

def add_suffix(district_num):
    "Adds proper suffix to district numbers"
    districtcompare = district_num % 10
    if districtcompare == 2:
        th = 'nd'
    elif districtcompare == 3:
        th = 'rd'
    elif districtcompare == 1:
        th = 'st'
    elif district_num == 11 or district_num == 12 or district_num == 13:
        th = 'th'
    else:
        th = 'th'
    return th

def print_candidates(items, filenames, name):
    "Saves out Text files for files"
    for item, filename in zip(items,filenames): #save out votes
        with open(name+filename, 'w') as output:
            output.write(item)

def print_votes(items, filenames, name):
    "Saves out Text files for files"
    for item, filename in zip(items,filenames): #save out votes
        with open(name+filename, 'w') as output:
            output.write(add_commas(item))

def print_item(item, filename):
    "Saves out single items as text files"
    file = open(filename, "w") 
    file.write(item)
    file.close()


def create_data2(parsedJSON, race_id, candidate_1, candidate_2, candidate_1_name, candidate_2_name):
    "creates dictionary files"
    Canidates = find_values('CandidateName', parsedJSON) #search terms from JSON
    Votes = find_values('Votes', parsedJSON)
    Percentages = find_values('Percentage', parsedJSON)
    Party = find_values('PartyName', parsedJSON)

    Votes = [int(x) for x in Votes[0:]] #convert votes to Int for comparison
    Canidates = remove_first_name(Canidates)

    # ============Builds dictionary===============
    vote = dict(zip(Canidates, Votes,))
    perc = dict(zip(Canidates, Percentages,))
    my_party = dict(zip(Canidates, Party,))

    # ============Sorting ===============
    Cand = collections.namedtuple('Cand', 'vote name')
    best = sorted([Cand(v,k) for (k,v) in vote.items()], reverse=True)#sorts by highest number

    first = best[0]
    second = best[1]

    # =========================img links =================================================
    first_img ='##"N:\Election_Results\candpictures\c2018fall\congress\{0}\{1}.png" '.format(race_id,str(first.name))
    second_img ='##"N:\Election_Results\candpictures\c2018fall\congress\{0}\{1}.png" '.format(race_id,str(second.name))

    # ============================Building sorted Lists========================
    names = { candidate_1: candidate_1_name, candidate_2 : candidate_2_name }# update for naming
    ordered_votes = [vote[str(first.name)], vote[str(second.name)] ]
    ordered_percentage = [perc[str(first.name)], perc[str(second.name)]  ]
    ordered_picture = [first_img, second_img ]
    ordered_names = [names[str(first.name)], names[str(second.name)]  ]
    ordered_file_names = ['01.txt', '02.txt']
    short_name_print = [first.name, second.name ]
    ordered_party_name = [my_party[str(first.name)], my_party[str(second.name)]]

    race_num= race_id[:-2]
    suffix = race_id[-2:]

    ordered_names = combine_party(ordered_names, ordered_party_name)
    short_name_print = combine_party(short_name_print, ordered_party_name)



    map_color = '##"N:\Election_Results\candpictures\map\{0}_{1}.png" '.format(race_id, my_party[str(first.name)])
    

    #===============================Update number for each race=====================================
    crawl = "RACE FOR PA U.S. {6} CONGRESSIONAL DISTRICT:  {0}({1}) {2}, {3}({4}) {5}    ".format(first.name, my_party[str(first.name)],  add_commas(first.vote), second.name, my_party[str(second.name)], add_commas(second.vote), race_id  )


    save_directory = 'N:\Election_Results\pythonbackup\2018FallElection\congress'
    # =====================Write Text files==========================
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\congress') #changes directory to N drive 

    print_votes(ordered_votes, ordered_file_names, race_id +'_votes')
    print_candidates(ordered_percentage, ordered_file_names, race_id +'_percentage')
    print_candidates(ordered_picture, ordered_file_names, race_id +'_picture')
    print_candidates(ordered_names, ordered_file_names, race_id +'_name')
    print_candidates(short_name_print, ordered_file_names, race_id +'_shor-name')
    print_candidates(ordered_party_name, ordered_file_names, race_id +'_party')

    print_item(suffix, race_id+"_suffix.txt")
    print_item(race_num, race_id+"_suffixNum.txt")

    print_item(map_color, race_id+"_map.txt")


    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\crawl') #Change to crawl

    print_item(crawl, race_id+"_crawl.txt")

    # crawl_filename = race_id + "_crawl.txt"
    # file = open(crawl_filename, "w") #Save out text for crawl
    # file.write(crawl)
    # file.close()

    os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory

    print "US "+ race_id + " UPDATED First Place is " + str(first.name) + " Votes " + str(first.vote) ,datetime.datetime.time(datetime.datetime.now())
#### UPDATE DATA3
def create_data3(parsedJSON, race_id, candidate_1, candidate_2, candidate_3, candidate_1_name, candidate_2_name, candidate_3_name):
    "creates dictionary files"
    Canidates = find_values('CandidateName', parsedJSON) #search terms from JSON
    Votes = find_values('Votes', parsedJSON)
    Percentages = find_values('Percentage', parsedJSON)
    Party = find_values('PartyName', parsedJSON)

    Votes = [int(x) for x in Votes[0:]] #convert votes to Int for comparison
    Canidates = remove_first_name(Canidates)

    # ============Builds dictionary===============
    vote = dict(zip(Canidates, Votes,))
    perc = dict(zip(Canidates, Percentages,))
    my_party = dict(zip(Canidates, Party,))

    # ============Sorting ===============
    Cand = collections.namedtuple('Cand', 'vote name')
    best = sorted([Cand(v,k) for (k,v) in vote.items()], reverse=True)#sorts by highest number

    first = best[0]
    second = best[1]
    third = best[2]

    # =========================img links =================================================
    first_img ='##"N:\Election_Results\candpictures\c2018fall\congress\{0}\{1}.png" '.format(race_id,str(first.name))
    second_img ='##"N:\Election_Results\candpictures\c2018fall\congress\{0}\{1}.png" '.format(race_id,str(second.name))
    third_img ='##"N:\Election_Results\candpictures\c2018fall\congress\{0}\{1}.png" '.format(race_id,str(third.name))

    # ============================Building sorted Lists========================
    names = { candidate_1: candidate_1_name, candidate_2 : candidate_2_name, candidate_3 : candidate_3_name }# update for naming
    ordered_votes = [vote[str(first.name)], vote[str(second.name)], vote[str(third.name)] ]
    ordered_percentage = [perc[str(first.name)], perc[str(second.name)], perc[str(third.name)]  ]
    ordered_picture = [first_img, second_img, third_img ]
    ordered_names = [names[str(first.name)], names[str(second.name)], names[str(third.name)]  ]
    ordered_file_names = ['01.txt', '02.txt', '03.txt']
    short_name_print = [first.name, second.name, third.name ]
    ordered_party_name = [my_party[str(first.name)], my_party[str(second.name)], my_party[str(third.name)]]

    race_num= race_id[:-2]
    suffix = race_id[-2:]
    
    ordered_names = combine_party(ordered_names, ordered_party_name)
    short_name_print = combine_party(short_name_print, ordered_party_name)

    #===============================Update number for each race=====================================
    crawl = "RACE FOR PA U.S. {6} CONGRESSIONAL DISTRICT:  {0}({1}) {2}, {3}({4}) {5}, {7}({8}) {9}    ".format(first.name, my_party[str(first.name)],  add_commas(first.vote), second.name, my_party[str(second.name)], add_commas(second.vote), race_id, third.name, my_party[str(third.name)], add_commas(third.vote)  )


    save_directory = 'N:\Election_Results\pythonbackup\2018FallElection\congress' 
    # =====================Write Text files==========================
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\congress') #changes directory to N drive 

    print_votes(ordered_votes, ordered_file_names, race_id +'_votes')
    print_candidates(ordered_percentage, ordered_file_names, race_id +'_percentage')
    print_candidates(ordered_names, ordered_file_names, race_id +'_name')
    print_candidates(ordered_picture, ordered_file_names, race_id +'_picture')
    print_candidates(short_name_print, ordered_file_names, race_id +'_shor-name')
    print_candidates(ordered_party_name, ordered_file_names, race_id +'_party')

    print_item(suffix, race_id+"_suffix.txt")
    print_item(race_num, race_id+"_suffixNum.txt")

    print_item(crawl, race_id+"_crawl.txt")


    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\crawl') #Change to crawl

    print_item(crawl, race_id+"_crawl.txt")

    os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory

    print "US "+ race_id + " UPDATED First Place is " + str(first.name) + " Votes " + str(first.vote) ,datetime.datetime.time(datetime.datetime.now())

# ================Select races========================#
dist1 = parse_raw_json('1st Congressional District$$2$$')
dist2 = parse_raw_json('2nd Congressional District$$3$$')
dist3 = parse_raw_json('3rd Congressional District$$4$$')
dist4 = parse_raw_json('4th Congressional District$$5$$')
dist5 = parse_raw_json('5th Congressional District$$6$$')
dist6 = parse_raw_json('6th Congressional District$$7$$')
dist7 = parse_raw_json('7th Congressional District$$8$$')
dist8 = parse_raw_json('8th Congressional District$$9$$')
dist9 = parse_raw_json('9th Congressional District$$10$$')
dist10 = parse_raw_json('10th Congressional District$$11$$')
dist11 = parse_raw_json('11th Congressional District$$12$$')
dist12 = parse_raw_json('12th Congressional District$$13$$')
dist13 = parse_raw_json('13th Congressional District$$14$$')
dist14 = parse_raw_json('14th Congressional District$$15$$')
dist15 = parse_raw_json('15th Congressional District$$16$$')
dist16 = parse_raw_json('16th Congressional District$$17$$')
dist17 = parse_raw_json('17th Congressional District$$18$$')


create_data2(dist1, race_id, candidate_1, candidate_2, 'Scott Wallace', 'Brian Fitzpatrick' )
create_data2(dist2, '2nd', 'BOYLE', 'TORRES', 'Brendan Boyle', 'David Torres' )
create_data2(dist3, '3rd', 'EVANS', 'LEIB', 'Dwight Evans', 'Bryan Leib' )
create_data2(dist4, '4th', 'DEAN CUNNANE ', 'DAVID', 'Madeleine Dean', 'Daniel David' )
create_data2(dist5, '5th', 'SCANLON', 'KIM', 'Mary Gay Scanlon', 'Pearl Kim' )
create_data2(dist6, '6th', 'HOULAHAN', 'MCCAULEY', 'Christina Houlahan', 'Greg McCauley' )
create_data3(dist7, '7th', 'WILD', 'NOTHSTEIN', 'SILFIES', 'Susan Wild', 'Marty Nothstein', 'Tim Silfies' )
create_data2(dist8, '8th', 'CARTWRIGHT', 'CHRIN', 'Matt Cartwright', 'John Chrin' )
create_data2(dist9, '9th', 'WOLFF', 'MEUSER', 'Denny Wolff', 'Dan Meuser' )
create_data2(dist10, '10th', 'SCOTT', 'PERRY', 'George Scott', 'Scott Perry' )
create_data2(dist11, '11th', 'KING', 'SMUCKER', 'Jess King', 'Lloyd Smucker' )
create_data2(dist12, '12th', 'FRIEDENBERG', 'MARINO', 'Marc Friedenberg', 'Tom Marino' )
create_data2(dist13, '13th', 'OTTAWAY', 'JOYCE', 'Brent Ottaway', 'John Joyce' )
create_data2(dist14, '14th', 'BOERIO', 'RESCHENTHALER', 'Bibiana Boerio', 'Guy Reschenthaler' )
create_data2(dist15, '15th', 'BOSER', 'THOMPSON', 'Susan Boser', 'Glenn Thompson' )
create_data3(dist16, '16th', 'DINICOLA', 'KELLY', 'BEEMAN', 'Ronald DiNicola', 'Mike Kelly', 'Ebert Beeman' )
create_data2(dist17, '17th', 'LAMB', 'ROTHFUS', 'Conor Lamb', 'Keith Rothfus' )





# # ==============PARSING JSON===================
# Canidates = find_values('CandidateName', rdata) #search terms from JSON
# Votes = find_values('Votes', rdata)
# Percentages = find_values('Percentage', rdata)
# Party = find_values('PartyName', rdata)

# Votes = [int(x) for x in Votes[0:]] #convert votes to Int for comparison
# Canidates = remove_first_name(Canidates)


# # ============Builds dictionary===============
# my_votes = dict(zip(Canidates, Votes,))
# my_percentage = dict(zip(Canidates, Percentages,))

# # from collections import namedtuple #converts dictionary to named tuple
# # def convert(dictionary, name):
# #     return namedtuple(name, dictionary.keys())(**dictionary)


# # ==========================UPDATE THIS FOR FILTERING======================================
# vote = dict((key,my_votes[key]) for key in (candidate_1,candidate_2) if key in my_votes) # create sub dictionary
# perc = dict((key,my_percentage[key]) for key in (candidate_1,candidate_2) if key in my_percentage)#creates perc subdirectory


# # ==========USE For TESTING ==========
# # vote ['CLARK'] = 9990
# # rep_gov_vote ['ELLSWORTH'] = 1999
# # rep_gov_vote ['WAGNER'] = 23989


# # ===================SORTING=========================================
# Cand = collections.namedtuple('Cand', 'vote name')
# best = sorted([Cand(v,k) for (k,v) in vote.items()], reverse=True)#sorts by highest number

# first = best[0]
# second = best[1]

# # =========================img links =================================================
# first_img ='##"N:\Election_Results\candpictures\2018fall\{0}\{1}.png" '.format(race_id,str(first.name))
# second_img ='##"N:\Election_Results\candpictures\2018fall\{0}\{1}.png" '.format(race_id,str(second.name))


# # ============================Building sorted Lists========================
# ordered_votes = [vote[str(first.name)], vote[str(second.name)] ]
# ordered_percentage = [perc[str(first.name)], perc[str(second.name)]  ]
# ordered_picture = [first_img, second_img ]
# ordered_names = [names[str(first.name)], names[str(second.name)]  ]
# ordered_file_names = ['01.txt', '02.txt']
# short_name_print = [first.name, second.name ]
# ordered_party_name = [party[str(first.name)], party[str(second.name)]]


# #===============================Update number for each race=====================================
# crawl = "RACE FOR PA U.S. {6} CONGRESSIONAL DISTRICT:  {0}({1}) {2}, {3}({4}) {5}    ".format(first.name, party[str(first.name)],  add_commas(first.vote), second.name, party[str(second.name)], add_commas(second.vote), race_id  )


# save_directory = 'N:\Election_Results\pythonbackup\2018FallElection\text\' + race_id'  
# # =====================Write Text files==========================
# # os.chdir (r'save_directory') #changes directory to N drive 

# for item, filename in zip(ordered_votes,ordered_file_names): #save out votes
#      with open('votes'+filename, 'w') as output:
#          output.write(add_commas(item))

# for item, filename in zip(ordered_percentage,ordered_file_names): #save out percentage
#      with open('percentage'+filename, 'w') as output:
#          output.write(item)

# for item, filename in zip(ordered_picture,ordered_file_names): #save out picture link
#      with open('picture'+filename, 'w') as output:
#          output.write(item)

# for item, filename in zip(ordered_names,ordered_file_names): #save out name
#      with open('name'+filename, 'w') as output:
#          output.write(item)

# for item, filename in zip(short_name_print,ordered_file_names): #save out name
#      with open('shor-name'+filename, 'w') as output:
#          output.write(item)

# for item, filename in zip(ordered_party_name, ordered_file_names): #save out name
#      with open('party'+filename, 'w') as output:
#          output.write(item)



# os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\text\crawl') #Change to crawl

# crawl_filename = race_id + "_crawl.txt"
# file = open(crawl_filename, "w") #Save out text for crawl
# file.write(crawl)
# file.close()



# os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory


# =============Return to see if it is working==================


# print "US "+ race_id + " UPDATED First Place is " + str(first.name) + " Votes " + str(first.vote) ,datetime.datetime.time(datetime.datetime.now())






