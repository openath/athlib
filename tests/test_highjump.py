"""
Tests of High Jump / Pole Vault competition logic
"""

from unittest import TestCase, main
from decimal import Decimal

from athlib.highjump import HighJumpCompetition
from athlib.exceptions import RuleViolation

ESAA_2015_HJ = [
    # Eglish Schools Senior Boys 2015 - epic jumpoff ending in a draw
    # We did not include all other jumpers
    # See http://www.esaa.net/v2/2015/tf/national/results/fcards/tf15-sb-field.pdf
    # and http://www.englandathletics.org/england-athletics-news/great-action-at-the-english-schools-aa-championships
    ["place", "order", "bib", "first_name", "last_name", "team", "category",
        "1.81", "1.86", "1.91", "1.97", "2.00", "2.03", "2.06", "2.09", "2.12", "2.12", "2.10", "2.12", "2.10", "2.12"],
    ["", 1, 85, "Harry", "Maslen", "WYork", "SB", "o", "o", "o", "xo", "xxx"],
    ["", 2, 77, "Jake", "Field", "Surrey", "SB", "xxx"],
    ["1", 4, 53, "William", "Grimsey", "Midd", "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"],
    ["1", 5, 81, "Rory", "Dwyer", "Warks",     "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"]
]


def create_empty_competition(matrix):
    "Creates from an array similar to above; named athletes with bibs"
    c = HighJumpCompetition()

    headers = ESAA_2015_HJ[0]
    body = ESAA_2015_HJ[1:]
    for row in body:
        kwargs = dict(zip(headers, row)[1:7])
        c.add_jumper(**kwargs)

    return c


class HighJumpTests(TestCase):

    def test_competition_setup(self):
        """Tests basic creation of athletes with names and bibs"""

        c = create_empty_competition(ESAA_2015_HJ)
        self.assertEquals("Dwyer", c.jumpers[-1].last_name)

        self.assertEquals("Maslen", c.jumpers_by_bib[85].last_name)

    def test_progression(self):
        c = create_empty_competition(ESAA_2015_HJ)
        h1 = Decimal("1.81")
        c.set_bar_height(h1)

        # round 1
        c.cleared(85)

        j = c.jumpers_by_bib[85]
        self.assertEquals(j.attempts_by_height, ['o'])
        self.assertEquals(j.highest_cleared, h1)

        c.failed(77)
        c.failed(77)
        c.failed(77)

        jake_field = c.jumpers_by_bib[77]
        self.assertEquals(jake_field.highest_cleared, Decimal("0.00"))
        self.assertEquals(jake_field.attempts_by_height, ['xxx'])
        self.assertTrue(jake_field.eliminated)

        harry_maslen = c.jumpers_by_bib[85]

        # attempt at fourth jump should fail
        self.assertRaises(RuleViolation, c.failed, 77)

        self.assertEquals(jake_field.place, 4)
        self.assertEquals(harry_maslen.place, 1)


    def test_replay_to_jumpoff(self):
        "Run through to where the jumpoff began"
        c = create_empty_competition(ESAA_2015_HJ)

        headers = ESAA_2015_HJ[0]
        text_heights = headers[7:16]  # up to first 2:12
        body = ESAA_2015_HJ[1:]
        info = []
        for row in body:
            dikt = dict(zip(headers, row))
            info.append(dikt)

        # print info[-1]
        for text_height in text_heights:
            c.set_bar_height(Decimal(text_height))
            #  print "height set to", text_height
            for attempt in range(3):
                #  print " try %d" % (attempt + 1)
                for jumper in info:
                    bib = jumper['bib']
                    atts = jumper.get(text_height, '')   # they may not be listed
                    #print "bib %s, height %s got %s" % (bib, text_height, atts)
                    if not atts:  # they passed at this one
                        continue
                    #print "   %s at %s: attempts %s" % (bib, text_height, atts)
                    if attempt < len(atts):
                        result = atts[attempt]
                        #print "   %s: attempt %d: %s" % (bib, (attempt + 1), result)
                        if result == 'x':
                            c.failed(bib)
                        elif result == 'o':
                            c.cleared(bib)
                        elif result == 'r':
                            c.retired(bib)
                        else:
                            raise RuleViolation("Unknown jump result code '%s'" % result)
            # print "end of %s round" % text_height


        # see who is winning
        maslen = c.jumpers_by_bib[85]
        field = c.jumpers_by_bib[77]
        grimsey = c.jumpers_by_bib[53]
        dwyer = c.jumpers_by_bib[81]

        self.assertEquals(field.place, 4)
        self.assertEquals(maslen.place, 3)
        self.assertEquals(grimsey.place, 1)
        self.assertEquals(dwyer.place, 1)


        # print "after 2:12 round"
        # print grimsey.failures_at_height
        # print grimsey.consecutive_failures
        # print grimsey.attempts_by_height
        # # if not for jump-off rules, it would be game over
        # self.assertEquals(c.remaining(), 0)




if __name__ == '__main__':
    main()
