"""
This file contains tests for an Overwatch hero data scraper.
"""
import unittest
from models import Hero


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

    def test_get_abilities(self):
        """ Compare number of scraped abilities to true number of abilities.
        """
        self.maxDiff = None

        for hero, num_abilities in self.heroes_abilities.items():
            test_hero = Hero(hero)
            test_num_abilities = len(test_hero.abilities)

            with self.subTest(num_abilities=num_abilities):
                self.assertEqual(num_abilities, test_num_abilities,
                                 f"{hero.title()} has {num_abilities} "
                                 f"abilities, not {test_num_abilities}.")

    def test_get_details(self):
        """ Compare keys of scraped details to keys of universal/required
        details.
        """
        universal_details_keys = {
            "name", "age", "occupation", "baseofoperations",
            "affiliation", "role", "health"
        }

        for hero in self.heroes_abilities.keys():
            test_hero = Hero(hero)
            test_details_keys = test_hero.details.keys()

            with self.subTest(hero=hero):
                self.assertTrue(universal_details_keys
                                .issubset(test_details_keys),
                                "Missing required details for {0}: {1}"
                                .format(hero.title(),
                                        universal_details_keys
                                        .difference(test_details_keys)
                                        )
                                )


if __name__ == '__main__':
    unittest.main()
