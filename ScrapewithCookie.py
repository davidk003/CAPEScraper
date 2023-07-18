import time
import json
import os
import selenium.webdriver.support.expected_conditions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select # Used in dropdown to selections
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def wait_for_page():
    try:
        driver.set_page_load_timeout(30)
    except Exception as e:
        print("Page failed to load after 30 seconds")
        if debugFlag:
            print(e)
        exit(1)


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
    departmentCodes.append(department.get_attribute('value'))
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


driver.switch_to.new_window('tab')
driver.get(BASE_SEARCH_URL + departmentCodeQueue.pop(0))
#Keep looping while queue not empty and length 
while len(departmentCodeQueue)!=0 and len(driver.window_handles)!=1:
    #add a new tab and search if under limit
    while len(driver.window_handles) < 11 and len(departmentCodeQueue)>0:
        driver.switch_to.new_window('tab')
        driver.get(BASE_SEARCH_URL + departmentCodeQueue.pop(0))
        print("Added window, current length: " + str(len(driver.window_handles)))
    # Check all window handles (except original window), if ready harvest and close.

    lenBeforeCheck = len(driver.window_handles)
    windowIndex = 1
    while(windowIndex < len(driver.window_handles)):
        print("checked i: " + str(windowIndex) + "; windowhandles length: " + str(len(driver.window_handles)))
        driver.switch_to.window(driver.window_handles[windowIndex])
        try:
            driver.find_element(By.ID, "ContentPlaceHolder1_gvCAPEs")
            with open("CAPEdata/CAPE " + driver.current_url.replace(BASE_SEARCH_URL, '') + ".html", 'w') as file:
                file.write(driver.page_source)
            driver.close()
            #lenBeforeCheck-=1
            print("window " + str(windowIndex) + " removed.")
        except:
            print("window check/removal failed.")
        windowIndex+=1
    driver.switch_to.window(originalWindow)

driver.switch_to.window(originalWindow)

    


print("End and sleep.")

time.sleep(100)
driver.quit()


