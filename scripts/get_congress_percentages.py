import urllib, json, locale, os, ssl, decimal

import schedule
import time


counties = [ 
    'ADAMS',
    'ALLEGHENY',
    'ARMSTRONG',
    'BEAVER',
    'BEDFORD',
    'BERKS',
    'BLAIR',
    'BRADFORD',
    'BUCKS',
    'BUTLER',
    'CAMBRIA',
    'CAMERON',
    'CARBON',
    'CENTRE',
    'CHESTER',
    'CLARION',
    'CLEARFIELD',
    'CLINTON',
    'COLUMBIA',
    'CRAWFORD',
    'CUMBERLAND',
    'DAUPHIN',
    'DELAWARE',
    'ELK',
    'ERIE',
    'FAYETTE',
    'FOREST',
    'FRANKLIN',
    'FULTON',
    'GREENE',
    'HUNTINGDON',
    'INDIANA',
    'JEFFERSON',
    'JUNIATA',
    'LACKAWANNA',
    'LANCASTER',
    'LAWRENCE',
    'LEBANON',
    'LEHIGH',
    'LUZERNE',
    'LYCOMING',
    'MCKEAN',
    'MERCER',
    'MIFFLIN',
    'MONROE',
    'MONTGOMERY',
    'MONTOUR',
    'NORTHAMPTON',
    'NORTHUMBERLAND',
    'PERRY',
    'PHILADELPHIA',
    'PIKE',
    'POTTER',
    'SCHUYLKILL',
    'SNYDER',
    'SOMERSET',
    'SULLIVAN',
    'SUSQUEHANNA',
    'TIOGA',
    'UNION',
    'VENANGO',
    'WARREN',
    'WASHINGTON',
    'WAYNE',
    'WESTMORELAND',
    'WYOMING',
    'YORK' ]

testcounty = [
    'ADAMS',
    'YORK' ]

firstCounties = ['BUCKS','MONTGOMERY']
firstCounties = ['BUCKS','MONTGOMERY']
secondCounties = ['PHILADELPHIA']
thirdCounties = ['PHILADELPHIA']
fourthCounties = ['BERKS', 'MONTGOMERY']
fifthCounties = ['CHESTER', 'DELAWARE', 'MONTGOMERY', 'PHILADELPHIA']
sixthCounties = ['BERKS', 'CHESTER']
seventhCounties = ['LEHIGH', 'MONROE', 'NORTHAMPTON']
eighthCounties = ['LACKAWANNA', 'LUZERNE', 'MONROE', 'PIKE', 'WAYNE']
ninethCounties = ['BERKS', 'CARBON', 'COLUMBIA', 'LEBANON', 'LUZERNE', 'MONTOUR', 'NORTHUMBERLAND', 'SCHUYLKILL']
tenthCounties = ['CUMBERLAND', 'DAUPHIN', 'YORK']
eleventhCounties = ['LANCASTER', 'YORK']
twelvethCounties = ['BRADFORD', 'CENTRE', 'CLINTON', 'JUNIATA', 'LYCOMING', 'MIFFLIN', 'NORTHUMBERLAND', 'PERRY', 'POTTER', 'SNYDER', 'SULLIVAN', 'SUSQUEHANNA', 'TIOGA', 'UNION', 'WYOMING']
thirteenthCounties = ['ADAMS', 'BEDFORD', 'BLAIR', 'CAMBRIA', 'CUMBERLAND', 'FRANKLIN', 'FULTON', 'HUNTINGDON', 'SOMERSET', 'WESTMORELAND']
fourteenthCounties = ['FAYETTE', 'GREENE', 'WASHINGTON', 'WESTMORELAND']
fifteenthCounties = ['ARMSTRONG', 'BUTLER', 'CAMBRIA', 'CAMERON', 'CENTRE', 'CLARION', 'CLEARFIELD', 'ELK', 'FOREST', 'INDIANA', 'JEFFERSON', 'MCKEAN', 'VENANGO', 'WARREN']
sixteenthCounties = ['BUTLER', 'CRAWFORD', 'ERIE', 'LAWRENCE', 'MERCER']
seventeenthCounties = ['ALLEGHENY', 'BEAVER', 'BUTLER']
eighteenthCounties = ['ALLEGHENY']


def find_values(id, json_repr):
    "This parses JSON for values"
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # return value ignored
    return results

json_repr = '{"P1": "ss", "Id": 1234, "P2": {"P1": "cccc"}, "P3": [{"P1": "aaa"}]}'


