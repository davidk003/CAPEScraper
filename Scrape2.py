import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


#Initialize URL
URL = "https://cape.ucsd.edu/responses/Results.aspx"
browser = webdriver.Chrome()
browser.get(URL)

# userNameField = browser.find_element(By.ID, "ssousername")
# userNameField.send_keys(input("Enter SSO username\n"))

# passwordField = browser.find_element(By.ID, 'ssopassword')
# passwordField.send_keys(input("Enter SSO password\n"))
time.sleep(5)
while browser.current_url!="https://cape.ucsd.edu/responses/Results.aspx":
    time.sleep(1)

URL = browser.current_url
print(URL)

#http request to get page
page = requests.get(URL)
#Open file to write
print("Writing to file")
webpageFile = open("capes.html", 'w')
webpageFile.write(page.text)
#Open file to read and print to console
# webpageFile = open("capes.html", 'r')
# print(webpageFile.read())


#https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
#check how to login and get page


webpageFile.close()