#!/usr/bin/env python3.5
import imaplib
import smtplib
import time
import datetime
import email
from email.mime.text import MIMEText
from dateutil import tz
import subprocess
from confidentials import *
import re

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(myEmail, gpass)
mail.list

mail.select("inbox")
result, data = mail.search(None, "(FROM " + myEmail + ")")
ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest
# fetch the email body (RFC822) for the given ID
result, data = mail.fetch(latest_email_id, "(RFC822)")
raw_email = data[0][1].decode("utf-8")
email_message = email.message_from_string(raw_email)
recieved = email_message['Received']
if abs(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - datetime.datetime.strptime(recieved[recieved.find(";")+2:len(recieved)-6], '%a, %d %b %Y %H:%M:%S %z').astimezone(tz.gettz("America/Chicago"))) < datetime.timedelta(seconds=60):
    if email_message.is_multipart():
        msg = email_message.get_payload()[0].as_string()
    else:
        msg = email_message.get_payload().as_string()
    #remove extra spaces that exist, for some reason
    msg = msg[msg.find("\n")+1:len(msg)]
    msg = msg[msg.find("\n")+1:len(msg)]
    msgArray = []
    msgArray = re.split('\n', msg, flags=re.A|re.M)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(myEmail, gpass)
    for i in range(1, len(msgArray)-1, 2):
        if msgArray[0] == executionString:
            try:
                output = subprocess.check_output([ msgArray[i], msgArray[i+1]])
            except subprocess.CalledProcessError as error:
                error = MIMEText(str(error))
                error['Subject'] = "Command Error"
                error['From'] = myEmail
                error['To'] = phone
                server.sendmail(myEmail, [phone], error.as_string())
                print(error)
    server.quit()
