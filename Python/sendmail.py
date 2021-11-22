import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


msg = MIMEMultipart('alternative')
msg['Subject'] = "subject"
msg['From'] = "Your mail ID"
msg['To'] = "recipient mail ID"

s = smtplib.SMTP("SMTP Server") 
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
