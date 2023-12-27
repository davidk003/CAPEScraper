import requests
import time
import json
from bs4 import BeautifulSoup
#_schedOption1: 1-99
#_schedOption2: 100-198
#_schedOption3: 200-297
#_schedOption4: 195s
#_schedOption5: 199s
#_schedOption7: 298s
#_schedOption8: 299s
#_schedOption9: 500+
#_schedOption10: 400+
#_schedOption11: 87&90s courses
#_schedOption12: 99s courses
#_schedOption13: 300+ courses

# #===============UNUSED PAYLOAD/FORM DATA========================
# #Used for search by professor or title
# instructorType = None 
# titleType = None
# #Used for search by section id(s)
# courses = []
# #Used for search by code(s)
# sections = []
# #Used for search by department
# selectedDepartments = [] # Leave empty

# _hideFullSec = None # on by default "only show sections with seats available" checkbox
# _showPopup = None # on by default "show the results in a popup window" checkbox
# schStartTimeDept = None #0 by default
# schEndAmPmDept = None #0 by default
# #===============================================================

WRITE_FILE = "test.html"
BASE_REQUEST_STRING = "https://act.ucsd.edu/scheduleOfClasses"
SCHEDULE_RESULT_PATH = "/scheduleOfClassesFacultyResult.htm"
SELECTED_TERM_QUERY_STRING = "?selectedTerm="
SUBJECT_LIST_PATH = "/subject-list.json"
TERM_LIST = ["FA", "WI", "SP", "SA", "SU"] #Fall, Winter, Spring, Summer Sessions(All but med), "Summer Med School"
pageNum = 1
selectedSubjects = [] #Must choose, more than one input possible Ex: "CSE", "ANTH" etc..



print("Initialization Pass Started")
requestStart = time.time()

#Get the current/latest term (Default term selection on page entry)
r = requests.get(BASE_REQUEST_STRING+SCHEDULE_RESULT_PATH)
soup = BeautifulSoup(BeautifulSoup(r.text, "lxml").prettify(), "lxml")
latestTerm = soup.find_all(id="selectedTerm")[0].option["value"]

#Grab all subjects for the given latest term
r = requests.get(BASE_REQUEST_STRING + SUBJECT_LIST_PATH , params={"selectedTerm": latestTerm})
subjectList  = [ d["code"] for d in json.loads(r.text) ] #One liner equivalent to converting list of dictionaries to a list of their "code" values.

requestStop = time.time()
print("Latest term: "  + latestTerm)
print("Subjects for the quarter: " + str(subjectList))
print("Initialization Pass end")
print("Initialization Pass HTTP Request time took "  + str(requestStop-requestStart) + " secs.")

#Form list of subjects into HTTP message data
messageData = {'selectedTerm': latestTerm,
               'selectedSubjects': subjectList,
               "schedOption1" : "true",
               "schedOption2" : "true"}
HTTPparams = {
    'page': str(pageNum),
}

print("")
requestStart = time.time()
r = requests.post(BASE_REQUEST_STRING+SCHEDULE_RESULT_PATH, params=HTTPparams, data=messageData)
with open(WRITE_FILE, "w") as file:
    print("Writing to " + WRITE_FILE)
    file.write(r.text)
requestStop = time.time()
print(str(requestStop-requestStart))

soup = BeautifulSoup(BeautifulSoup(r.text, "lxml").prettify(), "lxml")
s = list(soup.find(id="socDisplayCVO").findAll("a"))
s = s[len(s)-1]["href"]
maxPage = int(s[s.rfind("=")+1:])
print(maxPage)


#h2->span->class="centeralign"