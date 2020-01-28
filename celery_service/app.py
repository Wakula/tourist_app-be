from celery import Celery
from config import MailServiceConfig, CeleryConfig
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json


app = Celery(
    CeleryConfig.CELERY_APP_NAME,
    broker=CeleryConfig.CELERY_BROKER_URL
)


@app.task
def async_email(recipient, subject, body):
    mail = smtplib.SMTP(
        host=MailServiceConfig.MAIL_SERVER,
        port=MailServiceConfig.MAIL_PORT
    )


    msg = MIMEMultipart()

    msg['From'] = MailServiceConfig.MAIL_USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    mail.starttls()
    mail.login(msg['From'], MailServiceConfig.MAIL_PASSWORD)
    mail.sendmail(msg['From'], msg['To'], msg.as_string())
    mail.quit()
