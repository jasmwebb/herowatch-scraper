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


def make_request(hero):
    """ Makes a request to the Overwatch wiki. """

    # Sanitize hero name for URL
    hero = hero.title().replace(" ", "_")

    r = requests.get(f"https://overwatch.gamepedia.com/{hero}?action=edit")
    soup = bs(r.content, "html.parser")

    # Isolate contents of textarea tag that contains all hero information
    # Create list of each block of content
    try:
        source_content = soup.find("textarea").contents[0].split("\n\n")
    except AttributeError:
        pass

    return source_content


def get_abilities(hero):
    """ Scrapes and parses ability data for a single hero from the Overwatch
    wiki.
    """
    content = make_request(hero)

    # Define pattern that each ability info block begins with
    pattern = compile(r"{{Ability[_\s]details")

    # Create and return a list of only the blocks that contain pattern
    return list(filter(pattern.search, content))


def get_basic_info(hero):
    """ Scrapes and parses general information for a single hero from the
    Overwatch wiki.
    """
    content = make_request(hero)

    return content[0]


def main():
    """ Main entry point of the app """
    test_hero = "genji"
    print(get_basic_info(test_hero))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
