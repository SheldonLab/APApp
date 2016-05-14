# Import smtplib for the actual sending function
import mimetypes
import smtplib

# Import the email modules we'll need
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import os

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# Create a text/plain message
from os.path import basename

files = ['/home/ubuntu/appServer/Workbook3.xlsx']

me = 'ap_app_automatic@mail.com'
you = 'bbzylstra@randolphcollege.edu'
SUBJECT = "Time Test: time is 4:20"

msg = MIMEMultipart()
msg['Subject'] = SUBJECT
msg['From'] = me
msg['To'] = you

part = MIMEBase('application', "octet-stream")
part.set_payload(open("main.py", "rb").read())
encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="main.py"')

msg.attach(part)
print msg
# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
s.starttls()
s.ehlo()
s.login(user='AKIAIT6YYNXSVVVTGTLQ',password='AmpnuPQdUECljleQ3oM/9wV6pmOXLLGVm47SsTI3Y2Fn')
s.sendmail(me, [you], msg.as_string())
print s.quit()