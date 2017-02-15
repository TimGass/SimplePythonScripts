#!/usr/bin/env python3.5
import imaplib
import smtplib
import time
import datetime
import email
from email.mime.text import MIMEText
from dateutil import tz
from subprocess import call
from confidentials import *

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
    msg = msg[msg.find("\n")+1:len(msg)]
    msg = msg[msg.find("\n")+1:len(msg)]
    firstLineIndex = msg.find("\n")
    if msg[0:firstLineIndex] == executionString:
        secondLineIndex = msg.find("\n", firstLineIndex+1)
        thirdLineIndex = msg.find("\n", secondLineIndex+1)
        print(msg[firstLineIndex+1:secondLineIndex])
        try:
            call(msg[firstLineIndex+1:secondLineIndex], shell=True)
        except OSError:
            string = "Command not input command properly! Could not run."
            error = MIMEText(string)
            error['Subject'] = "Command Error"
            error['From'] = myEmail
            error['To'] = phone
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(myEmail, gpass)
            server.sendmail(myEmail, [phone], error.as_string())
            server.quit()
