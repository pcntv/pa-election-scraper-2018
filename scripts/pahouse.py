import urllib, json
import locale
import os, ssl
import collections
import datetime
import schedule
import time



def add_commas(number):
    "puts commas in a number"
    array = []
    for integer, comma in enumerate(reversed(str(number))):
        if integer and (not (integer % 3)):
            array.insert(0, ',')
        array.insert(0, comma)
    return ''.join(array)

# ===========UPDATE this each year=========================
url = "https://www.electionreturns.pa.gov/api/ElectionReturn/GetOfficeData?officeId=13&methodName=GetOfficeDetails&electionid=undefined&electiontype=undefined&isactive=undefined"

def combine_party(names, parties):
    "Concatenates party at end of names"
    result = []
    for name, party in zip(names,parties):
        s = name + " (" + party[0] + ")"
        result.append(s)
    return result

def add_suffix(district_num):
    "Adds proper suffix to district numbers"
    districtcompare = district_num % 10
    if district_num == 11 or district_num == 12 or district_num == 13 or district_num == 111 or district_num == 112 or district_num == 113:
        th = 'th'
    elif districtcompare == 2:
        th = 'nd'
    elif districtcompare == 3:
        th = 'rd'
    elif districtcompare == 1:
        th = 'st'
    else:
        th = 'th'
    return th


def parse_raw_json(string):
    "parses json for specific race"
    response = urllib.urlopen(url)
    rdata = json.loads(response.read())
    parsedata = json.loads(rdata)['Election']['Representative in the General Assembly'][0][string][0]
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
    first_img ='##"N:\Election_Results\candpictures\c2018fall\state_house\{0}\{1}.png" '.format(race_id,str(first.name))
    second_img ='##"N:\Election_Results\candpictures\c2018fall\state_house\{0}\{1}.png" '.format(race_id,str(second.name))

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
    
    #===============================Update number for each race=====================================

    #save_directory = 'N:\Election_Results\pythonbackup\2018FallElection\text\' + race_id'  
    # =====================Write Text files==========================
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\state_house') #changes directory to N drive 

    print_votes(ordered_votes, ordered_file_names, race_id +'_votes')
    print_candidates(ordered_percentage, ordered_file_names, race_id +'_percentage')
    print_candidates(ordered_picture, ordered_file_names, race_id +'_picture')
    print_candidates(ordered_names, ordered_file_names, race_id +'_name')
    print_candidates(short_name_print, ordered_file_names, race_id +'_shor-name')
    print_candidates(ordered_party_name, ordered_file_names, race_id +'_party')

    print_item(suffix, race_id+"_suffix.txt")
    print_item(race_num, race_id+"_suffixNum.txt")

    # for item, filename in zip(ordered_votes,ordered_file_names): #save out votes
    #     with open(race_id+'_votes'+filename, 'w') as output:
    #         output.write(add_commas(item))

    # for item, filename in zip(ordered_percentage,ordered_file_names): #save out percentage
    #     with open(race_id+'_percentage'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_picture,ordered_file_names): #save out picture link
    #     with open(race_id+'_picture'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_names,ordered_file_names): #save out name
    #     with open(race_id+'_name'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(short_name_print,ordered_file_names): #save out name
    #     with open(race_id+'_shor-name'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_party_name, ordered_file_names): #save out name
    #     with open(race_id+'_party'+filename, 'w') as output:
    #         output.write(item)
    
    # title_filename = race_id + "_number.txt"
    # file = open(title_filename, "w") 
    # file.write(race_num)
    # file.close()

    # suffix_filename = race_id + "_suffix.txt"
    # file = open(suffix_filename, "w") 
    # file.write(suffix)
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
    first_img ='##"N:\Election_Results\candpictures\2018fall\{0}\{1}.png" '.format(race_id,str(first.name))
    second_img ='##"N:\Election_Results\candpictures\2018fall\{0}\{1}.png" '.format(race_id,str(second.name))
    third_img ='##"N:\Election_Results\candpictures\2018fall\{0}\{1}.png" '.format(race_id,str(third.name))

    # ============================Building sorted Lists========================
    names = { candidate_1: candidate_1_name, candidate_2 : candidate_2_name, candidate_3 : candidate_3_name }# update for naming
    ordered_votes = [vote[str(first.name)], vote[str(second.name)], vote[str(third.name)] ]
    ordered_percentage = [perc[str(first.name)], perc[str(second.name)], perc[str(third.name)]]
    ordered_picture = [first_img, second_img, third_img ]
    ordered_names = [names[str(first.name)], names[str(second.name)], names[str(third.name)]  ]
    ordered_file_names = ['01.txt', '02.txt', '03.txt']
    short_name_print = [first.name, second.name, third.name ]
    ordered_party_name = [my_party[str(first.name)], my_party[str(second.name)], my_party[str(third.name)]]

    race_num= race_id[:-2]
    suffix = race_id[-2:]

    ordered_names = combine_party(ordered_names, ordered_party_name)
    

    #===============================Update number for each race=====================================

    save_directory = 'N:\Election_Results\pythonbackup\2018FallElection\text\' + race_id'  
    # =====================Write Text files==========================
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\state_house') #changes directory to N drive 

    print_votes(ordered_votes, ordered_file_names, race_id +'_votes')
    print_candidates(ordered_percentage, ordered_file_names, race_id +'_percentage')
    print_candidates(ordered_picture, ordered_file_names, race_id +'_picture')
    print_candidates(ordered_names, ordered_file_names, race_id +'_name')
    print_candidates(short_name_print, ordered_file_names, race_id +'_shor-name')
    print_candidates(ordered_party_name, ordered_file_names, race_id +'_party')

    print_item(suffix, race_id+"_suffix.txt")
    print_item(race_num, race_id+"_suffixNum.txt")

    # for item, filename in zip(ordered_votes,ordered_file_names): #save out votes
    #     with open('votes'+filename, 'w') as output:
    #         output.write(add_commas(item))

    # for item, filename in zip(ordered_percentage,ordered_file_names): #save out percentage
    #     with open('percentage'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_picture,ordered_file_names): #save out picture link
    #     with open('picture'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_names,ordered_file_names): #save out name
    #     with open('name'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(short_name_print,ordered_file_names): #save out name
    #     with open('shor-name'+filename, 'w') as output:
    #         output.write(item)

    # for item, filename in zip(ordered_party_name, ordered_file_names): #save out name
    #     with open('party'+filename, 'w') as output:
    #         output.write(item)

    # os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\text\crawl') #Change to crawl

    # crawl_filename = race_id + "_crawl.txt"
    # file = open(crawl_filename, "w") #Save out text for crawl
    # file.write(crawl)
    # file.close()

    os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory

    print "US "+ race_id + " UPDATED First Place is " + str(first.name) + " Votes " + str(first.vote) ,datetime.datetime.time(datetime.datetime.now())

