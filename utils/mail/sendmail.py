from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from data.config import SMTP_PASSWORD
import smtplib


class SendMail():
    def __init__(self, mailto):
        self.msg = MIMEMultipart()
        self.msg['From'] = 'hse.telegram.bot@gmail.com'
        self.msg['To'] = mailto
        self.msg['Subject'] = Header('Код для авторизации', 'utf-8')

        self.password = SMTP_PASSWORD
    
    async def sendmail(self, message):
        self.msg.attach(MIMEText(message, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(self.msg['From'], self.password)
    
        server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        
        server.quit()