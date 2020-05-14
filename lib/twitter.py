from lib.constants import KEY_PATH
from lib.words import get_wiki_url
from collections import namedtuple
from typing import Tuple, List

import tweepy
import sys

TwitterAuth = namedtuple(
    "TWITTER",
    ["consumer_key", "consumer_secret", "access_token", "access_token_secret"],
)


#def get_twitter_credentials(keyfile=KEY_PATH):
def get_twitter_credentials():
    """
    Get twitter credentials from keyfile.

    """
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
def send_tweet(tweet_stuffs: List, image_path=""):
    """
    Post text and optionally an image to twitter.

    Parameters:
      tweet_stuffs (List): Our monstrosity of a data type containing the title
      of the wiki page and many many more details........ God this sucks

      image_path (str): Optionally the path to the image to be uploaded along
      with the tweet.

    Returns:
      tweepy.status object, contains response from twitter request.
    """
    msg = tweet_stuffs[0]
    if tweet_stuffs[1][2] == True:
        msg = f"{tweet_stuffs[1][3]} {msg}"

    print("-------------------")
    print(f"{msg}\n{tweet_stuffs[1][4]}\n{get_wiki_url(tweet_stuffs[0])}")
    print(f"{image_path}")
    print("-------------------")

    return True
    """
    TWITTER = get_twitter_credentials()
    auth = tweepy.OAuthHandler(TWITTER.consumer_key, TWITTER.consumer_secret)
    auth.set_access_token(TWITTER.access_token, TWITTER.access_token_secret)

    api = tweepy.API(auth)

    if image_path:
        return api.update_with_media(filename=image_path, status=tweet_text)
    else:
        return api.update_status(tweet_text)

    return api.update_status(tweet_text)
    """
