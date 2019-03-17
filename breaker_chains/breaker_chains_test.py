import unittest
from unittest import TestCase
from random import choice, shuffle

from .breaker_chains import _KINGDOMS, ALLEGIANCE, extract_keyword, create_msg_packet, Ruler


class TestRunToss(TestCase):

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
        self.allegiance: ALLEGIANCE = {}

    def testDetectEmblem(self):
        pandaMsg = 'a1d22n333a4444p'
        receiver = 'lANd'
        expected = 'panda'
        self.assertEqual(expected.lower(), extract_keyword(pandaMsg, receiver),
                         'keyword should matches receiving kingdoms emblem')

    def testPreRun(self):
        ruler = Ruler(contenders=['Ice', 'Space', 'Air'])
        ruler._pre()
        self.assertTrue(ruler._subject_kingdoms, 'subject kingdoms should populate.')
        self.assertTrue(ruler._messages, 'subject kingdoms should populate.')
        self.assertTrue(ruler._msg_kingdom, 'msgs should populate.')
        self.assertTrue(ruler._contenders, 'there should be contenders.')

    def testAddContenders(self):
        ruler = Ruler()
        ruler.add_contenders(['Ice', 'Space', 'Air'])
        self.assertTrue(ruler._contenders)

    def testPostRun(self):
        ruler = Ruler(contenders=['Ice', 'Space', 'Air'])
        ruler._run()
        ruler.get_winner()
        self.assertTrue(ruler._nominations, 'there should be nominations.')
        self.assertTrue(ruler.allegiance_map, 'should have winners.')

    def testShufflePop(self):
        ruler = Ruler(contenders=['Ice', 'Space', 'Air'])
        ruler._pre()
        self.assertTrue(ruler._shuffle_choice(ruler._msg_kingdom), 'should return randomly.')

    def testBeingNomination(self):
        ruler = Ruler(contenders=['Ice', 'Space', 'Air'])
        ruler._pre()
        ruler._begin_nomination()
        self.assertTrue(ruler.ballot, 'ballot should populate.')


if __name__ == '__main__':
    unittest.main()
