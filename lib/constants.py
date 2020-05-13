import re

# Constants for use throughout the application.
# Someday maybe I'll use configs or CLI args. For now this is easier.

MAX_ATTEMPTS = 1000
MAX_STATUS_LEN = 280
BACKOFF = 2
TIMEOUT_BACKOFF = 240
KEY_PATH = r''

# What image should we put subtitles on?
# TODO: Have a series of images and choose a random one of any of them,
# so one image isn't constantly reused.
IMG_PATH = '/Users/neet/Desktop/STIUTKWikiBot/img/'
SRC_IMG = IMG_PATH + 'nyjstiutk.jpg'
DEST_IMG = SRC_IMG + '.jpg'

# Article titles the contain strings in BANNED_WORDS are skipped.
# Banned words are things that are very inappropriate, or things
# that are oversaturating the timeline, i.e. historic districts
BANNED_WORDS = ("rape", "nazi", "victim", "shootings")
BANNED_PHRASES = (r"(", "shooting", "railway station", "rugby union", "historic district", "murder of", "killing of", "rugby player", ", baron ")
PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"), ("Laos", "1"))

# I didn't want us to be limited by just one phrase, so we can
# match two. These are set to match for "Somebody That I Used To Know"
# or the longer "Now You're Just Somebody That I Used To Know"
#STIUTK_STRESSES = re.compile(r"1[02]0[12]1[12]1[12]")
#STIUTK_STRESSES_AGAIN = re.compile(r"1[12][12]120[12]11[12][12]")

STIUTK_STRESSES = re.compile(r"1[02]0[02]1[02]1[02]")
STIUTK_STRESSES_AGAIN = re.compile(r"1[02][02]120[02]11[02][02]")


CHARS_ONLY = re.compile("[^a-zA-Z]")
