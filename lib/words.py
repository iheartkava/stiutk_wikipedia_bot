from lib.constants import (
    BANNED_WORDS,
    BANNED_PHRASES,
    CHARS_ONLY,
    PRONUNCIATION_OVERRIDES,
    STIUTK_STRESSES,
    STIUTK_STRESSES_AGAIN
)
from num2words import num2words as n2w
from urllib.parse import quote_plus
from typing import Tuple
from sys import stdout

import pronouncing
import urllib
import re

def is_stiutk(title: str) -> Tuple[bool, int]:
    """Checks if a Wikipedia page title has the same stress pattern as STIUTK
    >>> is_stiutk('Somebody That I Used To Know')
    True

    >>> is_stiutk("Now You're Just Somebody That I Used To Know")
    True

    >>> is_stiutk('Romeo, Romeo, wherefore art thou, Romeo?')
    False
    """
    if contains_banned(title):
        return (False, 0)

    title = clean_str(title)
    title_stresses = get_title_stresses(title)

    """Remember! We can match two different patterns. Either the shorter
    "Somebody That I Used To Know", but the longer "Now You're Just Somebody
    That I Used To Know" is valid as well. That's why this part is a little
    bit weird...
    It returns a Touple (bool, int) where bool indicates if it's a valid stiutk
    title, and int indicates if it's the long or short pattern.
    """
    if (not title_stresses) or ((len(title_stresses) != 8) and
                                (len(title_stresses) != 11)):
        return (False, 0)

    if STIUTK_STRESSES.match(title_stresses):
        return (True, 1)
    elif STIUTK_STRESSES_AGAIN.match(title_stresses):
        return (True, 2)
    else:
        return (False, 0)

def contains_banned(title: str) -> bool:
    """Return True if banned words or phrases in string.

    This implementation is slow, but is was fast to write and I don't care about
    speed for this script.
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
    """Takes a wikipedia title and gets the combined stresses of all words.

    >>> get_title_stresses('Teenage Mutant Ninja Turtles')
    '12101010'

    Args:
        title: String, title of a wikipedia page.
    Returns:
        String, stresses of each syllable as 0, 1, and 2s.
    """
    title_words = title.split()
    title_stresses = ""
    while title_words:
        if len(title_stresses) > 11:
           return None

        word = title_words.pop(0)
        word_stresses = get_word_stresses(word)

        # If word was a long number, it may have been parsed into several words.
        if isinstance(word_stresses, list):
            title_words = word_stresses + title_words
        else:
            title_stresses += get_word_stresses(word)

    return title_stresses


def get_word_stresses(word: str) -> str:
    word = numbers_to_words(word)
    if " " in word:
        return word.split()

    for override, stresses in PRONUNCIATION_OVERRIDES:
        if word.lower() == override.lower():
            return stresses

    try:
        phones = pronouncing.phones_for_word(word)
        stresses = pronouncing.stresses(phones[0])
    except IndexError:
        # Hacky way of discarding candidate title
        return "1111111111"

    return stresses


def numbers_to_words(word) -> str:
    ordinal_number_endings = ("nd", "rd", "st", "th")
    if word.isdigit():
        if len(word) == 4:
            try:
                word = n2w(word, to="year")
            except Exception:
                # Hacky way of discarding candidate title
                return "1111111111"
        else:
            try:
                word = n2w(word)
            except Exception:
                # Hacky way of discarding candidate title

                return "1111111111"
    if word[:-2].isdigit() and word[-2:] in ordinal_number_endings:
        word = word[-2:]
        try:
            word = n2w(word, to="ordinal")
        except Exception:
            # Hacky way of discarding candidate title
            return "1111111111"

    return word


def clean_str(s: str) -> str:
    """Remove characters that the pronouncing dictionary doesn't like.

    This isn't very efficient, but it's readable at least. :-)

    >>> clean_str('fooBar123')
    'fooBar123'

    >>> clean_str('Hello ([world])')
    'Hello world'

    >>> clean_str('{hello-world}')
    'hello world'

    Args:
        s: String to be stripped of offending characters
    Returns:
        String without offending characters
    """
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";", "."]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        s = s.replace(char, replacement)

    return s


def get_wiki_url(title: str) -> str:
    title = title.replace(" ", "_")
    title = quote_plus(title)
    return "https://en.wikipedia.org/wiki/" + title
