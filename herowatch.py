#!/usr/bin/env python3
"""
Scrapes Overwatch hero data from https://overwatch.gamepedia.com/
"""

__author__ = "Jasmine Webb"
__version__ = "0.1.0"
__license__ = "MIT"

from models import Hero


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

    test = Hero("sigma")
    print(test.details)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