def get_county_percentages( counties ):
    "This pulls the json data for counties down"
    for county in counties:
        response = urllib.urlopen('https://www.electionreturns.pa.gov/api/ElectionReturn/GetCountyMessageData?countyName={}&methodName=GetCountyMessageData&electionid=undefined&electiontype=G&isactive=undefined'.format(county))
        rdata = json.loads(response.read())
        Percentage = find_values('Percentage', rdata)
        VotingDistrict = find_values('VotingDistrict', rdata)
        ReportingDistrict = find_values('ReportingDistrict', rdata)

        os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\county_return') #changes directory to N drive

        file = open("{}_perc.txt".format(county), "w")
        file.write(Percentage[0])
        file.close()

        file = open("{}_voteDistrict.txt".format(county), "w")
        file.write(VotingDistrict[0])
        file.close()

        file = open("{}_reportDistrict.txt".format(county), "w")
        file.write(ReportingDistrict[0])
        file.close()

        os.chdir (r'C:\Python27\2018FallElection\scripts') #changes directory to N drive


def get_statewide_percentages():
    "This gets statewide percentage saves out as text file"
    statewide = 'statewide'
    response = urllib.urlopen('https://www.electionreturns.pa.gov/api/ElectionReturn/GetDashboardMessage?countyName=&methodName=GetDashboardMessage&electionid=63&electiontype=G&isactive=1')
    rdata = json.loads(response.read())
    Percentage = find_values('Percentage', rdata)
    VotingDistrict = find_values('VotingDistrict', rdata)
    ReportingDistrict = find_values('ReportingDistrict', rdata)

    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection') #changes directory to N drive

    file = open("perc--{}.txt".format(statewide), "w")
    file.write(Percentage[0])
    file.close()

    file = open("voteDistrict--{}.txt".format(statewide), "w")
    file.write(VotingDistrict[0])
    file.close()

    file = open("reportDistrict--{}.txt".format(statewide), "w")
    file.write(ReportingDistrict[0])
    file.close()

    os.chdir (r'C:\Python27\2018FallElection\scripts') #changes directory to N drive

def get_timestamp():
    "This gets timestamp to verify if json is being updated"
    statewide = 'statewide'
    response = urllib.urlopen('https://www.electionreturns.pa.gov/api/ElectionReturn/GetUpdatedTimeStamp?methodName=LastUpdatedTimeStamp')
    rdata = json.loads(response.read())
    print rdata
    print "Percentages Updated"

def get_return_district(counties, district_name):
    "This calculates district voting percentages"
    votingDistrict = []
    reportingDistrict = []
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\county_return')
    for county in counties:
        response = open('{}_voteDistrict.txt'.format(county), 'r')
        district = int(response.read())
        votingDistrict.append(district)
    for county in counties:
        response = open('{}_reportDistrict.txt'.format(county), 'r')
        district = int(response.read())
        reportingDistrict.append(district)
    vote_total = sum(votingDistrict)
    reporting_total = sum(reportingDistrict)
    divideNumbers = (reporting_total/float(vote_total)*(100))
    # testNumbers = (reporting_total/float(vote_total)*(100))
    final_numbers = str(round(divideNumbers, 2))
    print final_numbers
    #Save out file
    os.chdir (r'N:\Election_Results\pythonbackup\2018FallElection\congress')
    file = open("{}_returns.txt".format(district_name), "w")
    file.write(final_numbers)
    file.close()
    os.chdir (r'C:\Python27\2018FallElection\scripts') #changes directory to N drive


# def job():
get_county_percentages(counties)
get_statewide_percentages()
get_timestamp()

get_return_district(firstCounties, '1st')
get_return_district(secondCounties, '2nd')
get_return_district(thirdCounties, '3rd')
get_return_district(fourthCounties, '4th')
get_return_district(fifthCounties, '5th')
get_return_district(sixthCounties, '6th')
get_return_district(seventhCounties, '7th')
get_return_district(eighthCounties, '8th')
get_return_district(ninethCounties, '9th')
get_return_district(tenthCounties, '10th')
get_return_district(eleventhCounties, '11th')
get_return_district(twelvethCounties, '12th')
get_return_district(thirteenthCounties, '13th')
get_return_district(fourteenthCounties, '14th')
get_return_district(fifteenthCounties, '15th')
get_return_district(sixteenthCounties, '16th')
get_return_district(seventeenthCounties, '17th')
get_return_district(eighteenthCounties, '18th')

# schedule.every(30).seconds.do(job)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

