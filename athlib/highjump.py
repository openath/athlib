"""High Jump and Pole Vault calculator.

This module provides an object to simulate a high jump or pole vault
competition, and to work out the scores.

We can present and extract data in this format, which is normally
how field cards are written.

ESAA_2015_HJ = [
    # Eglish Schools Senior Boys 2015 - epic jumpoff ending in a draw
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




Not yet implemented:  jumpoff
"""
from decimal import Decimal

from .exceptions import RuleViolation

class Jumper(object):
    """Used by HighJumpCompetition internally"""
    def __init__(self, **kwargs):
        "Allow keyword initialisation"
        self.order = 1  # if we get only one, I guess they jump first
        self.place = 1  # if we only get one, I guess they are winning

        # list of strings containing '', 'o', 'xo', 'xxo', 'xxx', 'x', 'xx'
        self.attempts_by_height = []
        self.highest_cleared = Decimal("0.00")
        self.failures_at_height = 0
        self.consecutive_failures = 0
        self.total_failures = 0
        self.eliminated = False  # still in the competition?

        for (arg, default) in [
            ('first_name', 'unknown'),
            ('last_name', 'athlete'),
            ('bib', '0'),
            ('team', 'GUEST'),
            ('gender', 'M'),  # sexist but valid
            ('category', 'OPEN')
        ]:
            value = kwargs.get(arg, default)
            setattr(self, arg, value)

    def _set_jump_array(self, height_count):
        """Ensure they have one string for each height in the competition

        Jumpers can miss out heights.
        """
        assert height_count > 0, "Start at height number 1, not 0"
        atts = self.attempts_by_height
        # they may have skipped some, pas with empty strings
        while len(atts) < height_count:
            atts.append('')

    def ranking_key(self):
        """Return a sort key to determine who is winning"""

        return (
            - self.highest_cleared,
            self.failures_at_height,
            self.total_failures
        )

    def cleared(self, height_count, height):
        """Add a clearance at the current bar position

        First round is index zero
        """
        if self.eliminated:
            raise RuleViolation("Cannot jump after being eliminated")

        self._set_jump_array(height_count)

        # Holds their pattern of 'o' and 'x'
        cur = self.attempts_by_height[-1]
        cur += 'o'
        self.attempts_by_height[-1] = cur

        assert len(cur) <= 3, "Can attempt a maximum of %d times" % len(cur)

        self.highest_cleared = height
        self.failures_at_height = 0
        self.consecutive_failures = 0

    def failed(self, height_count, height):
        """Add a failure at the current bar position

        """
        if self.eliminated:
            raise RuleViolation("Cannot jump after being eliminated")

        self._set_jump_array(height_count)

        # Holds their pattern of 'o' and 'x'
        cur = self.attempts_by_height[-1]
        cur += 'x'
        self.attempts_by_height[-1] = cur

        assert len(cur) <= 3, "More than 3 attempts at height"

        self.failures_at_height += 1
        self.consecutive_failures += 1
        if self.consecutive_failures == 3:
            self.eliminated = True

    def retired(self, height_count, height):
        "Competitor had enough, or pulls out injured"
        if self.eliminated:
            raise RuleViolation("Cannot retire after being eliminated")

        self._set_jump_array(height_count)

        # Holds their pattern of 'o' and 'x'

        cur = self.attempts_by_height[-1]
        cur += 'r'
        self.attempts_by_height[-1] = cur
        assert len(cur) <= 3, "More than 3 attempts at height"

        self.eliminated = True

        self.actions.append(('retired', height_count, height))


