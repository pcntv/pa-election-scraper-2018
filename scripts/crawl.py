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





