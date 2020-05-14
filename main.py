#!/usr/bin/env python3
from lib.constants import (
	FETCH,
	BACKOFF,
	MAX_ATTEMPTS,
	MAX_STATUS_LEN,
	TIMEOUT_BACKOFF
)

from typing import Tuple, List
from lib import twitter
from lib import images
from lib import words

import wikipedia
import random
import time
import sys
import os
import re

def main():
	while True:
		loop()
		print("\t -- We Sleeping Now --")
		time.sleep(10)

def loop():
	title = search_for_stiutk(MAX_ATTEMPTS, BACKOFF)
	if not title:
		print(f"\nNo matches found.")
		return False

	img = images.make_subs(title)
	_ = twitter.send_tweet(title, img)
	return True

def search_for_stiutk() -> List:
	"""
	Make attempts to crawl for matching titles.

	Parameters:
	  None.

	Returns:
	  Our hell-monstrosity list/tuple, or None on failure.
	"""
	matches = [ ]	
	for attempt in range(attempts):
		match = crawl_for_stiutk(attempt)
		time.sleep(backoff)

		if not match:
			continue

		try:
			if type(match[0]) == str and len(match[0]) > 1:
				matches.append(match)
		except TypeError:
			print(f"TypeError: {str(type(match))}")
			pass
		except Exception as e:
			print(f"Exception: " + str(e) + '\n')

	if not matches:
		return None

	return best_match(matches)


def get_wiki_titles() -> List:
	"""
	Get a list of random titles from wikipedia. Change number in lib/constants.py

	Parameters:
	  None.

	Returns:
	  List of titles.
	"""
	wikipedia.set_rate_limiting(True)

	try:
		titles = wikipedia.random(FETCH)
	except wikipedia.exceptions.HTTPTimeoutError as e:
		print(f"Wikipedia timout exception: {e}")
		time.sleep(TIMEOUT_BACKOFF)
		sys.exit(1)
	except wikipedia.exceptions.WikipediaException as e:
		print(f"Wikipedia exception: {e}")
		sys.exit(1)
	except Exception as e:
		print(f"Exception while fetching wiki titles: {e}")
		sys.exit(1)

	return titles

def best_match(matches: List) -> List:
	"""
	Run through our monstrisity hell list/tuple, finding which one matches with
	the longest number of syllables. I did this to myself.

	Paramters:
	  matches (List): A list of... a list of lists of string/tuple. Hell.

	Returns:
	  The string/tuple list matching the most syllables.
	"""
	i = 0
	n = 0
	b = 0

	for match in matches:
		if match[1][0] > b:
			b = match[1][0]
			i = n
		n += 1

	return matches[i]

def crawl_for_stiutk(total: int) -> List:
	"""
	Check every title from get_wiki_titles, then return the best matching.

	Parameters:
	  total (int): Just for output, how many times have we done this?

	Returns:
	  Our best matching title in our classic hellish string/tuple list.
	"""
	matches = [ ]
	for title in get_wiki_titles():
		match = words.is_stiutk(title)
		if match:
			print(f"\nAnother match: {match[0]} ({match[1][4]})")
			matches.append(match)

	if matches:
		return best_match(matches)

	return None

if __name__ == "__main__":
	main()
