import os
import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "../config.yml")
with open(CONFIG_FILE_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

mail = config["mail"]
USER_MAIL = os.environ.get("INF5190_SERVER_MAIL")
MAIL_PASSWORD = os.environ.get("INF5190_MAIL_SERVER_PASSWORD")
DEST = mail["destination"]
SUBJECT = mail["subject"]


def sendMail(new_installations):
    """TODO"""

    body = """
    Bonjour, voici la liste des nouvelles installations que nous avons ajouté
    depuis votre dernière visite:
    """
    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = USER_MAIL
    msg["To"] = DEST
    msg["ReplyTo"] = USER_MAIL
    for installation in new_installations:
        body += f"\n\t- {installation}"
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(USER_MAIL, MAIL_PASSWORD)
    server.sendmail(USER_MAIL, DEST, msg.as_string())
    server.quit()
