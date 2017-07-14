"""
Tests of High Jump / Pole Vault competition logic
"""

from unittest import TestCase, main
from decimal import Decimal

from athlib.highjump import HighJumpCompetition
from athlib.exceptions import RuleViolation

ESAA_2015_HJ = [
    # English Schools Senior Boys 2015 - epic jumpoff ending in a draw
    # We did not include all other jumpers
    # See http://www.esaa.net/v2/2015/tf/national/results/fcards/tf15-sb-field.pdf
    # and http://www.englandathletics.org/england-athletics-news/great-action-at-the-english-schools-aa-championships
    ["place", "order", "bib", "first_name", "last_name", "team", "category",
        "1.81", "1.86", "1.91", "1.97", "2.00", "2.03", "2.06", "2.09", "2.12", "2.12", "2.10", "2.12", "2.10", "2.12"],
    ["", 1, '85', "Harry", "Maslen", "WYork", "SB",
        "o", "o", "o", "xo", "xxx"],
    ["", 2, '77', "Jake", "Field", "Surrey", "SB",
        "xxx"],
    ["1", 4, '53', "William", "Grimsey", "Midd", "SB",
        "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"],
    ["1", 5, '81', "Rory", "Dwyer", "Warks",
        "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"]
]



class HighJumpTests(TestCase):

    def test_competition_setup(self):
        """Tests basic creation of athletes with names and bibs"""

        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=0)
        self.assertEquals("Dwyer", c.jumpers[-1].last_name)

        self.assertEquals("Maslen", c.jumpers_by_bib['85'].last_name)

    def test_progression(self):
        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=0)
        h1 = Decimal("1.81")
        c.set_bar_height(h1)

        # round 1
        c.cleared('85')

        j = c.jumpers_by_bib['85']
        self.assertEquals(j.attempts_by_height, ['o'])
        self.assertEquals(j.highest_cleared, h1)

        c.failed('77')
        c.failed('77')
        c.failed('77')

        jake_field = c.jumpers_by_bib['77']
        self.assertEquals(jake_field.highest_cleared, Decimal("0.00"))
        self.assertEquals(jake_field.attempts_by_height, ['xxx'])
        self.assertTrue(jake_field.eliminated)

        harry_maslen = c.jumpers_by_bib['85']

        # attempt at fourth jump should fail
        self.assertRaises(RuleViolation, c.failed, '77')

        self.assertEquals(jake_field.place, 4)
        self.assertEquals(harry_maslen.place, 1)


    def test_replay_to_jumpoff(self):
        "Run through to where the jumpoff began - ninth bar position"
        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=9)

        # see who is winning
        maslen = c.jumpers_by_bib['85']
        field = c.jumpers_by_bib['77']
        grimsey = c.jumpers_by_bib['53']
        dwyer = c.jumpers_by_bib['81']

        self.assertEquals(field.place, 4)
        self.assertEquals(maslen.place, 3)
        self.assertEquals(grimsey.place, 1)
        self.assertEquals(dwyer.place, 1)

        # print "after 2:12 round"
        # print grimsey.failures_at_height
        # print grimsey.consecutive_failures
        # print grimsey.attempts_by_height
        # if not for jump-off rules, it would be game over
        self.assertEquals(c.remaining(), 0)



if __name__ == '__main__':
    main()
