#!/usr/bin/env python3
"""
Scrapes Overwatch hero data from https://overwatch.gamepedia.com/ and stores
data in a JSON file.
"""

__author__ = "Jasmine Webb"
__version__ = "0.1.0"
__license__ = "MIT"

from json import dump
from models import Hero


def generate_hero(heroes):
    """ Generates hero data while iterating through give hero list. """
    for hero in heroes:
        hero = Hero(hero)
        yield (
            hero.name,
            {
                "details": hero.details,
                "abilities": hero.abilities
            }
        )


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

    # Write scraped hero data to JSON file
    with open("heroes.json", "w") as heroes_json:
        dump(
            {k: v for (k, v) in generate_hero(heroes)},
            heroes_json
        )


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
