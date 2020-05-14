from lib.constants import (
	BANNED_WORDS,
	BANNED_PHRASES,
	CHARS_ONLY,
	PRONUNCIATION_OVERRIDES,
	STRESSES
)
from num2words import num2words as n2w
from urllib.parse import quote_plus
from typing import Tuple, List
from random import choice
from sys import stdout

import pronouncing
import urllib
import re

def is_stiutk(title: str) -> List:
	"""
	Determine if a string has the same cadence as any line we search for.

	Parameters:
	  title (str): The string we want to check.

	Returns:
	  List where the first element is the title string, and the second element
	  is the tuple from lib.constants.STRESSES it matched against.
	"""
	if contains_banned(title):
		return None

	title = clean_str(title)
	title_stresses = get_title_stresses(title)
	matches = []

	# If there's an A, that means get_word_stresses failed on a word, so we
	# have to discard it.
	if not title_stresses or "A" in title_stresses:
		return None

	# Check against every item in STRESSES.
	for pattern in STRESSES:
		if len(title_stresses) != pattern[0]:
			continue

		# If there's a match there might be more than one, so we append it
		# rather than just straight-up returning here.
		if pattern[1].match(title_stresses):
			matches.append(pattern)

	# I don't even know if there can be more than one match anymore, but in case
	# there is (and because I don't wanna change it and it works), return a
	# random match that has been appended.
	if matches:
		return [title, choice(matches)]

	return None


def contains_banned(title: str) -> bool:
	"""
	Check for any of the banned phrases found in lib/constants.py

	This implementation is slow, but is was fast to write and I don't care about
	speed for this script.

	Parameters:
	  title (str): The string to check.

	Returns:
	  True if there are banned words or phrase, otherwise False.
	""" 

	def _contains_banned_word(title: str):
		for word in title.split():
			word = CHARS_ONLY.sub("", word.lower())
			if word in BANNED_WORDS:
				return True
		return False

	def _contains_banned_phrase(title: str):
		for phrase in BANNED_PHRASES:
			if phrase in title.lower():
				return True
		return False

	return _contains_banned_word(title) or _contains_banned_phrase(title)


def get_title_stresses(title: str) -> str:
	"""
	Return the combined stresses of every word in a sentence.

	Parameters:
	  title (str): The sentence to check for.

	Returns:
	  String of 0s, 1s, and 2s, which represent the stresses of each word.
	  If there is an error or word that can't be detected, the string will
	  Contain and A and be discarded.
	"""
	title_words = title.split()
	title_stresses = ""

	while title_words:
		word = title_words.pop(0)
		word_stresses = get_word_stresses(word)

		# If word was a long number, it may have been parsed into several words.
		if isinstance(word_stresses, list):
			title_words = word_stresses + title_words
		else:
			title_stresses += get_word_stresses(word)

	return title_stresses


def get_word_stresses(word: str) -> str:
	"""
	Using the pronouncing library, get the stress pattern of a single word.
	Numbers will be changed into words, e.g. 10 -> ten, and then the stress
	of that checked. If a number is 4 digits, it will be treated as a year, e.g.
	1918 -> "nineteen eighteen".

	Parameters:
	  word (str): The word to check.

	Returns:
	  A string of 0s, 1s, or 2s, representing the stress pattern of any given
	  word. If a word isn't recognized, or for any other reason there's an
	  error, the string will contain an A for easy checking.

	"""

	# If the word is "500", numbers_to_words changes that to "five hundred", two
	# seperate words. Return a list of every word, so get_title_stresses() can
	# go over them again.
	word = numbers_to_words(word)
	if " " in word:
		return word.split()

	# We want to forceably change the stress for certain words (found in
	# constants.py).
	for override, stresses in PRONUNCIATION_OVERRIDES:
		if word.lower() == override.lower():
			return stresses

	phones = pronouncing.phones_for_word(word)
	if not phones:
		return "A"

	stresses = pronouncing.stresses(phones[0])
	return stresses


def numbers_to_words(word: str) -> str:
	"""
	Change numbers into words, e.g. 10 -> "ten". 4-digit numbers will be treated
	as years, e.g. 1918 -> "nineteen eighteen".
	Also handles ordinals, e.g. "3rd" -> "third".

	Parameters:
	  word (str): The number, as a string, to convert to words.

	Returns:
	  Words for the number, e.g. numbers_to_words("10") returns "ten".
	  On any error, return "A".
	"""
	ordinal_number_endings = ("nd", "rd", "st", "th")

	# If the number is 4 digits, treat it as a word. Catch any exceptions.
	if word.isdigit():
		if len(word) == 4:
			try:
				word = n2w(word, to="year")
			except Exception:
				return "A"
		# It's not 4 digits, so just a normal word.
		else:
			try:
				word = n2w(word)
			except Exception:
				return "A"

	# Check if the last 2 characters are ordinals and handle that.
	if word[:-2].isdigit() and word[-2:] in ordinal_number_endings:
		word = word[-2:]
		try:
			word = n2w(word, to="ordinal")
		except Exception:
			return "A"

	return word


def clean_str(s: str) -> str:
	"""
	Remove characters the pronouncing library can't handle.

	Parameters:
	  s (str): The string to sanitize.

	Returns:
	  The sanitized string.
	"""
	DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";", "."]
	SWAP_CHARS = [("-", " ")]

	for char in DEL_CHARS:
		s = s.replace(char, "")

	for char, replacement in SWAP_CHARS:
		s = s.replace(char, replacement)

	return s


def get_wiki_url(title: str) -> str:
	"""
	Turn a string into a valid URL, appending it onto wikipedia's URL.

	Parameters:
	  title (str): The string to become a URL.

	Returns:
	  URL to wikipedia.
	"""
	title = title.replace(" ", "_")
	title = quote_plus(title)
	return "https://en.wikipedia.org/wiki/" + title
