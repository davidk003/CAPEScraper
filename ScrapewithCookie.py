import time
import json
import os
import selenium.webdriver.support.expected_conditions

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select # Used in dropdown to selections
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def wait_for_page():
    try:
        driver.set_page_load_timeout(30)
    except Exception as e:
        print("Page failed to load after 30 seconds")
        if debugFlag:
            print(e)
        exit(1)

scriptStartTime = time.time()
chromeOptions = Options()
chromeOptions.page_load_strategy = 'none' #Wont wait for page to load
debugFlag = False
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options= chromeOptions)

#pre-load this site to add cookies (must be this site or else cookies will fail to add from domain mismatch)
driver.get("https://cape.ucsd.edu")
wait_for_page()
#Try loading logincookie.json
try:
    for jsonObject in json.load(open("logincookie.json")):
        #add cookies from file
        try:
            driver.add_cookie(jsonObject)
        except:
            print("Failed to add cookies, login required.")
            break
    print("Cookies added successfully")
except Exception as e:
    print("logincookie.json not present or failed to load")
    if debugFlag:
        print(e)

#Clear previous cookies by deleting logincookie.json
try:
    os.remove("logincookie.json")
except FileNotFoundError:
    print("logincookie.json not present, file not removed.")


driver.get("https://cape.ucsd.edu/responses/Results.aspx")
wait_for_page()

WebDriverWait(driver, timeout=120).until(selenium.webdriver.support.expected_conditions.url_to_be("https://cape.ucsd.edu/responses/Results.aspx"))

allCookies = driver.get_cookies()
logincookies = open("logincookie.json", "w")
json.dump(driver.get_cookies(), logincookies)
logincookies.close()

if debugFlag:
    print("Cookies after login: ")
    for cookie in allCookies:
        print(cookie)
    print("number of cookies: " + str(len(allCookies)))

print("Capes site loaded.")

WebDriverWait(driver, timeout=120).until(selenium.webdriver.support.expected_conditions.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlDepartments")))
departmentSelection = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDepartments"))
departmentCodes = []
departmentFullName = []

for i, department in enumerate(departmentSelection.options):
    departmentCodes.append(department.get_attribute('value').replace(" ", ""))
    departmentFullName.append(department.get_attribute('text'))
    #driver.find_element(By.ID, "ContentPlaceHolder1_btnSubmit").click()

#The first option in the dropdown "Select a department" needs to be removed
try:
    departmentCodes.remove('')
except:
    pass
    #do nothing
try:
    departmentFullName.remove('Select a Department')
except:
    pass



if debugFlag:
    print("Dept. FullNames [{0}]:".format(len(departmentFullName)))
    print(departmentFullName)
    print("Dept. Codes [{0}]:".format(len(departmentCodes)))
    print(departmentCodes)

BASE_SEARCH_URL = "https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber="

try:
    os.makedirs("CAPEdata")
except:
    print("directory creation failed or already exists.")

originalWindow = driver.current_window_handle
departmentCodeQueue = departmentCodes.copy()
windowHandles = []
progressCount = 0


#Load 10 windows
for i in range(0, 10):
    driver.switch_to.new_window('tab')
    driver.current_window_handle
    driver.get(BASE_SEARCH_URL + departmentCodeQueue.pop(0))

print("Extracting site html: ")
#Loop until all windows processed
while progressCount < len(departmentCodes):
    #Loop through the 10 loaded tabs
    for i in range(1, len(driver.window_handles)): #try 11 if len doesnt work
        driver.switch_to.window(driver.window_handles[i])
        try:
            driver.find_element(By.ID, "ContentPlaceHolder1_gvCAPEs")
            with open("CAPEdata/CAPE_" + driver.current_url.replace(BASE_SEARCH_URL, '') + ".html", 'w') as file:
                file.write(driver.page_source)
            if len(departmentCodeQueue) > 0:
                driver.get(BASE_SEARCH_URL + departmentCodeQueue.pop())
                progressCount+=1
                print("Progress: " + str(progressCount) + "/" + str(len(departmentCodes)))
            else:
                break
        except:
            print("Progress: " + str(progressCount) + "/" + str(len(departmentCodes)))
            continue
    if len(departmentCodeQueue) == 0:
        for window in driver.window_handles:
            if window != originalWindow:
                try:
                    driver.set_page_load_timeout(30)
                    with open("CAPEdata/CAPE_" + driver.current_url.replace(BASE_SEARCH_URL, '') + ".html", 'w') as file:
                        file.write(driver.page_source)
                        progressCount+=1
                        print("Progress: " + str(progressCount) + "/" + str(len(departmentCodes)))
                        driver.close()
                except:
                    pass
                    #print("Exceeded load time, rerun.")
                    
    


#Cleanup all windows except original
for window in driver.window_handles:
    if window != originalWindow:
        driver.switch_to.window(window)
        WebDriverWait(driver, timeout=120).until(selenium.webdriver.support.expected_conditions.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlDepartments")))
        with open("CAPEdata/CAPE_" + driver.current_url.replace(BASE_SEARCH_URL, '') + ".html", 'w') as file:
                file.write(driver.page_source)
        driver.close()
driver.switch_to.window(originalWindow)

progressCount = 0
print("Parsing html to extract data to csv:")
try:
    os.makedirs("CAPEcsv")
except:
    print("\"CAPEcsv\" directory creation failed or already exists.")
for code in departmentCodes:
    with open("CAPEdata/CAPE_" + code + ".html", 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        #Check for failed harvest
    with open("CAPEcsv/CAPE_" + code + ".csv", 'w') as file:
        if len(soup.findAll(id="ContentPlaceHolder1_gvCAPEs_lblEmptyData")) != 0 or soup.table is None:
                print("------ EMPTY DATA, TABLE GENERATION FAILED [" + file.name + "] ------")
                file.write("empty")
        else:
            for i, string in enumerate(soup.table.stripped_strings):
                if i % 10 == 0 : #Table/CSV header is 10 elements
                    file.write("\n")
                else:
                    file.write(",")
                file.write(string.replace("\n", ""))
    progressCount+=1
    print("Progress: " + str(progressCount) + "/" + str(len(departmentCodes)))



print("End and sleep.")
print("Time to completion: " + str(time.time()-scriptStartTime) + " seconds")

time.sleep(100)
driver.quit()


