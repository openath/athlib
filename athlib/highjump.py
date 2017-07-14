"""High Jump and Pole Vault calculator.

This module provides an object to simulate a high jump or pole vault
competition, and to work out the scores.

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
