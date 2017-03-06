from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from confidentials import *
from webdriverLocation import *
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
import math
import time

session = requests.Session()
display = Display(visible=0, size=(1366, 768))
display.start()
browser = webdriver.Chrome(driverLocation)
browser.set_window_size(1366, 768)
browser.get("https://us3.walmartone.com/")
button = browser.find_element_by_css_selector("a.e-button.e-button--compact")
webdriver.ActionChains(browser).move_to_element(button).perform()
button.click()
browser.execute_script("document.querySelector('#uxUserName').value='" + wally + "';document.querySelector('#uxPassword').focus();document.querySelector('#uxPassword').value='" + password + "';document.querySelector('input#SubmitCreds').click();")
browser.get("https://us.walmartone.com/en/walmart/profile/schedule/")
frame = browser.find_element_by_css_selector("div#DeskSchedule iframe")
browser.switch_to.frame(frame)
passwordTag = WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.ID, 'uxPassword')))
usernameTag = browser.find_element_by_id("uxUserName")
passwordTag = browser.find_element_by_id("uxPassword")
submitTag = browser.find_element_by_id("SubmitCreds")
usernameTag.send_keys(wally)
passwordTag.send_keys(password)
submitTag.click()
browser.refresh()
frame = browser.find_element_by_css_selector("div#DeskSchedule iframe")
browser.switch_to.frame(frame)
soup = BeautifulSoup(browser.page_source, "html5lib")
browser.quit()
display.stop()
table = soup.findAll("table", class_="weekTable")[3]
details = []
for detail in table.findAll("div", class_="dayDets"):
    for div in detail.findAll("div"):
        details.append(div.text)
times = []
for span in table.select("div.Sched > span > span:nth-of-type(1)"):
    if (span.find("b") == None):
        times.append(span.text)
    else:
        times.append(span.find("b").text)
dataString = "Walmart schedule for next week:\n"
for i, val in enumerate(details):
    if ((i % 2) == 0):
        dataString += val + " "
    else:
        dataString += val + ": " + times[int((i-1)/2)] + "\n"
stringList = []
textsNum = math.ceil(len(dataString)/140)
for i in range(textsNum):
    if(i == 0):
        stringList.append(dataString[:dataString.find("\n", 140)])
    else:
        stringList.append(dataString[dataString.find("\n", (i*140)):dataString.find("\n", ((i*140))+140)])
for string in stringList:
    if stringList.index(string) != 0:
        time.sleep(100)
    msg = MIMEText(string)
    msg['Subject'] = ""
    msg['From'] = myEmail
    msg['To'] = phone
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(myEmail, gpass)
    server.sendmail(myEmail, [phone], msg.as_string())
    server.quit()
