from lib.constants import KEY_PATH
from collections import namedtuple
from typing import Tuple

import tweepy
import sys

TwitterAuth = namedtuple(
    "TWITTER",
    ["consumer_key", "consumer_secret", "access_token", "access_token_secret"],
)


#def get_twitter_credentials(keyfile=KEY_PATH):
def get_twitter_credentials():
    return True
    '''   try:
        with open(keyfile, "r") as f:
            keys = f.read()
    except Exception as e:
        sys.stderr.write(f"Exception fetching Twitter keys: {e}")
        sys.exit(1)

    keys = keys.split()
    keys = [key.strip() for key in keys]

    return TwitterAuth(
        consumer_key=keys[0],
        consumer_secret=keys[1],
        access_token=keys[2],
        access_token_secret=keys[3],
    )'''


#def send_tweet(tweet_text: str, image_path=""):
def send_tweet(tweet_stuffs: Tuple[str, int]):
    print(tweet_stuffs[0])
    print(tweet_stuffs[1])
    '''"""Post some text, and optionally an image to twitter.

    Args:
        tweet_stuffs: Tuple[str, int] String title and Int matched meter type.
        image_path: String, path to image on disk to be posted to twitter
    Returns:
        tweepy.status object, contains response from twitter request
    """
    TWITTER = get_twitter_credentials()
    auth = tweepy.OAuthHandler(TWITTER.consumer_key, TWITTER.consumer_secret)
    auth.set_access_token(TWITTER.access_token, TWITTER.access_token_secret)

    api = tweepy.API(auth)

    if image_path:
        return api.update_with_media(filename=image_path, status=tweet_text)
    else:
        return api.update_status(tweet_text)

    return api.update_status(tweet_text)'''
