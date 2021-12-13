import config
import tweepy
import smtplib
from datetime import datetime
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

    api = authenticate_to_twitter()
    date = datetime.now().strftime("%Y:%m:%d %H:%M")
    tweet = f"""
    Info du {date} GMT
    Voici les nouvelles installations de notre application:
    """
    first_tweet = True
    created_tweet_id = ""
    i = 0
    for installation in new_installations:
        if (len(tweet) <= 140) and (i < len(new_installations)):
            tweet += f"\t- {installation}\n"
        else:
            if first_tweet:
                created_tweet_id = api.create_tweet(text=tweet).data["id"]
                first_tweet = False
            else:
                temp = api.create_tweet(
                    in_reply_to_tweet_id=created_tweet_id, text=tweet
                )
                created_tweet_id = temp.data["id"]
            tweet = f"\t- {installation}\n"
        i += 1
        if i == len(new_installations):
            api.create_tweet(in_reply_to_tweet_id=created_tweet_id, text=tweet)


def authenticate_to_twitter():
    """Authenticate the app to the twitter API"""

    auth = tweepy.OAuthHandler(
        config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.Client(
        bearer_token=config.TWITTER_BEARER_TOKEN,
        consumer_key=config.TWITTER_CONSUMER_KEY,
        consumer_secret=config.TWITTER_CONSUMER_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
    )
    return api
