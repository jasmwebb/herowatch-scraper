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


def info_to_dict(info):
    """ Parses information request response into dictionary. """

    # Divide information into iterable list
    info = info.split("| ")

    # Initialize final return balue
    info_dict = dict()

    # Define relevant information to return
    copy_categories = [
        "name", "realname", "aliases", "age", "nationality",
        "occuptation", "baseofoperations", "affiliation", "relations"
        "role", "health", "armor", "shield"
    ]

    for item in info:
        # Isolate key-value pairs within information list
        pattern = compile(r"(.*)=(.*)")
        matches = pattern.search(item)

        try:
            key = matches.group(1).strip()
            value = matches.group(2).strip()

            # Add relevant information to final return value
            if key in copy_categories:
                info_dict[key] = value
        except AttributeError:
            pass

    return info_dict


def main():
    """ Main entry point of the app """
    heroes = [
        "d.va", "orisa", "reinhardt", "roadhog", "sigma",
        "winston", "wrecking ball", "zarya",
        "ashe", "bastion", "doomfist", "echo", "genji",
        "hanzo", "junkrat", "mccree", "mei", "pharah",
        "reaper", "soldier: 76", "sombra", "symmetra",
        "torbjorn", "tracer", "widowmaker",
        "ana", "baptiste", "brigitte", "lucio", "mercy",
        "moira", "zenyatta"
    ]

    for hero in heroes:
        info = get_basic_info(hero)
        info_dict = info_to_dict(info)
        print(info_dict)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
