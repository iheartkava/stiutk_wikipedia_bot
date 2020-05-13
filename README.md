## STIUTK Wikipedia Bot

Similar to https://github.com/catleeball/tmnt_wikipedia_bot but search for
"(Now You're Just) Somebody That I Used To Know" instead of "Teeange
Mutant Ninja Turtles".

### Why

For fun! This idea came to me, falling asleep at 7am, as a vision
of a Twitter account that doesn't exist, but should. Of course
I needed to  make it a reality.
Inspired by https://github.com/catleeball/tmnt_wikipedia_bot
which in turn was inspired by https://xkcd.com/1412/

### How

When it runs, it:
- Pulls 25 random Wikipedia article titles
- Checks if they have the same stress pattern as Gotye's *Somebody That*
  *I Used To Know*
  - If not, pull 10 more articles ad infinitum until a match is found
- Create fake subtitles on Gotye's music video

### Environment

This script requires the following:

- Python >= 3.7
  - Earlier may work, only tested on 3.7
- Via PyPi:
  - pronouncing
  - num2words
  - PIL

### Configuration

Configuration is entirely `lib/constants.py`.

### Caveats

Performance could be improved, but it doesn't need to be
a blazing fast optimized program. Most if it will be spent
waiting to get more article titles, anyway...

### TODO

  - Find an effective pattern, I get very few matches currently...
  - Improved configuration
  - Use multiple images instead of one

Super bonus points:
  - CI
  - cache of titles : stresses