class HighJumpCompetition(object):
    """Simulation of a HighJump competition in progress.

    This is a small "state machine" which respons to things like
    "raise the bar", "do a jump", and aims to tell you who is leading
    at any point.
    """
    def __init__(self):
        self.jumpers = []
        self.jumpers_by_bib = {}
        self.ranked_jumpers = []

        self.bar_height = Decimal("0.00")
        self.trials = []
        self.heights = []   # sequence of heights so far
        self.in_jump_off = False

        self.actions = []  # log for replay purposes.

        self.verbose = 0  # helpful print statements



    def add_jumper(self, **kwargs):
        """Add one more person to the competition

        Normally we add them first, but can arrive mid-competition.
        If so, they are in last place until they clear a height.
        """

        j = Jumper(**kwargs)
        j.place = len(self.jumpers) + 1

        self.jumpers_by_bib[j.bib] = j
        self.jumpers.append(j)
        self.ranked_jumpers.append(j)

        # record what happened
        self.actions.append(('add_jumper', kwargs))

    def set_bar_height(self, new_height):
        prev_height = (self.heights and self.heights[-1]) or Decimal("0.00")
        if (not self.in_jump_off) and (prev_height >= new_height):
            raise RuleViolation("The bar can only go up, except in a jump-off")
        self.heights.append(new_height)
        self.bar_height = new_height

    def cleared(self, bib):
        "Record a successful jump"
        jumper = self.jumpers_by_bib[bib]
        jumper.cleared(len(self.heights), self.bar_height)
        self._rank()
        self.actions.append(('cleared', bib))

    def failed(self, bib):
        "Record a failed jump. Throws RuleViolation if out of order"
        jumper = self.jumpers_by_bib[bib]
        jumper.failed(len(self.heights), self.bar_height)
        self._rank()
        self.actions.append(('failed', bib))

    def retired(self, bib):
        "Record a failed jump. Throws RuleViolation if out of order"
        jumper = self.jumpers_by_bib[bib]
        jumper.retired(len(self.heights), self.bar_height)
        self._rank()
        self.actions.append(('retired', bib))

    def remaining(self):
        "How many are left in the competition?"
        remaining = 0
        for j in self.jumpers:
            if not j.eliminated:
                remaining += 1
        return remaining

    def _rank(self, verbose=True):
        "Determine who is winning"

        # sort them
        sorter = []
        for j in self.ranked_jumpers:
            key = j.ranking_key()
            sorter.append((key, j))
        sorter.sort()

        prev_key = None
        prev_jumper = None
        for i, (key, jumper) in enumerate(sorter):
            if i == 0:
                jumper.place = 1
            else:
                if key == prev_key:
                    jumper.place = prev_jumper.place
                else:
                    jumper.place = i + 1
            prev_key = key
            prev_jumper = jumper
        self.ranked_jumpers = [j for (key, j) in sorter]


    @classmethod
    def from_matrix(cls, matrix, to_nth_height=None):
        """ Convert from a pasteable tabular representation like this...

        RIO_MENS_HJ = [  # pasted from Wikipedia
            ["place", "order", "bib", "first_name", "last_name", "team", "2.20", "2.25", "2.29", "2.33", "2.36", "2.38", "2.40", "best", "note"],
            ["1", 7, 2197, "Derek", "Drouin", "Canada", "o", "o", "o", "o", "o", "o", "x", 2.38, ""],
            ["2", 9, 2878, "Mutaz", "Essa Barshim", "Qatar", "o", "o", "o", "o", "o", "xxx", "", 2.36, ""],
        ]

        Column headers looking like numbers will be taken as the heights.  They may repeat,
        as for a jumpoff where the bar comes down again.
        We pay attention only to order, bib, first_name, last_name, team, category and the heights.
        The place and best are calculated so discarded.  The personal details may be used to
        create competitor records if corresponding ones are not found.

        replays the bar heights up to the Nth bar if given.
        pass None for an empty competition.

        """
        self = cls()
        # heights are in the top row - change to h1, h2 etc
        heights = []
        headers = matrix[0][:]
        for (colNo, txt) in enumerate(headers):
            if self._looks_like_height(txt):
                height = Decimal(txt)
                heights.append(height)
                headers[colNo] = 'h%d' % len(heights)
        dikts = []
        for row in matrix[1:]:
            dikt = {}
            for key, value in zip(headers, row):
                if key == 'bib':
                    value = str(value)
                dikt[key] = value
            dikts.append(dikt)

        self._ensure_dicts_ordered(dikts)

        dikts.sort(key=lambda x: x['order'])

        for dikt in dikts:
            self.add_jumper(**dikt)

        if to_nth_height is None:
            heights_to_replay = heights
        else:  # we want some of them, or an empty competition
            heights_to_replay = heights[0:to_nth_height]


        for i, height in enumerate(heights_to_replay):
            height_key = "h%d" % (i + 1)
            self.set_bar_height(height)
            if self.verbose: 
                print "bar at %s" % height
            for a in range(3):
                for d in dikts:
                    bib = d['bib']
                    name  = d.get('last_name', '')
                    attempts = d.get(height_key, '')
                    if len(attempts) > a:
                        result = attempts[a]
                        if self.verbose: 
                            print "  %s %s attempt %d: %s" % (bib, name, a + 1, result)
                        if result == 'o':
                            self.cleared(bib)
                        elif result == 'x':
                            self.failed(bib)
                        elif result == 'r':
                            self.retired(bib)
                        else:
                            raise RuleViolation("Unknown jump result code '%s'" % result)





        return self

    def _looks_like_height(self, txt):
        try:
            h = float(txt)
            return True
        except ValueError:
            return False


    def _ensure_dicts_ordered(self, dikts):
        """Ensure they each have an 'order' attribute in which they jump

        If partially present, respect ordered ones first and place others after
        """
        unordered = []
        highest = 0
        for dikt in dikts:
            if 'order' not in dikt:
                unordered.append(dikt)
            else:
                highest = max(highest, dikt['order'])

        for u in unordered:
            highest += 1
            u['order'] = highest

