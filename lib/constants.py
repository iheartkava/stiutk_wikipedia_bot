import re

### General
MAX_ATTEMPTS = 10		# Max number of attempts before sleeping.
MAX_STATUS_LEN = 280	# Max number of characters for our tweet.
FETCH = 25				# How many random articles from wiki to fetch at a time.
BACKOFF = 1				# How many seconds to sleep during an attempt.
TIMEOUT_BACKOFF = 240	# How many seconds to sleep if we get a timeout from wiki.
KEY_PATH = r''			# Path to twitter keyfile.
###

### Image-related
# We look within SRC_DIR and pick any image from that directory at random, so be
# careful where you point this.
IMG_PATH = '/Users/neet/Desktop/STIUTKWikiBot/img/' # Path to our image directory.
FONT = '/Windows/Fonts/trebucit.ttf'				# Path to desired font.
SRC_DIR = IMG_PATH + 'src/'		# Path to source images from within IMG_PATH.
DEST_DIR = IMG_PATH + 'out/'	# Path to put new images within IMG_PATH.
MAX_FILE_LEN = 36				# Maximum file name length. Windows as a limit of 255
								# incl path, remember!
###

# Article titles the contain strings in BANNED_WORDS are skipped.
# Banned words are things that are very inappropriate, or things
# that are oversaturating the timeline, i.e. historic districts
BANNED_WORDS = ("rape", "nazi", "victim", "shootings")
BANNED_PHRASES = (r"(", "shooting", "railway station", "rugby union",
					"historic district", "murder of", "killing of",
					"rugby player", ", baron ")

PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"), ("Laos", "1"))

# Simply add your own regex in to check for stresses.
# The order is important:
# - STRESSES[n][0] is the number of syllables,
# - STRESSES[n][1] is the regex to search for
# - STRESSES[n][2] determines whether any text needs to be added
# - STRESSES[n][3] if [2] is True, this contains the text to be added.
# - STRESSES[n][4] is the original lyric, so we can post it and have context.
STRESSES = [
	# But You Didn't Have To Cut Me Off
	(9, re.compile(r"[12][12]10[12]211[12]"), False, "",
		"But You Didn't Have To Cut Me Off"),

	# And I Don't Even Need Your Love
	(8, re.compile(r"01[12]101[12][12]"), False, "",
		"And I Don't Even Need Your Love"),

	# Your Love
	(2, re.compile(r"[12]1"), True, "And I Don't Even Need",
		"(And I Don't Even Need) Your Love"),

	# You Can Get Addicted To A Certain Kind Of Sadness
	(14, re.compile(r"1110[12]0[12]01[02]1[12]1[02]"), False, "",
		"You Can Get Addicted To A Certain Kind Of Sadness"),

	# A Certain Kind Of Sadness
	(7, re.compile(r"01[02]1[12]1[02]"), True, "You Can Get Addicted To",
		"(You Can Get Addicted To) A Certain Kind Of Sadness"),

	# Well You Said That We Would Still Be Friends
	(9, re.compile(r"1[12][12][12][12][12]111"), False, "",
		"Well You Said That We Would Still Be Friends"),

	# We Would Still Be Friends
	(5, re.compile(r"[12][12]111"), True, "Well You Said That",
		"(Well You Said That) We Would Still Be Friends"),

	# No, You Didn't Have To Stoop So Low
	(9, re.compile(r"[12][12]10[12][12]111"), False, "",
		"No, You Didn't Have To Stoop So Low"),

	# Somebody That I Used To Know
	(8, re.compile(r"[12][12][02][012][012][12][012][12]"), True, "Now You're Just",
		"(Now You're Just) Somebody That I Used To Know"),

	# Now You're Just Somebody That I Used To Know
	(11, re.compile(r"1[12][12]1201[12][12][120][12]"), False, "",
		"Now You're Just Somebody That I Used To Know")
]

# Don't change this one.
CHARS_ONLY = re.compile("[^a-zA-Z]")
