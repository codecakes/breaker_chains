import unittest
from random import choice

from .breaker_chains import _KINGDOMS, extract_keyword


class TestRunToss(unittest.TestCase):

    def setUp(self):
        """
        LAND emblem - Panda,
        WATER emblem - Octopus,
        ICE emblem - Mammoth,
        AIR emblem - Owl,
        FIRE emblem - Dragon
        Space emblem - Gorilla
        """
        self.kingdoms = _KINGDOMS
        self.kingdoms_owners = list(self.kingdoms.keys())
        self.pick_one = lambda: choice(self.kingdoms_owners)

    def testDetectEmblem(self):
        pandaMsg = 'a1d22n333a4444p'
        receiver = 'lANd'
        expected = 'panda'
        self.assertEqual(expected.lower(), extract_keyword(pandaMsg, receiver),
                         'keyword should matches receiving kingdoms emblem')


if __name__ == '__main__':
    unittest.main()
