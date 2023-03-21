import requests

#Initialize URL
URL = "https://cape.ucsd.edu/responses/Results.aspx"
#http request to get page
page = requests.get(URL)
#Open file to write
webpageFile = open("capes.html", "w")
webpageFile.write(page.text)
#Open file to read and print to console
webpageFile = open("capes.html", "r")
print(webpageFile.read())


#https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
#check how to login and get page


webpageFile.close()