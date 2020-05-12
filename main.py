#!/usr/bin/env python3
from lib.constants import BACKOFF, MAX_ATTEMPTS, MAX_STATUS_LEN, TIMEOUT_BACKOFF
from typing import Tuple
from lib import twitter
from lib import images
from lib import words

import wikipedia
import time
import sys
import os

def main():
    title = search_for_stiutk(MAX_ATTEMPTS, BACKOFF)
    img = images.make_subs(title)
    status_text = "\n".join((title[0], words.get_wiki_url(title[0])))

    if len(status_text) > MAX_STATUS_LEN:
        status_text = title[0]

    title[0] = status_text

    _ = twitter.send_tweet(title)

def search_for_stiutk(attempts=MAX_ATTEMPTS, backoff=BACKOFF) -> Tuple[str, int]:
    """Loop MAX_ATTEMPT times, searching for a STIUTK meter wikipedia title.

    Args:
        Integer: attempts, retries remaining.
        Integer: backoff, seconds to wait between each loop.
    Returns:
        Tuple[str, int] where the first member is the string name
        of the Wiki article, and the 2nd is which meter it matches;
        "Somebody That I Used To Know" (1) or
        "Now You're Just Somebody That I Used To Know" (2)?
    """
    for attempt in range(attempts):
        print(f"\r{str(attempt * 25)} articles fetched...", end="")
        sys.stdout.flush()
        title = crawl_for_stiutk()

        time.sleep(backoff)

        if type(title) != None:
            continue

        try:
            if type(title[0]) == str and len(title[0]) > 1:
                print(f"\nMatched: {title[0]}")
                return title
        except TypeError:
            pass
        except Exception as e:
            print("Exception: " + str(e))

    print(f"\nNo matches found.")
    sys.exit(1)


def crawl_for_stiutk() -> Tuple[str, int]:
    """Get 10 random wiki titles, check if any of them isSTIUTK().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in STIUTK meter, return the title and which meter is matched.
    Otherwise, return False.

    Args:
        None
    Returns:
        Tuple[str, int] where the first member is the string name
        of the Wiki article, and the second is which meter it matches;
        "Somebody That I Used To Know" (1) or
        "Now You're Just Somebody That I Used To Know" (2)?
    """
    wikipedia.set_rate_limiting(True)

    try:
        titles = wikipedia.random(25)
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Wikipedia timout exception: {e}")
        time.sleep(TIMEOUT_BACKOFF)
        main()
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")
        sys.exit(1)

    for title in titles:
        stiutk_type = words.is_stiutk(title)
        if stiutk_type[0]:
            return (title, stiutk_type[1])

if __name__ == "__main__":
    main()
