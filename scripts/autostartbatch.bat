 :get_congress_percentages
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\senate.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\gov.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\get_congress_percentages.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\congress.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\pasenate.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\pahouse.py
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\crawl.py
 timeout /t 1
 goto get_congress_percentages

 :get_congress
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\congress.py
 timeout /t 1
 goto get_congress_percentages

 :get_gov
C:\Python27\python.exe C:\Python27\2018FallElection\scripts\gov.py
 timeout /t 1
 goto get_congress
 
