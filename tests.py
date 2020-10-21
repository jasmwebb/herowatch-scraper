"""
This file contains tests for an Overwatch hero data scraper.
"""
import unittest
from main import get_abilities, get_basic_info
from re import compile


class TestResponse(unittest.TestCase):
    """ Ensures every ability is scraped for each hero. """

    def setUp(self):
        self.heroes_abilities = {
            "d.va": 8, "orisa": 5, "reinhardt": 6, "roadhog": 5, "sigma": 5,
            "winston": 4, "wrecking ball": 6, "zarya": 6,
            "ashe": 5, "bastion": 6, "doomfist": 6, "echo": 6, "genji": 6,
            "hanzo": 6, "junkrat": 5, "mccree": 5, "mei": 5, "pharah": 5,
            "reaper": 5, "soldier: 76": 5, "sombra": 6, "symmetra": 5,
            "torbjorn": 6, "tracer": 4, "widowmaker": 5,
            "ana": 4, "baptiste": 6, "brigitte": 7, "lucio": 6, "mercy": 7,
            "moira": 5, "zenyatta": 5
        }

    def test_get_abilites(self):
        """ Compare number of scraped abilities to true number of abilities.
        """
        self.maxDiff = None

        for hero, num_abilities in self.heroes_abilities.items():
            got_abilities = len(get_abilities(hero))
            with self.subTest(num_abilities=num_abilities):
                self.assertEqual(num_abilities, got_abilities,
                                 f"{hero.title()} has {num_abilities} "
                                 f"abilities, not {got_abilities}.")

    def test_get_basic_info(self):
        """ Ensure retured content is the infobox content. """
        for hero in self.heroes_abilities.keys():
            got_basic_info = get_basic_info(hero)
            pattern = compile(r"{{Infobox character")

            with self.subTest(hero=hero):
                self.assertIsNotNone(pattern.search(got_basic_info),
                                     f"Wrong information for {hero.title()}")


if __name__ == '__main__':
    unittest.main()
