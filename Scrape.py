from selenium import webdriver
from selenium.webdriver.support.select import Select # Used in dropdown to selections
from selenium.webdriver.common.by import By
import time # to wait for page loading
import getpass # to conceal password

def loginPrompt():
    userNameField = browser.find_element(By.ID, "ssousername")
    userNameField.send_keys(input("Enter SSO username\n"))

    passwordField = browser.find_element(By.ID, 'ssopassword')
    passwordField.send_keys(getpass.getpass("Enter SSO password (hidden input field) \n"))

    #press login button
    browser.find_element(By.CLASS_NAME, "btn.btn-primary.pull-right.sso-button").click()
    # pageLoading = True
    # while pageLoading :
    #     try:
    #         browser.find_element(By.ID, "duo_iframe").is_displayed
    #     except NoSuchElementException:

    while browser.find_element(By.ID, "duo_iframe").is_displayed or browser.find_element(By.ID, "_login_error_message").is_displayed:
        time.sleep(0.1)
        print(browser.find_element(By.ID, "duo_iframe").is_displayed)
        print("promptloop")

    if browser.find_element(By.ID, "_login_error_message").is_displayed:
        return False
    else:
        return True
    


URL = "https://cape.ucsd.edu/responses/Results.aspx"
browser = webdriver.Chrome()
browser.get(URL)

while(not loginPrompt()):
    print("loginloop")
    print(browser.find_element(By.ID, "_login_error_message").text)

#Dealing with iframes https://stackoverflow.com/questions/24247490/find-elements-inside-forms-and-iframe-using-java-and-selenium-webdriver
#Switch to iframe on selenium driver
browser.switch_to.frame('duo_iframe')

#Waits on browser duo iframe to load by checking if the text next to the dropdown is rendered
#(Required because dropdown options text will not output correctly otherwise)
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
    print("(" + str(deviceCount) + ") " +  device.text + "\n")
    deviceCount+=1


time.sleep(1000)