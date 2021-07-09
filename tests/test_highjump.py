# coding: utf8
"""
Tests of High Jump / Pole Vault competition logic
"""

from unittest import TestCase, main
from decimal import Decimal

from athlib.highjump import HighJumpCompetition, _012
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
    ["1", 5, '81', "Rory", "Dwyer", "Warks", "SB",
        "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"]
    ]
_1066 = [
    #based on above, but we have a winner
    ["place", "order", "bib", "first_name", "last_name", "team", "category",
        "1.81", "1.86", "1.91", "1.97", "2.00", "2.03", "2.06", "2.09", "2.12", "2.12", "2.10", "2.12", "2.10", "2.12", "2.11"],
    ["", 1, '85', "Dafydd", "Briton", "WYork", "SB",
        "o", "o", "o", "xo", "xxx"],
    ["", 2, '77', "Jake", "Saxon", "Surrey", "SB",
        "xxx"],
    ["1", 4, '53', "William", "Norman", "Midd", "SB",
        "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x", "x"],
    ["1", 5, '81', "Harald", "England", "Warks", "SB",
        "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x", "o"]
    ]

RIO_MENS_HJ = [  # pasted from Wikipedia
    ["place", "order", "bib", "first_name", "last_name", "team", "category", "2.20", "2.25", "2.29", "2.33", "2.36", "2.38", "2.40", "best", "note"],
    ["1", 7, 2197, "Derek", "Drouin", "CAN", "M", "o", "o", "o", "o", "o", "o", "x", 2.38, ""],
    ["2", 9, 2878, "Mutaz", "Essa Barshim", "QAT", "M", "o", "o", "o", "o", "o", "xxx", "", 2.36, ""],
    ["3", 3, 3026, "Bohdan", "Bondarenko", "UKR", "M", "-", "o", "-", "o", "-", "xx-", "x", 2.33, ""],
    ["4=", 8, 2456, "Robert", "Grabarz", "GBR", "M", "o", "xo", "o", "o", "xxx", "", "", 2.33, "=SB"],
    ["4=", 15, 3032, "Andriy", "Protsenko", "UKR", "M", "o", "o", "xo", "o", "xxx", "", "", 2.33, "SB"],
    ["6", 6, 3084, "Erik", "Kynard", "USA", "M", "o", "xo", "o", "xxo", "xxx", "", "", 2.33, ""],
    ["7=", 5, 2961, "Majededdin", "Ghazal", "SYR", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
    ["7=", 12, 2294, "Kyriakos", "Ioannou", "CYP", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
    ["7=", 13, 2076, "Donald", "Thomas", "BAH", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
    ["10", 1, 2182, "Tihomir", "Ivanov", "BUL", "M", "o", "xo", "o", "xxx", "", "", "", 2.29, "=PB"],
    ["11", 10, 2062, "Trevor", "Barry", "BAH", "M", "o", "o", "xxx", "", "", "", "", 2.25, ""],
    ["12", 4, 2293, "Dimitrios", "Chondrokoukis", "M", "CYP", "xo", "o", "xxx", "", "", "", "", 2.25, ""],
    ["13", 11, 2871, "Luis", "Castro", "PUR", "M", "o", "xxo", "xxx", "", "", "", "", 2.25, ""],
    ["14", 14, 2297, "Jaroslav", "Bába", "CZE", "M", "o", "xxx", "", "", "", "", "", 2.2, ""],
    ["15", 2, 2052, "Brandon", "Starc", "AUS", "M", "xo", "xxx", "", "", "", "", "", 2.2, ""]
]

class HighJumpTests(TestCase):

    def test_competition_setup(self):
        """Tests basic creation of athletes with names and bibs"""

        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=0)
        self.assertEqual("Dwyer", c.jumpers[-1].last_name)

        self.assertEqual("Maslen", c.jumpers_by_bib['85'].last_name)

    def test_progression(self):
        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=0)
        h1 = Decimal("1.81")
        c.set_bar_height(h1)

        # round 1
        c.cleared('85')

        j = c.jumpers_by_bib['85']
        self.assertEqual(j.attempts_by_height, ['o'])
        self.assertEqual(j.highest_cleared, h1)

        c.failed('77')
        c.failed('77')
        c.failed('77')

        jake_field = c.jumpers_by_bib['77']
        self.assertEqual(jake_field.highest_cleared, Decimal("0.00"))
        self.assertEqual(jake_field.attempts_by_height, ['xxx'])
        self.assertTrue(jake_field.eliminated)

        harry_maslen = c.jumpers_by_bib['85']

        # attempt at fourth jump should fail
        self.assertRaises(RuleViolation, c.failed, '77')

        self.assertEqual(jake_field.place, 4)
        self.assertEqual(harry_maslen.place, 1)

    def test_replay_to_jumpoff(self):
        "Run through to where the jumpoff began - ninth bar position"
        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ, to_nth_height=9)

        # see who is winning
        maslen = c.jumpers_by_bib['85']
        field = c.jumpers_by_bib['77']
        grimsey = c.jumpers_by_bib['53']
        dwyer = c.jumpers_by_bib['81']

        self.assertEqual(field.place, 4)
        self.assertEqual(maslen.place, 3)
        self.assertEqual(grimsey.place, 1)
        self.assertEqual(dwyer.place, 1)

        # print "after 2:12 round"
        # print grimsey.failures_at_height
        # print grimsey.consecutive_failures
        # print grimsey.attempts_by_height
        # if not for jump-off rules, it would be game over
        self.assertEqual(len(c.remaining), 2)
        self.assertEqual(c.state, 'jumpoff')

    def test_replay_through_jumpoff(self):
        "Run through a jumpoff to a draw"
        c = HighJumpCompetition.from_matrix(ESAA_2015_HJ)
        self.assertRaises(RuleViolation,c.failed,'53')

        # see who is winning
        maslen = c.jumpers_by_bib['85']
        field = c.jumpers_by_bib['77']
        grimsey = c.jumpers_by_bib['53']
        dwyer = c.jumpers_by_bib['81']

        self.assertEqual(field.place, 4)
        self.assertEqual(maslen.place, 3)

        self.assertEqual(grimsey.place, 1)
        self.assertEqual(dwyer.place, 1)

        self.assertEqual(len(c.remaining), 2)
        self.assertEqual(c.state, 'jumpoff')

    def test_replay_jumpoff_and_finish(self):
        "Run through a jumpoff to the final winner"
        c = HighJumpCompetition.from_matrix(_1066)
        self.assertRaises(RuleViolation,c.failed,'53')
        self.assertRaises(RuleViolation,c.failed,'81')

        # see who is winning
        briton = c.jumpers_by_bib['85']
        saxon = c.jumpers_by_bib['77']
        norman = c.jumpers_by_bib['53']
        england = c.jumpers_by_bib['81']

        self.assertEqual(saxon.place, 4)
        self.assertEqual(briton.place, 3)

        self.assertEqual(norman.place, 2)
        self.assertEqual(england.place, 1)

        self.assertEqual(len(c.remaining), 1)
        self.assertEqual(c.state, 'finished')
        self.assertEqual(england.highest_cleared, Decimal("2.11"))

        self.assertRaises(RuleViolation,c.set_bar_height, Decimal("2.12"))

    def test_countback_to_tie(self):
        "Run both fail, but tie countback wins"
        c = HighJumpCompetition.from_matrix(
                [
                ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
                ["",      1,       'A',  "Harald", "England",        "o",    "o",    "xo",   "xo",   "xxx"],
                ["",      2,       'B',  "William", "Norman",        "o",    "o",    "o",    "xxo",  "xxx"],
                ]
                )
        self.assertRaises(RuleViolation,c.failed,'A')
        self.assertRaises(RuleViolation,c.failed,'B')

        # see who is winning
        A = c.jumpers_by_bib['A']
        B = c.jumpers_by_bib['B']
        self.assertEqual(A.place, 1)
        self.assertEqual(B.place, 2)
        self.assertEqual(len(c.remaining), 0)
        self.assertEqual(c.state, 'finished')
        self.assertEqual(A.highest_cleared, Decimal("2.12"))
        self.assertEqual(B.highest_cleared, Decimal("2.12"))
        self.assertEqual(A.ranking_key,(2, Decimal('-2.12'), 1, 2))
        self.assertEqual(B.ranking_key,(2, Decimal('-2.12'), 2, 2))

    def test_countback_total_failure_rank(self):
        "test_countback_total_failure_rank"
        c = HighJumpCompetition.from_matrix(
                [
                ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08"],
                ["",    1,     'A',  "Harald", "England",    "o",  "o"],
                ["",    2,     'B',  "William", "Norman",    "xxx"],
                ]
                )
        self.assertRaises(RuleViolation,c.failed,'B')

        # see who is winning
        A = c.jumpers_by_bib['A']
        B = c.jumpers_by_bib['B']
        self.assertEqual(A.place, 1)
        self.assertEqual(B.place, 2)
        self.assertEqual(len(c.remaining), 1)
        self.assertEqual(c.state, 'won')
        self.assertEqual(A.highest_cleared, Decimal("2.08"))
        self.assertEqual(B.highest_cleared, Decimal("0.00"))
        self.assertEqual(A.ranking_key,(0, Decimal('-2.08'), 0, 0))
        self.assertEqual(B.ranking_key,(3, Decimal('0.00'), 0, 0))

    def test_countback_to_total_failures(self):
        "test_countback_to_total_failures"
        c = HighJumpCompetition.from_matrix(
                [
                ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
                ["",      1,       'A',  "Harald", "England",        "o",    "o",    "xo",   "xo",   "xxx"],
                ["",      2,       'B',  "William", "Norman",        "o",    "xo",   "xo",   "xo",  "xxx"],
                ]
                )
        self.assertRaises(RuleViolation,c.failed,'A')
        self.assertRaises(RuleViolation,c.failed,'B')

        # see who is winning
        A = c.jumpers_by_bib['A']
        B = c.jumpers_by_bib['B']
        self.assertEqual(A.place, 1)
        self.assertEqual(B.place, 2)
        self.assertEqual(len(c.remaining), 0)
        self.assertEqual(c.state, 'finished')
        self.assertEqual(A.highest_cleared, Decimal("2.12"))
        self.assertEqual(B.highest_cleared, Decimal("2.12"))
        self.assertEqual(A.ranking_key,(2, Decimal('-2.12'), 1, 2))
        self.assertEqual(B.ranking_key,(2, Decimal('-2.12'), 1, 3))

    def test_won_ending(self):
        "check the status changes at a won ending which finishes"
        mx = [
            ["place", "order", "bib", "first_name", "last_name", "team", "category"],
            ["1", 1, '53', "William", "Norman", "Midd", "SB"],
            ["1", 2, '81', "Harald", "England", "Warks", "SB"],
            ]
        c = HighJumpCompetition.from_matrix(mx)
        self.assertEqual(c.state,'scheduled')
        self.assertEqual(len(c.remaining),2)
        for height,perfs,xstate,lenremj in (
                                            (2.11,("o","o"),'started',2),
                                            (2.12,("o","o"),'started',2),
                                            (2.13,("o","o"),'started',2),
                                            (2.14,("xxx","o"),'won',1),
                                            (2.16,("","o"),'won',1),
                                            (2.17,("","xxo"),'won',1),
                                            (2.18,("","xxx"),'finished',0)):
            c.set_bar_height(height)
            for i in _012:
                for j,p in enumerate(perfs):
                    if len(p)<i+1: continue
                    c.bib_trial(mx[1+j][2],p[i])
            self.assertEqual(c.state,xstate,"height=%s expected state %s not %s" % (height,xstate,c.state))
            self.assertEqual(len(c.remaining),lenremj,"height=%s expected lenremj %s not %s" % (height,lenremj,len(c.remaining)))

    def test_score_olympic_final(self):
        "Do we get the same results as the Olympics?"
        c = HighJumpCompetition.from_matrix(RIO_MENS_HJ, verbose=False)

        # for r in c.ranked_jumper
        # all the positions should agree
        given_finish_positions = []
        for row in RIO_MENS_HJ[1:]:
            place, order, bib = row[0:3]
            expected_place = int(place.replace('=', ''))
            jumper = c.jumpers_by_bib[str(bib)]
            actual_place = jumper.place
            
            self.assertEqual(actual_place, expected_place)

    def test_dismissed(self):
        c = HighJumpCompetition()
        c.add_jumper(bib='A',first_name='Harald',last_name='England')
        c.add_jumper(bib='B',first_name='William',last_name='Norman')
        self.assertRaises(RuleViolation,c.cleared,'A')
        self.assertRaises(RuleViolation,c.passed,'A')
        self.assertRaises(RuleViolation,c.failed,'A')
        self.assertRaises(RuleViolation,c.retired,'A')
        c.set_bar_height(Decimal('2.00'))
        A=c.jumpers_by_bib['A']
        B=c.jumpers_by_bib['B']
        self.assertEqual(A.dismissed,False)
        self.assertEqual(B.dismissed,False)
        c.cleared('A')
        c.passed('B')
        self.assertEqual(A.dismissed,True)
        self.assertEqual(B.dismissed,True)
        c.set_bar_height(Decimal('2.02'))
        self.assertEqual(A.dismissed,False)
        self.assertEqual(B.dismissed,False)
        c.cleared('A')
        c.failed('B')
        self.assertEqual(A.dismissed,True)
        self.assertEqual(B.dismissed,False)
        c.passed('B')
        self.assertEqual(B.dismissed,True)

    def test_trials(self):
        c = HighJumpCompetition()
        c.add_jumper(bib='A',first_name='Harald',last_name='England')
        c.add_jumper(bib='B',first_name='William',last_name='Norman')
        h1 = Decimal('1.10')
        h2 = Decimal('1.15')
        h3 = Decimal('1.14')
        c.set_bar_height(h1)
        self.assertEqual(c.state,'started','state should be started')
        self.assertEqual(c.is_finished,False,'not finished')
        self.assertEqual(c.is_running,True,'is running')
        c.cleared('A')
        c.cleared('B')
        c.set_bar_height(h2)
        c.failed('A')
        c.failed('B')
        c.failed('A')
        c.failed('B')
        c.failed('A')
        c.failed('B')
        self.assertEqual(c.state,'jumpoff','jumpoff state should be reached')
        self.assertEqual(c.is_finished, False,"jumpoff competition is not finished")
        self.assertEqual(c.is_running, True,"jumpoff competition is running")
        c.set_bar_height(h3)
        self.assertEqual(c.trials,[('A',h1,'o'),('B',h1,'o'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x')],'trials in jumpoff state')
        c.failed('A')
        self.assertEqual(c.state,'jumpoff','still in jumpoff after A fails at 1.14')
        self.assertEqual(c.trials,[('A',h1,'o'),('B',h1,'o'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x'),('A',h3,'x')], 'trials after A fails at 1.14')
        c.cleared('B')
        self.assertEqual(c.state,'finished','state finished after B clears at 1.14')
        fal = [('A',h1,'o'),('B',h1,'o'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x'),('A',h2,'x'),('B',h2,'x'),('A',h3,'x'),('B',h3,'o')]
        fadl = [dict(bib=a[0],height=a[1],result=a[2]) for a in fal]
        self.assertEqual(c.trials, fal, 'final trials')
        self.assertEqual(c.trial_objs, fadl, 'final trial_objs')
        self.assertEqual(c.from_actions().trials, fal, 'd.from_actions().trials should match c.trials')
        self.assertEqual(c.from_actions().trial_objs, fadl, 'd.from_actions().trial_objs should match c.trial_objs')

    def test_action_letter(self):
        c = HighJumpCompetition()
        self.assertEqual(c.action_letter['cleared'],'o',"action_letter['cleared']=='o'")
        self.assertEqual(c.action_letter['failed'],'x',"action_letter['failed']=='x'")
        self.assertEqual(c.action_letter['passed'],'-',"action_letter['passed']=='-'")
        self.assertEqual(c.action_letter['retired'],'r',"action_letter['passed']=='r'")

    actions_a = [["add_jumper",dict(bib='A')], ["add_jumper",dict(bib='B')], ["set_bar_height",1.1], ["cleared","A"], ["cleared","B"],
        ["set_bar_height",1.2], ["failed","A"], ["failed","B"], ["failed","A"], ["failed","B"], ["failed","A"], ["failed","B"],
        ["set_bar_height",1.15], ["cleared","A"], ["cleared","B"], ["set_bar_height",1.17], ["failed","A"], ["failed","B"],
        ["set_bar_height",1.16], ["retired","A"], ["retired","B"]]
    matrix_a = [
        ["bib", "1.10", "1.20", "1.15", "1.17", "1.16"],
        ["A",   "o",    "xxx",  "o",    "x",    "r"],
        ["B",   "o",    "xxx",  "o",    "x",    "r"],
        ]

    def test_retire_after_jumpoff(self):
        c = HighJumpCompetition().from_actions(self.actions_a)
        self.assertEqual(c.state,'drawn','both retiring after jumpoffs should draw')
        c = HighJumpCompetition().from_matrix(self.matrix_a)
        self.assertEqual(c.state,'drawn','both retiring after jumpoffs should draw')
        self.assertEqual(c.to_matrix(),self.matrix_a,'matrix round trip should match')
        self.assertEqual(c.is_finished, True,"competition is finished")
        self.assertEqual(c.is_running, False,"competition is not running")

    def test_rieto_pv(self):
        c = HighJumpCompetition.from_matrix(
            [_.split() for _ in '''bib 3.00 3.20 3.40 3.60 3.70 3.80 3.85 3.90 3.95 4.00
QF000595    -    -    o    o    -    o    -    o  xxx
EH004164    -    -    -   xo   xo    o    o  xxo  xxx
JA112119    -    -    o   xo    o  xxx
CB064342    -    -    o   xo    o  xxx
FC009594    -    -    -    o    o   x-    o  xx-    x
HC000711    -    -    o    o    -  xxx
CF058632    -    -   xo   xo  xxx
GL001818   xo    o  xxx
EC001108    o   xo    o  xxx
VA008725    o    o  xxo  xxx
JE001383    o    o  xxx
CG000293    o   xo  xxx
BC000303    o   xo  xxx
EE010870    -    -    o    o  xxo    o  xx-    x
EE006186   xo   xo  xxx
JC003084    o  xxx
EF007915    -    -    o    o   xo    o  xxo   xo  xxo  xxx
GL000737    o  xxx
DA011840    o    o  xxx
CK006373   xo  xxx
GJ001614   xo  xxx
ED000485   x-   xx
JA103141  xxx'''.split('\n')]
                , verbose=False)
        self.assertEqual(c.state,'finished','One winning jumper failed at his chosen height')
        self.assertEqual(c.jumpers_by_bib['EF007915'].place,1,'EF007915 came first')

    def test_nor_strangeness(self):
        mx = [_.split() for _ in '''bib 4.65 4.75 4.85 4.95 5.05 4.95 4.90 4.85
193 o xo o xxx - x x x
175 o xo o - xxx x x o'''.split('\n')]
        def check(r1v, r2v, p175, p193):
            mx[1][8] = r1v;
            mx[2][8] = r2v;
            c = HighJumpCompetition.from_matrix(mx)
            self.assertTrue(c.jumpers_by_bib['175'].place==p175
                            and
                            c.jumpers_by_bib['193'].place==p193,
                            '175 place %s 193 place %s %s %s' % (p175,p193,r1v,r2v))
        check('x', 'o', 1, 2);
        check('r', 'o', 1, 2);
        check('r', 'r', 1, 1);
        check('x', 'x', 1, 1);


if __name__ == '__main__':
    main()
