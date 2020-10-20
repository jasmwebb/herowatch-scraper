#!/usr/bin/env python3
"""
Scrapes Overwatch hero data from https://overwatch.gamepedia.com/
"""

__author__ = "Jasmine Webb"
__version__ = "0.1.0"
__license__ = "MIT"

from bs4 import BeautifulSoup as bs
import requests
from re import compile


def get_abilities(hero):
    """ Scrapes and parses ability data from Overwatch. """

    # Sanitize hero name for URL
    hero = hero.title().replace(" ", "_")

    r = requests.get(f"https://overwatch.gamepedia.com/{hero}?action=edit")
    soup = bs(r.content, "html.parser")

    try:
        source_content = soup.find("textarea").contents[0].split("\n\n")
    except AttributeError:
        pass

    pattern = compile(r"{{Ability[_\s]details")

    return list(filter(pattern.search, source_content))


def main():
    """ Main entry point of the app """
    hero = "d.va"
    get_abilities(hero)
    # for index, ability in enumerate(abilities):
    #     print(index, ability)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
