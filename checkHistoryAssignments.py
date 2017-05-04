from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from confidentials import *
import math
import time

session = requests.Session()
data = { 'd2l_referer': '', 'userName': userName, 'password': password }
session.post("https://elearn.mscc.edu/d2l/lp/auth/login/login.d2l", data=data);
history = session.get("https://elearn.mscc.edu/d2l/home/6810221"); #change this link by checking network logs for the address you ping for each class when you click on that class's tab
soup = BeautifulSoup(history.content, "html5lib")
assignmentsDivs = soup.findAll('div', class_='d2l-collapsepane')
assigmentsList = assignmentsDivs[1].find('ul')
assignments = assigmentsList.findAll('li')
data = []
title = soup.find("a", class_="d2l-menuflyout-link-link")
data.append(title.text)
string = ""
REMOVE_STRING = "View Event - "
for assignment in assignments:
    spans = assignment.findAll("span")
    for index in range(len(assignment.findAll("div", class_="d2l-textblock"))):
        if(index % 2 == 0):
            string = assignment.findAll("div", class_="d2l-textblock")[index].text
        else:
            string += " "
            string += assignment.findAll("div", class_="d2l-textblock")[index].text
            data.append(string)
    for index in range(len(spans)):
        if(index != 0):
            if(index == 1):
                if(REMOVE_STRING in spans[index].text):
                    data[-1] += " at " + spans[index].text.replace(REMOVE_STRING, "")
                else:
                    data[-1] += " at " + spans[index].text
            else:
                if(REMOVE_STRING in spans[index].text):
                    data.append(spans[index].text.replace(REMOVE_STRING, ""))
                else:
                    data.append(spans[index].text)
dataString = "Here are your reminders for the day:\n"
for string in data:
    dataString += string + "\n"
stringList = []
textsNum = math.ceil(len(dataString)/140)
msg = MIMEText(dataString)
msg['Subject'] = ""
msg['From'] = myEmail
msg['To'] = phone

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(myEmail, gpass)
server.sendmail(myEmail, [phone], msg.as_string())
server.quit()
