import csv
import os
import datetime
import schedule
import time

# os.chdir (r'C:\Python27\2018election\csv')

# Get Returns Percentage
#f = open('../text/returns.txt', 'r')
#returns = f.read()

os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\crawl')

keystone = '##"N:\Election_Results\candpictures\keystone.png" '
#election_results = ' ' + returns + '% OF RETURNS STATEWIDE: '

# Races gov-r lt-d lt-r sen-r cd4-d cd5-d cd7-d cd7-r cd9-d cd9-r cd13-r cd14-d cd14-r
def open_text_file(file_location):
    "Opens Text File"
    f = open(file_location, 'r')
    return f.read()

def check_add_to_list(crawl, result, array):
    "Checks to see if crawl has result if not returns zero"
    crawlf = '{0} {1}% OF RETURNS {2}'.format(keystone, result, crawl)
    if result == '0.0':
        print 'Empty'
    else:
        array.append(crawlf)

    

os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\crawl')
# ===========READ TEXT FILES =========
congress_1st = open_text_file('1st_crawl.txt')
congress_2nd = open_text_file('2nd_crawl.txt')
congress_3rd = open_text_file('3rd_crawl.txt')
congress_4th = open_text_file('4th_crawl.txt')
congress_5th = open_text_file('5th_crawl.txt')
congress_6th = open_text_file('6th_crawl.txt')
congress_7th = open_text_file('7th_crawl.txt')
congress_8th = open_text_file('8th_crawl.txt')
congress_9th = open_text_file('9th_crawl.txt')
congress_10th = open_text_file('10th_crawl.txt')
congress_11th = open_text_file('11th_crawl.txt')
congress_12th = open_text_file('12th_crawl.txt')
congress_13th = open_text_file('13th_crawl.txt')
congress_14th = open_text_file('14th_crawl.txt')
congress_15th = open_text_file('15th_crawl.txt')
congress_16th = open_text_file('16th_crawl.txt')
congress_17th = open_text_file('17th_crawl.txt')
gov = open_text_file('gov_crawl.txt')
senate = open_text_file('us-senate.txt')

os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\congress')
return_1st = open_text_file('1st_returns.txt')
return_2nd = open_text_file('2nd_returns.txt')
return_3rd = open_text_file('3rd_returns.txt')
return_4th = open_text_file('4th_returns.txt')
return_5th = open_text_file('5th_returns.txt')
return_6th = open_text_file('6th_returns.txt')
return_7th = open_text_file('7th_returns.txt')
return_8th = open_text_file('8th_returns.txt')
return_9th = open_text_file('9th_returns.txt')
return_10th = open_text_file('10th_returns.txt')
return_11th = open_text_file('11th_returns.txt')
return_12th = open_text_file('12th_returns.txt')
return_13th = open_text_file('13th_returns.txt')
return_14th = open_text_file('14th_returns.txt')
return_15th = open_text_file('15th_returns.txt')
return_16th = open_text_file('16th_returns.txt')
return_17th = open_text_file('17th_returns.txt')
os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection')
return_state = open_text_file('perc--statewide.txt')
package = []

statewide_crawl = '{0} {1}% OF RETURNS STATEWIDE {2}{0} {3} '.format(keystone, return_state, gov, senate )

package.append(statewide_crawl)


check_add_to_list(congress_1st, return_1st, package)
check_add_to_list(congress_2nd, return_2nd, package)
check_add_to_list(congress_3rd, return_3rd, package)
check_add_to_list(congress_4th, return_4th, package)
check_add_to_list(congress_5th, return_5th, package)
check_add_to_list(congress_6th, return_6th, package)
check_add_to_list(congress_7th, return_7th, package)
check_add_to_list(congress_8th, return_8th, package)
check_add_to_list(congress_9th, return_9th, package)
check_add_to_list(congress_10th, return_10th, package)
check_add_to_list(congress_11th, return_11th, package)
check_add_to_list(congress_12th, return_12th, package)
check_add_to_list(congress_13th, return_13th, package)
check_add_to_list(congress_14th, return_14th, package)

package.append(keystone)
s =""
final = s.join(package)
print final

os.chdir (r'N:\Election_Results')

text_file = open("electcrawlfinal2018.txt", "w")
text_file.write(final)
text_file.close()

os.chdir (r'C:\Python27\2018FallElection\scripts') #Change to root directory




# f = open('../text/crawl/dem_5th_crawl.txt', 'r')
# dem_5th = f.read()

# f = open('../text/crawl/dem_7th_crawl.txt', 'r')
# dem_7th = f.read()

# f = open('../text/crawl/dem_9th_crawl.txt', 'r')
# dem_9th = f.read()

# f = open('../text/crawl/dem_14th_crawl.txt', 'r')
# dem_14th = f.read()

# f = open('../text/crawl/dem_lt_gov_crawl.txt', 'r')
# dem_lt_gov = f.read()

# f = open('../text/crawl/rep_7th_crawl.txt', 'r')
# rep_7th = f.read()

# f = open('../text/crawl/rep_9th_crawl.txt', 'r')
# rep_9th = f.read()

# f = open('../text/crawl/rep_13th_crawl.txt', 'r')
# rep_13th = f.read()

# f = open('../text/crawl/rep_14th_crawl.txt', 'r')
# rep_14th = f.read()

# f = open('../text/crawl/rep_lt_gov_crawl.txt', 'r')
# rep_lt_gov = f.read()

# f = open('../text/crawl/rep_us-senate.txt', 'r')
# senate = f.read()