# ================Select races========================#
# sd6 = parse_raw_json('{0}th Senatorial District$${1}$$').format(6, )
# sd10 = parse_raw_json('10th Senatorial District$$32$$')
# sd12 = parse_raw_json('12th Senatorial District$$34$$')
# sd16 = parse_raw_json('16th Senatorial District$$38$$')
# sd24 = parse_raw_json('24th Senatorial District$$46$$')
# sd26 = parse_raw_json('26th Senatorial District$$48$$')
# sd32 = parse_raw_json('32nd Senatorial District$$54$$')
# sd34 = parse_raw_json('34th Senatorial District$$56$$')
# sd38 = parse_raw_json('38th Senatorial District$$60$$')
# sd40 = parse_raw_json('40th Senatorial District$$62$$')
# sd44 = parse_raw_json('44th Senatorial District$$66$$')
# sd46 = parse_raw_json('46th Senatorial District$$68$$')


os.system('get_congress_percentages')
create_data2(get_district_data(170), '170th', 'DOYLE', 'WHITE', 'Mike Doyle', 'Martina White' )
create_data2(get_district_data(160), '160th', 'ANDREW', 'BARRAR', 'Anton Andrew', 'Stephen Barrar' )
create_data2(get_district_data(165), '165th', 'OMARA', 'CHARLTON', 'Jennifer Omara', 'Alex Charlton' )
create_data2(get_district_data(163), '163rd', 'ZABEL', 'SANTORA', 'Mike Zabel', 'Jamie Santora' )
create_data2(get_district_data(158), '158th', 'SAPPEY', 'ROE', 'Christina Sappey', 'Eric Roe' )
create_data2(get_district_data(167), '167th', 'HOWARD', 'MILNE', 'Kristine Howard', 'Duane Milne' )
create_data2(get_district_data(61), '61st', 'HANBIDGE', 'HARPER', 'Liz Hanbidge', 'Kate Harper' )
create_data2(get_district_data(157), '157th', 'SHUSTERMAN', 'KAMPF', 'Melissa Shusterman', 'Warren Kampf' )
create_data2(get_district_data(49), '49th', 'TOPRANI', 'COOK', 'Steven Toprani', 'Bud Cook' )
create_data2(get_district_data(29), '29th', 'DIXON', 'SCHROEDER', 'Andrew Dixon', 'Meghan Schroeder' )
create_data2(get_district_data(74), '74th', 'WILLIAMS', 'TURNER', 'Mike Doyle', 'Martina White' )
create_data2(get_district_data(181), '181st', 'KENYATTA', 'STREET', 'Malcolm Kenyatta', 'Milton Street' )
create_data2(get_district_data(105), '105th', 'EPSTEIN', 'LEWIS', 'Eric Epstein', 'Andrew Lewis' )
create_data2(get_district_data(162), '162nd', 'DELLOSO', 'HOPPER', 'David Delloso', 'Mary Hopper' )
create_data2(get_district_data(30), '30th', 'MONROE', 'MIZGORSKI', 'Betsy Monroe', 'Lori Mizgorski' )
create_data2(get_district_data(54), '54th', 'MCCABE', 'BROOKS', 'Jon McCabe', 'Bob Brooks' )
create_data3(get_district_data(199), '199th', 'MCGINNIS', 'GLEIM', 'BOUST', 'Sherwood McGinnis', 'Barbara Gleim','Chuck Boust' )
create_data2(get_district_data(44), '44th', 'KNOLL', 'GAYDOS', 'Michele Knoll', 'Valerie Gaydos' )
create_data2(get_district_data(62), '62nd', 'DELLAFIORA', 'STRUZZI', 'Logan Dellafiora', 'James Struzzi' )
create_data3(get_district_data(53), '53rd', 'MALAGARI', 'SZEKELY', 'WALDENBERGER', 'Steve Malagari', 'George Szekely', 'John Waldenberger' )
create_data2(get_district_data(146), '146th', 'CIRESI', 'QUIGLEY', 'Joe Ciresi', 'Tom Quigley' )
create_data2(get_district_data(40), '40th', 'GUIDI', 'MIHALEK STUCK ', 'Sharon Guidi', 'Natalie Mihalek' )
create_data2(get_district_data(25), '25th', 'MARKOSEK', 'SCHLAUCH', 'Brandon Markosek', 'Steve Schlauch' )
create_data2(get_district_data(80), '80th', 'BURKE', 'GREGORY', 'Laura Burke', 'James Gregory' )
create_data2(get_district_data(144), '144th', 'BUCK', 'POLINCHOCK', 'Meredith Buck', 'Todd Polinchock' )
create_data2(get_district_data(2), '2nd', 'MERSKI', 'KUZMA', 'Bob Merski', 'Tim Kuzma' )
create_data2(get_district_data(193), '193rd', 'NELSON', 'ECKER', 'Matt Nelson', 'Torren Ecker' )
create_data2(get_district_data(150), '150th', 'WEBSTER', 'FOUNTAIN', 'Joe Webster', 'Nick Fountain' )
create_data3(get_district_data(153), '153rd', 'SANCHEZ', 'BEAVER', 'BOZZACCO', 'Ben Sanchez', 'Marc Bozzacco', 'Douglas Beaver' )
create_data2(get_district_data(39), '39th', 'RHODERICK', 'PUSKARIC', 'Rob Rhoderick', 'Mike Puskaric' )
create_data2(get_district_data(112), '112th', 'MULLINS', 'LEMONCELLI', 'Kyle Mullins', 'Enerst Lemoncelli' )
create_data2(get_district_data(143), '143rd', 'ULLMAN', 'FLOOD', 'Wendy Ullman', 'Joe Flood' )
create_data2(get_district_data(93), '93rd', 'RIVERA-LYTLE', 'JONES', 'Delma Rivera-Lytle', 'Mike Jones' )
create_data2(get_district_data(50), '50th', 'SNYDER', 'ROHANNA MCCLURE', 'Pam Snyder', 'Betsy Rohanna McClure' )
create_data2(get_district_data(15), '15th', 'MITKO', 'KAIL', 'Terri Mitko', 'Josh Kail' )
create_data2(get_district_data(177), '177th', 'HOHENSTEIN', 'KOZLOWSKI', 'Joe Hohenstein', 'Patty Kozlowski' )
create_data2(get_district_data(31), '31st', 'WARREN', 'GALLAGHER', 'Perry Warren', 'Ryan Gallagher' )
create_data2(get_district_data(33), '33rd', 'DERMODY', 'NULPH', 'Frank Dermody', 'Josh Nulph' )
create_data2(get_district_data(76), '76th', 'HANNA', 'BOROWICZ', 'Mike Hanna', 'Stephanie Borowicz' )
create_data2(get_district_data(48), '48th', 'MITCHELL', "O'NEAL", 'Clark Mitchell', "Tim O'Neal" )
create_data2(get_district_data(152), '152nd', 'BOLING', 'MURT', 'Daryl Boling', 'Tom Murt' )
create_data2(get_district_data(12), '12th', 'SMITH', 'METCALFE', 'Daniel Smith', 'Daryl Metcalfe' )
create_data2(get_district_data(28), '28th', 'SKOPOV', 'TURZAI', 'Emily Skopov', 'Mike Turzai' )
create_data2(get_district_data(88), '88th', 'FOSCHI', 'DELOZIER', 'Jean Foschi', 'Sheryl Delozier' )
create_data2(get_district_data(178), '178th', 'TAI', 'THOMAS', 'Helen Tai', 'Wendi Thomas' )
create_data2(get_district_data(168), '168th', 'SEALE', 'QUINN', 'Kristin Seale', 'Christopher Quinn' )
create_data2(get_district_data(122), '122nd', 'SCOTT', 'HEFFLEY', 'Kara Scott', 'Doyle Heffley' )
create_data2(get_district_data(155), '155th', 'OTTEN', 'CORBIN', 'Danielle Otten', 'Becky Corbin' )
create_data2(get_district_data(97), '97th', 'GULICK', 'MENTZER', 'Dana Gulick', 'Steven Mentzer' )
create_data3(get_district_data(13), '13th', 'WALKER', 'LAWRENCE', 'PIROCCHI',  'Susannah Walker', 'John Lawrence', 'Dominic Pirocchi' )
create_data2(get_district_data(183), '183th', 'RUFF', 'MAKO', 'Jason Ruff', 'Zach Mako' )
create_data2(get_district_data(104), '104th', 'SMITH', 'HELM', 'Patty Smith', 'Sue Helm' )
create_data2(get_district_data(9), '9th', 'SAINATO', 'MICHALEK', 'Chris Sainato', 'Gregory Michalek' )
create_data2(get_district_data(14), '14th', 'FAZIO', 'MARSHALL', 'Amy Fazio', 'James Marshall' )
create_data2(get_district_data(26), '26th', 'HACKER', 'HENNESSEY', 'Pam Hacker', 'Tim Hennessey' )
create_data2(get_district_data(46), '46th', 'TIMMINS', 'ORTITAY', 'Byron Timmins', 'Jason Ortitay' )
create_data2(get_district_data(51), '51st', 'MAHONEY', 'DOWLING', 'Tim Mahoney', 'Matthew Dowling' )
create_data2(get_district_data(57), '57th', 'WARREN', 'NELSON', 'Collin Warren', 'Eric Nelson' )
create_data2(get_district_data(62), '62nd', 'DELLAFIORA', 'STRUZZI', 'Logan Dellafiora', 'Jim Struzzi' )
create_data2(get_district_data(58), '58th', 'POPOVICH', 'WALSH', 'Mary Popovich', 'Justin Walsh' )
create_data2(get_district_data(115), '115th', 'MADDEN', 'PARKER', 'Maureen Madden', 'David Parker' )
create_data2(get_district_data(131), '131st', 'LEE', 'SIMMONS', 'Andy Lee', 'Justin Simmons' )
create_data2(get_district_data(134), '134th', 'APPLEBACH', 'MACKENZIE', 'Tom Applebach', 'Ryan Mackenzie' )
create_data3(get_district_data(137), '137th', 'COZZE', 'EMRICK', 'REAGAN', 'Amy Cozze', 'Joe Emrick', 'Ed Reagan' )
create_data3(get_district_data(138), '138th', 'DONAHER', 'HAHN', 'TOWNE', 'Dean Donaher', 'Marcia Hahn', 'Jake Towne' )
create_data2(get_district_data(142), '142nd', 'LAREAU', 'FARRY', 'Malinda LaReau', 'Frank Farry' )
create_data2(get_district_data(151), '151st', 'JOHNSON ROTHMAN', 'STEPHENS', 'Sara Johnson Rothman', 'Todd Stephens' )
create_data2(get_district_data(189), '189th', 'RODRIGUEZ', 'BROWN', 'Adam Rodriguez', 'Rosemary Brown' )
create_data2(get_district_data(121), '121st', 'PASHINSKI', 'HENRY', 'Eddie Day Pashinski', 'Susan Henry' )










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






