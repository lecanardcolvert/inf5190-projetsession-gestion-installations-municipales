import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


USER_MAIL = os.environ.get("INF5190_SERVER_MAIL")
MAIL_PASSWORD = os.environ.get("INF5190_MAIL_SERVER_PASSWORD")


def send_mail(recipient_email, subject, body):
    """Send a mail to a recipient"""

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = USER_MAIL
    msg["To"] = recipient_email
    msg["ReplyTo"] = USER_MAIL
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(USER_MAIL, MAIL_PASSWORD)
    server.sendmail(USER_MAIL, recipient_email, msg.as_string())
    server.quit()
