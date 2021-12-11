import config
import tweepy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(recipient_email, subject, body):
    """Send a mail to a recipient"""

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = config.USER_MAIL
    msg["To"] = recipient_email
    msg["ReplyTo"] = config.USER_MAIL
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(config.USER_MAIL, config.MAIL_PASSWORD)
    server.sendmail(config.USER_MAIL, recipient_email, msg.as_string())
    server.quit()


def send_tweet(new_installations):
    """Send a tweet on the app twitter account"""

    # authentication
    auth = tweepy.OAuthHandler(
        config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET
    )

    tweet = """
    Bonjour Le canardColvert, voici la liste des nouvelles installations que nous avons ajouté
    dans notre application:
    """
    # for installation in new_installations:
    #     tweet += f"\n\t- {installation}"
    api = tweepy.Client(
        bearer_token=config.TWITTER_BEARER_TOKEN,
        consumer_key=config.TWITTER_CONSUMER_KEY,
        consumer_secret=config.TWITTER_CONSUMER_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
    )

    api.create_tweet(text=tweet)
