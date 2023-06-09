#USE VENV FOR PYTHON OR OTHER ALTERNATIVE, NOT RUNNING CORRECTLY ON Ubuntu 22.04.2 LTS
#TRY LOOKING INTO TKINTER FOR GUI INSTEAD OF GARBAGE TERMINAL INTERFACE
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select # Used in dropdown to selections
from selenium.webdriver.common.by import By
import time # to wait for page loading
import getpass # to conceal password
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

#webdriver manager https://pypi.org/project/webdriver-manager/#use-with-firefox
#Chrome imports
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#Chromium imports
#from selenium.webdriver.chrome.service import Service as ChromiumService
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

#Edge imports
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

#Firefox imports
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

#Internet Explorer imports
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager

    
def loginPrompt():
    userNameField = browser.find_element(By.ID, "ssousername")
    userNameField.send_keys(input("Enter SSO username\n"))

    passwordField = browser.find_element(By.ID, 'ssopassword')
    passwordField.send_keys(getpass.getpass("Enter SSO password (hidden input field) \n"))

    #press login button
    browser.find_element(By.CLASS_NAME, "btn.btn-primary.pull-right.sso-button").click()

    #0 - not yet loaded, 1 - duo loaded, 2 - login error loaded 
    browserState = 0
    #Using try catch cause find element throws a fit inbetween rendering/if element is nonexistant
    while browserState == 0:
        try:
            browser.find_element(By.ID, "duo_iframe").is_displayed
            browserState = 1
        except:
            try:
                browser.find_element(By.ID, "_login_error_message").is_displayed
                browserState = 2
            except:
                pass #do nothing

    # saved browser state to return boolean
    if browserState == 1:
        return True
    else:
        return False


URL = "https://cape.ucsd.edu/responses/Results.aspx"
#browser = webdriver.Chrome()
try:
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument("--headless=new")
    #https://pypi.org/project/webdriver-manager/
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chromeOption)
    print("Using chrome binary")
except WebDriverException:
    try:
        #dumbFireFoxProfile = webdriver.FirefoxProfile()
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.add_argument("-headless")
        browser = webdriver.Firefox(options=fireFoxOptions)
        #browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(version="v0.33.0")),firefox_options=fireFoxOptions, firefox_profile=dumbFireFoxProfile)
        print("Using firefox binary")
    except:
        print("chrome and firefox launch failure")



browser.get(URL)
browser.implicitly_wait(20)

while(not loginPrompt()):
    print(browser.find_element(By.ID, "_login_error_message").text)

#Dealing with iframes https://stackoverflow.com/questions/24247490/find-elements-inside-forms-and-iframe-using-java-and-selenium-webdriver
#Switch to iframe on selenium driver
browser.switch_to.frame('duo_iframe')
#Waits on browser duo iframe to load by checking if the text next to the dropdown is rendered
#(Required because dropdown options text will not output correctly otherwise)
#Somtimes fails??? Very rarely
while browser.find_element(By.CLASS_NAME, "cramped-frame-view").text != "Device:":
    time.sleep(0.5)

# convert element into selection dropdown
duoDeviceDropDown = Select(browser.find_element(By.TAG_NAME, 'select'))
#change dropdown into options list and iterate
print("Duo authentication device options (type the number to select)")
print("↓ [default] ↓")

# convert dropdown selections to list of options and iterate, convert devicecount to string before printing
deviceCount = 1
for device in duoDeviceDropDown.options:
    print("(" + str(deviceCount) + ") " + device.get_attribute('text')  + "\n")
    deviceCount+=1

# Enter device number
duoDeviceDropDown.select_by_index(int(input("Enter device number to DUO authenticate with: "))-1)
    # try:
    #     duoDeviceDropDown.select_by_index(int(input("Enter device number to DUO authenticate with: "))-1)
    #     isValidInput = True
    # except:
    #     print("Invalid input. (Usually Index out of bounds or non integer input)")

# TEMPORARY METHOD FOR SELECTING AUTHENTICATION METHODS (ASSUMES ONLY DUO PUSH/PASSCODE OPTIONS) maybe use xpath next time
isValidInput = False
if input("Enter (1) to sent a push notification, enter (2) to login via passcode: ") == "1":
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(browser.find_element(By.CLASS_NAME, "auth-button.positive")))
    browser.find_element(By.CLASS_NAME, "auth-button.positive").click()
    print("Duo push notification has been sent.")
else:
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(browser.find_element(By.ID, "passcode")))
    browser.find_element(By.ID, "passcode").click()
    while not isValidInput:
        try:
            browser.find_element(By.CLASS_NAME, "passcode-input").click()
            browser.find_element(By.CLASS_NAME, "passcode-input").clear()
            browser.find_element(By.CLASS_NAME, "passcode-input").send_keys(input("Enter passcode: "))
            browser.find_element(By.ID, "passcode").click()
            wait = WebDriverWait(browser, 3)
            wait.until(EC.text_to_be_present_in_element(browser.find_element(By.CSS_SELECTOR, "span.message-text")))
            print(browser.find_element(By.CSS_SELECTOR, "span.message-text").text)
            browser.find_element(By.CLASS_NAME, "btn-dismiss.medium-or-larger").click()
            isValidInput = True
        except:
            if browser.current_url == "https://cape.ucsd.edu/responses/Results.aspx":
                isValidInput = True
            else:
                print("Incorrect passcode/generate a new passcode and try again")
                #Spams message, fix later

while browser.current_url != "https://cape.ucsd.edu/responses/Results.aspx":
    time.sleep(0.1)
print("CAPES SITE LOADED")
browser.switch_to.default_content()
# ASSUME CAPES SITE LOADED
# TRY USING THIS FOR ALL ABOVE WAITS/UNTILS
# WebDriverWait(browser, 20).until(EC.element_to_be_clickable(browser.find_element(By.ID, "ContentPlaceHolder1_btnSubmit")))
CAPEsearchButton = browser.find_element(By.ID, "ContentPlaceHolder1_btnSubmit")
# WebDriverWait(browser, 20).until(EC.presence_of_element_located(browser.find_element(By.ID, "ContentPlaceHolder1_ddlDepartments")))
departmentDropdown = Select(browser.find_element(By.ID, "ContentPlaceHolder1_ddlDepartments"))

#Start writing to file
output = open("capescraperoutput.txt", 'w')

#Iterate over dropdown text
for i in range(1, len(departmentDropdown.options)):
    dropdownOption = departmentDropdown.options[i].get_attribute('text')
    output.write(dropdownOption + "\n")
    print(departmentDropdown.options[i].get_attribute('text'))

print("END OF DROPDOWN")

output = open("capescraperoutput.txt", 'w')
output.close()

time.sleep(1000)
