from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from confidentials import *

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
browser.get("https://jaserader.github.io/new_portfolio/#/resumepage"); #change this link by checking network logs for the address you ping for each class when you click on that class's tab
soup = BeautifulSoup(browser.page_source, "html5lib")
browser.quit()
display.stop()
info = soup.find('p', id='skills')
skills = info.text[(info.text.find(":")+2):]
dataString = "Hello Jase, these are your skills:\n" + skills + "\nSent by raspberry pi."
textsNum = round(len(dataString)/140)
stringList = []
for i in range(textsNum):
    if(i == 0):
        stringList.append(dataString[:dataString.find("\n", ((i*140))+140)])
    else:
        stringList.append(dataString[dataString.find("\n", (i*140)):dataString.find("\n", ((i*140))+140)])
for string in stringList:
    msg = MIMEText(string)
    msg['Subject'] = ""
    msg['From'] = myEmail
    msg['To'] = "6158385484@vtext.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(myEmail, gpass)
    server.sendmail(myEmail, ["6158385484@vtext.com"], msg.as_string())
    server.quit()
