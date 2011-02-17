#!/usr/bin/env python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

class ErrorReporter:
    def __init__(self,Configs):
        self.Configs = Configs
        self.gmail_user = "songzz123@gmail.com"
        self.gmail_pwd = "song1123...."
        
    def mail(self,to, subject, text, attach):
       msg = MIMEMultipart()
       msg['From'] = self.gmail_user
       msg['To'] = to
       msg['Subject'] = subject
       msg.attach(MIMEText(text))
       if attach !="":
           part = MIMEBase('application', 'octet-stream')
           part.set_payload(open(attach, 'rb').read())
           Encoders.encode_base64(part)
           part.add_header('Content-Disposition',
                   'attachment; filename="%s"' % os.path.basename(attach))
           msg.attach(part)
       mailServer = smtplib.SMTP("smtp.gmail.com", 587)
       mailServer.ehlo()
       mailServer.starttls()
       mailServer.ehlo()
       mailServer.login(self.gmail_user, self.gmail_pwd)
       mailServer.sendmail(self.gmail_user, to, msg.as_string())
       # Should be mailServer.quit(), but that crashes...
       mailServer.close()

if __name__ == '__main__':
    this = ErrorReporter("")
    this.mail('mscame@gmail.com',"JiuJiu error Report","hi","")