# f = open('../text/crawl/gov_crawl.txt', 'r')
# governor = f.read()

# keystone = '##"N:\Election_Results\candpictures\keystone.png" '
# election_results = ' ' + returns + '% OF RETURNS STATEWIDE: '


# finalCrawl = '{0}{1}{2}{0}{1}{3}{0}{1}{4}{0}{1}{5}{0}{1}{6}{0}{1}{7}{0}{1}{8}{0}{1}{9}{0}{1}{10}{0}{1}{11}{0}{1}{12}{0}{1}{13}{0}{1}{14}{0} '.format(keystone,election_results,governor,dem_lt_gov, rep_lt_gov,senate,dem_4th,dem_5th,dem_7th,rep_7th,dem_9th,rep_9th,rep_13th,dem_14th,rep_14th) 

# print finalCrawl

# # os.chdir (r'../text/crawl')

# text_file = open("../text/crawl/FINALCRAWL.txt", "w")
# text_file.write(finalCrawl)
# text_file.close()

# os.chdir (r'N:\Election_Results\pythonbackup\2018election\scripts') #Change to root directory




# ==================functions =================================================================
# ===================================================================================
# def add_commas(number):#puts commas in number
#     array = []
#     for integer, comma in enumerate(reversed(str(number))):
#         if integer and (not (integer % 3)):
#             array.insert(0, ',')
#         array.insert(0, comma)
#     return ''.join(array)

# def import_CSV_create_object(input_file_name, output_object_name):#build a function
#     for row in input_file_name:
#        print row
#     return row
    
# gov_votes = csv.DictReader(open("gubernatorial-votes.csv"))
# for row in gov_votes:
#     print row
#     gov_votes = row

# gov_percent = csv.DictReader(open("gubernatorial-percentage.csv"))
# for row in gov_percent:
#     print row
#     gov_percent = row

# lt_gov_votes = csv.DictReader(open("lt-gov-votes.csv"))
# for row in gov_votes:
#     print row
#     lt_gov_votes = row

# lt_gov_percent = csv.DictReader(open("lt-gov-percentage.csv"))
# for row in lt_gov_percent:
#     print row
#     lt_gov_percent = row

# senate_votes = csv.DictReader(open("senate-votes.csv"))
# for row in gov_votes:
#     print row
#     senate_votes = row

# senate_percent = csv.DictReader(open("senate-percentage.csv"))
# for row in senate_percent:
#     print row
#     senate_percent = row
# u_house_votes = csv.DictReader(open("US-House-votes.csv"))
# for row in gov_votes:
#     print row
#     u_house_votes = row

# u_house_percent = csv.DictReader(open("US-House-percentage.csv"))
# for row in u_house_percent:
#     print row
#     u_house_percent = row



#  os.chdir (r'N:\Election_Results\txt files') #changes directory to N drive




# # supremeOpen = ' RACE FOR PA SUPREME COURT (1 OPEN SEAT):   '
# # superiorOpen = ' RACE FOR PA SUPERIOR COURT (4 OPEN SEATS):   '
# # commonwealthOpen = ' RACE FOR PA COMMONWEALTH COURT(2 OPEN SEATS):  '


# # #===============SUPERIOR COURT CANDIDATES===============================
# MCLAUGHLIN = 'MCLAUGHLIN (DEM): ' + add_commas(superiorCourt['MCLAUGHLIN'])
# NICHOLS = '  NICHOLS (DEM): ' + add_commas(superiorCourt['NICHOLS'])
# KUNSELMAN = '  KUNSELMAN (DEM): ' + add_commas(superiorCourt['KUNSELMAN'])
# MOULTON = '  MOULTON (DEM): ' + add_commas(superiorCourt['MOULTON'])
# STEDMAN = '  STEDMAN (REP): '+ add_commas(superiorCourt['STEDMAN'])
# GIORDANO = '  GIORDANO (REP): '+ add_commas(superiorCourt['GIORDANO'])
# KAGARISE = '  KAGARISE (REP): '+ add_commas(superiorCourt['KAGARISE'])
# MURRAY = '  MURRAY (REP): '+ add_commas(superiorCourt['MURRAY'])
# MERMELSTEIN = '  MERMELSTEIN (GRE): '+ add_commas(superiorCourt['MERMELSTEIN'])

# #===============COMMONWEALTH COURT CANDIDATES===============================
# CEISLER = 'CEISLER (DEM): ' + add_commas(commonwealthCourt['CEISLER'])
# CLARK = '  CLARK (DEM): ' + add_commas(commonwealthCourt['CLARK'])
# LALLEY = '  LALLEY (REP): ' + add_commas(commonwealthCourt['LALLEY'])
# FIZZANO = '  FIZZANO CANNON (REP): ' + add_commas(commonwealthCourt['FIZZANO CANNON'])

# supremeCrawl = keystone + Election_Results + supremeOpen + 'WOODRUFF (DEM): ' + add_commas(supremeCourt['WOODRUFF']) + '   MUNDY (REP): ' + add_commas(supremeCourt['MUNDY']) +  '  '
# superiorCrawl = keystone + Election_Results + superiorOpen +  MCLAUGHLIN + NICHOLS + KUNSELMAN + MOULTON + STEDMAN + GIORDANO + KAGARISE + MURRAY + MERMELSTEIN +  '  '
# commonwealthCrawl = keystone + Election_Results + commonwealthOpen + CEISLER  + CLARK + LALLEY + FIZZANO +  '  '

# finalCrawl = supremeCrawl + superiorCrawl + commonwealthCrawl + keystone






