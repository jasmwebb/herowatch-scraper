"""
Contains class models for herowatch.py
"""

import requests
from bs4 import BeautifulSoup as bs
from re import compile, S


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
        source_content = soup.find("textarea").contents[0]

        return source_content

    def to_dict(self, content, copy_keys):
        """ Parses list of scraped content and returns a dictionary. """

        # Initialize final return balue
        content_dict = dict()

        for item in content:
            item = item.lstrip("|")

            # Identify key-value pairs within content list
            pattern = compile(r"([^=]+)=(.+)", flags=S)
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
        content = self.make_request()
        pattern = compile(
            r"(?<={{Infobox character\n)(.+?)\n*}}\n(?='''|\[\[)",
            flags=S
        )

        try:
            content = pattern.search(content).group(1).split("\n")
        # Ignore non-matches (None)
        except AttributeError:
            pass

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
        pattern = compile(
            r"(?<={{Ability_details\n|{{Ability details\s)(.+?)\n}}",
            flags=S
        )

        # Transform content into a list of only the content that contains
        # ability details
        content = pattern.findall(content)

        # Define relevant details to return
        copy_keys = [
            "ability_details", "ability_name", "ability_type", "ammo",
            "ammo_drain", "cast_time", "cooldown", "damage",
            "damage_fallof_range", "duration", "fire_rate", "headshot", "heal",
            "health", "mspeed", "official_description", "pellets", "pspeed",
            "radius", "range", "reload_time", "shot_type", "spread",
            "ult_gain", "ult_req"
        ]

        # Transform each ability into a list of unseparated key, value pairs
        try:
            content = (ability.split("\n|") for ability in content)
        # Ignore non-matches (None)
        except AttributeError:
            pass

        # Transform into list of dictionaries
        dict_content = [
            self.to_dict(ability, copy_keys) for ability in content
        ]

        # Transform string value of ability_details into a list of strings
        for ability in dict_content:
            if "ability_details" in ability:
                ability["ability_details"] = (
                    list(filter(None, ability["ability_details"].split("* ")))
                )

        return dict_content
