"""
Contains class models for herowatch.py
"""

import requests
from bs4 import BeautifulSoup as bs
from re import compile


class Hero:
    """ Model of Overwatch hero """
    def __init__(self, name):
        self.name = name
        self.details = self.get_details()
        self.abilities = self.get_abilities()

    # ---- Helper methods START
    def make_request(self):
        """ Makes a request to the Overwatch wiki for specified hero's page """

        # Sanitize hero name for URL
        self.name = self.name.title().replace(" ", "_")

        r = requests.get(f"https://overwatch.gamepedia.com/"
                         f"{self.name}?action=edit")
        soup = bs(r.content, "html.parser")

        # Isolate contents of textarea tag that contains all hero information
        # Create list of each block of content
        try:
            source_content = soup.find("textarea").contents[0].split("\n\n")
        except AttributeError:
            pass

        return source_content

    def to_dict(self, content, copy_keys):
        """ Parses scraped content and returns a dictionary. """

        # Initialize final return balue
        content_dict = dict()

        for item in content:
            # Identify key-value pairs within content list
            pattern = compile(r"([^=]+)={1}(.+)")
            matches = pattern.search(item)

            try:
                key = matches.group(1).strip()
                value = matches.group(2).strip()

                # Add relevant information to final return value
                if key in copy_keys:
                    content_dict[key] = value

            # Ignore non-matches (None)
            except AttributeError:
                pass

        return content_dict
    # Helper methods END ----

    def get_details(self):
        """ Scrapes and parses general information for a single hero from the
        Overwatch wiki. Returns information as a dictionary.
        """

        # Isolate then divide information into iterable list
        content = self.make_request()[0].split("| ")

        # Define relevant information to return
        copy_keys = [
            "name", "realname", "aliases", "age", "nationality",
            "occupation", "baseofoperations", "affiliation", "relations",
            "role", "health", "armor", "shield"
        ]

        return self.to_dict(content, copy_keys)

    def get_abilities(self):
        """ Scrapes and parses ability data for a single hero from the
        Overwatch wiki. Returns information as a list of dictionaries.
        """
        content = self.make_request()

        # Define pattern that each ability detail block begins with
        pattern = compile(r"{{Ability[_\s]details")

        # Transform content into a list of only the content that contains
        # ability details
        content = list(filter(pattern.search, content))
        content = [ability.split("| ") for ability in content]

        # Define relevant details to return
        copy_keys = [
            "ability_details", "ability_name", "ability_type", "ammo",
            "ammo_drain", "cast_time", "cooldown", "damage",
            "damage_fallof_range", "duration", "fire_rate", "headshot", "heal",
            "health", "mspeed", "official_description", "pellets", "pspeed",
            "radius", "range", "reload_time", "shot_type", "spread",
            "ult_gain", "ult_req"
        ]

        return [self.to_dict(ability, copy_keys) for ability in content]