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
"""
from __future__ import print_function, annotations
from decimal import Decimal
from .exceptions import RuleViolation
from typing import Tuple, List, Dict
_012 = 0,1,2    #range of attempts

#The countback rule used to separate competitors with equal best heights in High Jump and Pole Vault is possibly the most misunderstood rule in the whole of the sport. Here's how it operates:
#The athlete with the fewest attempts at the last height successfully cleared gets the verdict.
#This means that, no matter how poorly your earlier attempts have gone, there's still a way back into the competition.
#Then you count the athletes's number of failures, not including any attempts beyond the height actually cleared: the athlete with the fewest gets the verdict.
#So you cannot harm your cause by trying for a height which you think it unlikely that you will clear. But accurate jumping at the lower heights is vital!
#http://s250914043.websitehome.co.uk/offcourse/HighJumpRules.html

class Jumper(object):
    """Used by HighJumpCompetition internally"""
    def __init__(self, **kwargs):
        "Allow keyword initialisation"
        self.order = 1  # if we get only one, I guess they jump first
        self._place = 1 # if we only get one, I guess they are winning

        # list of strings containing '', 'o', 'xo', 'xxo', 'xxx', 'x', 'xx'
        self.attempts_by_height = []
        self.highest_cleared = Decimal("0.00")
        self.highest_cleared_index = -1
        self.eliminated = False     # still in the competition?
        self.dismissed = False      # still in the round?
        self.round_lim = 3
        self.consecutive_failures = 0

        for (arg, default) in [
            ('first_name', 'unknown'),
            ('last_name', 'athlete'),
            ('bib', '0'),
            ('team', 'GUEST'),
            ('gender', 'M'),  # sexist but valid
            ('category', 'OPEN'),
            ('order', 1),
        ]:
            value = kwargs.get(arg, default)
            setattr(self, arg, value)

    def _set_jump_array(self, height_count: int, label : str = 'jump') -> None:
        """Ensure they have one string for each height in the competition

        Jumpers can miss out heights.
        """
        assert height_count > 0, "Start at height number 1, not 0"
        if self.eliminated or self.dismissed:
            what = 'retiring' if self.has_retired else 'being eliminated' if self.eliminated else 'passing'
            raise RuleViolation("Cannot %s after %s" % (label,what))
        atts = self.attempts_by_height
        # they may have skipped some, pas with empty strings
        while len(atts) < height_count:
            atts.append('')
        if len(self.attempts_by_height[-1]) > self.round_lim-1:
            raise RuleViolation("Can attempt a maximum of %d times" % self.round_lim)

    @property
    def has_retired(self):
        return self.attempts_by_height and self.attempts_by_height[-1].endswith('r')

    @property
    def ranking_key(self) -> Tuple[int, Decimal, int, int]:
        """Return a sort key to determine who is winning"""
        x = self.highest_cleared_index
        if x<0:
            failures_before_and_at_height = failures_at_height = 0
        else:
            failures_at_height = self.attempts_by_height[x].count('x')
            failures_before_and_at_height = failures_at_height + sum(_.count('x') for _ in self.attempts_by_height[:x])
        return (
            (3 if x<0 else 2) if self.eliminated else (1 if x<0 else 0),
            - self.highest_cleared,
            failures_at_height,
            failures_before_and_at_height,
            )

    @property
    def place(self):
        if self.order in ('DQ','DNS'):
            return self.order
        elif self.highest_cleared_index<0:
            return ''
        return self._place

    def cleared(self, height_count: int, height: Decimal) -> None:
        """Add a clearance at the current bar position"""
        self._set_jump_array(height_count)

        # Holds their pattern of 'o' and 'x'
        self.attempts_by_height[-1] += 'o'
        self.highest_cleared = height
        self.highest_cleared_index = len(self.attempts_by_height)-1
        self.consecutive_failures = 0
        self.dismissed = True

    def failed(self, height_count: int, height: Decimal) -> None:
        """Add a failure at the current bar position"""
        self._set_jump_array(height_count)

        # Holds their pattern of 'o' and 'x'
        self.attempts_by_height[-1] += 'x'
        self.consecutive_failures += 1
        if self.consecutive_failures>=self.round_lim:
            self.eliminated = self.dismissed = True
        else:
            self.dismissed = False

    def passed(self, height_count: int, height: Decimal) -> None:
        "Competitor passes"
        self._set_jump_array(height_count,'pass')

        # Holds their pattern of 'o' and 'x'
        self.attempts_by_height[-1] += '-'
        self.dismissed = True

    def retired(self, height_count: int, height: Decimal) -> None:
        "Competitor had enough, or pulls out injured"
        self._set_jump_array(height_count,'retire')

        # Holds their pattern of 'o' and 'x'
        self.attempts_by_height[-1] += 'r'
        self.eliminated = True
        self.dismissed = True

class TrialObj(dict):
    def __init__(self, *args, **kwargs):
        super(TrialObj, self).__init__(*args, **kwargs)
        self.__dict__ = self

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
        self.heights = []   # sequence of heights so far
        self.in_jump_off = False
        self.actions = []  # log for replay purposes.
        self.verbose = 0  # helpful print statements
        self.state = 'scheduled'

    def add_jumper(self, **kwargs) -> None:
        """Add one more person to the competition

        Normally we add them first, but can arrive mid-competition.
        If so, they are in last place until they clear a height.
        """
        if self.state!='scheduled':
            raise RuleViolation("Cannot add jumpers in competition state %r" % self.state)
        j = Jumper(**kwargs)
        if j.bib in self.jumpers_by_bib:
            raise RuleViolation('cannot have two athletes with the same bib (%r)!' % j.bib)
        j._place = len(self.jumpers) + 1

        self.jumpers_by_bib[j.bib] = j
        self.jumpers.append(j)
        self.ranked_jumpers.append(j)

        # record what happened
        self.actions.append(('add_jumper', kwargs))

    def set_bar_height(self, new_height: Decimal) -> None:
        if self.state=='scheduled':
            self.state = 'started'
        elif self.state not in ('started','jumpoff','won'):
            raise RuleViolation('Bar height cannot be set in a %s competition!' % self.state)
        prev_height = (self.heights and self.heights[-1]) or Decimal("0.00")
        if (self.state!='jumpoff') and (prev_height >= new_height):
            raise RuleViolation("The bar can only go up, except in a jump-off")
        for j in self.jumpers:
            if not j.eliminated:
                j.dismissed = False
        self.heights.append(new_height)
        self.bar_height = new_height
        self.actions.append(('set_bar_height', new_height))

    def check_started(self, bib: str, label: str = 'jumping') -> Jumper:
        jumper = self.jumpers_by_bib[bib]
        state = self.state
        if state not in ('started','jumpoff'):
            if state in ('won','drawn'):
                if jumper._place!=1:
                    raise RuleViolation('The competition has been %s and %s is not allowed!' % (state,label))
            elif state == 'finished':
                raise RuleViolation('The competition has finished and %s is not allowed!' % label)
            else:
                raise RuleViolation('The competition has not been started yet!')
        elif jumper.order in ('DQ','DNS'):
            raise RuleViolation('Jumper with bib, %s, has order %s and %s is not allowed!' % (jumper.bib,jumper.order,label))
        return jumper

    def cleared(self, bib: str) -> None:
        "Record a successful jump"
        jumper = self.check_started(bib)
        jumper.cleared(len(self.heights), self.bar_height)
        self.actions.append(('cleared', bib))
        self._rank()

    def failed(self, bib: str) -> None:
        "Record a failed jump, raises RuleViolation if out of order"
        jumper = self.check_started(bib)
        jumper.failed(len(self.heights), self.bar_height)
        self.actions.append(('failed', bib))
        self._rank()

    def passed(self, bib: str) -> None:
        "Record a pass,  raises RuleViolation if out of order"
        jumper = self.check_started(bib)
        jumper.passed(len(self.heights), self.bar_height)
        self.actions.append(('passed', bib))
        self._rank()

    def retired(self, bib: str) -> None:
        "Record a failed jump. Throws RuleViolation if out of order"
        jumper = self.check_started(bib,'retiring')
        jumper = self.jumpers_by_bib[bib]
        jumper.retired(len(self.heights), self.bar_height)
        self.actions.append(('retired', bib))
        self._rank()

    action_letter = dict(cleared='o', failed='x', passed='-', retired='r')

    @property
    def trials(self) -> List[Tuple[str, Decimal, str]]:
        T = []
        aT = T.append
        al = self.action_letter
        bh = None
        for a,v in self.actions:
            if a=='set_bar_height':
                bh = v
            elif a in al:
                aT((v,bh,al[a]))
        return T

    @property
    def trial_objs(self) -> List[TrialObj]:
        return [TrialObj(bib=t[0],height=t[1],result=t[2]) for t in self.trials]

    @property
    def remaining(self) -> List[Jumper]:
        "remaining jumpers"
        return [j for j in self.jumpers if not j.eliminated]

    @property
    def eliminated(self) -> List[Jumper]:
        "eliminated jumpers"
        return [j for j in self.jumpers if j.eliminated]

    def _rankj(self) -> List[Jumper]:
        # sort ranked_jumpers
        rankj = self.ranked_jumpers
        for i,j in enumerate(rankj): j._old_pos = i
        rankj.sort(key=lambda j: (j.ranking_key, j._old_pos))

        pk = None
        pj = None
        for i, j in enumerate(rankj):
            del j._old_pos
            k = j.ranking_key
            if i == 0:
                j._place = 1
            else:
                if k == pk:
                    j._place = pj._place
                else:
                    j._place = i + 1
            pk = k
            pj = j
        return rankj

    def _rank(self, verbose: bool = False) -> None:
        "Determine who is winning"
        rankj = self._rankj()
        if not rankj: return

        if 1 and verbose: print('ranked jumpers in order %s:' % repr([(j._place,j.bib,j.ranking_key) for j in rankj]))

        remj = self.remaining
        if len(remj)==0:
            #they all failed or retired at this height
            if len(rankj)> 1 and rankj[1]._place==1:
                nc = 0
                for j in rankj:
                    if j._place!=1: continue
                    if j.has_retired:
                        j.rank_group = 1
                    else:
                        nc += 1
                        j.eliminated = False
                        j.round_lim = 1
                        j.consecutive_failures = 0
                        j.rank_group = 2
                self.state = 'jumpoff' if nc else 'drawn'
            elif self.state=='jumpoff' and not rankj[0].has_retired:
                    j = rankj[0]
                    j.eliminated = False
                    j.round_lim = 1
                    j.consecutive_failures = 0
            else:
                self.state = 'finished'
        elif (len(remj)==1 and (1+len(self.eliminated))==len(self.jumpers)
                and len(remj[0].attempts_by_height)==len(self.heights)
                and 'o' in remj[0].attempts_by_height[-1]):
            self.state = 'won' if self.state in ('started','won') else 'finished'

    def bib_trial(self, bib: str, trial: str) -> None:
        if trial == 'o':
            self.cleared(bib)
        elif trial == 'x':
            self.failed(bib)
        elif trial == 'r':
            self.retired(bib)
        elif trial == '-':
            pass  # sometimes people use - rather than a blank cell to show
                  # a deliberate pass.  Do nothing.
        else:
            raise RuleViolation("Unknown jump trial code '%s'" % trial)

    @classmethod
    def from_matrix(cls, matrix: List[List[str]], to_nth_height: int = None, verbose: bool = False) -> HighJumpCompetition:
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
        self.verbose = verbose
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
                print("bar at %s" % height)
            for a in _012:
                for d in dikts:
                    if d['order'] in ('DNS','DQ'): continue
                    bib = d['bib']
                    name  = d.get('last_name', '')
                    attempts = d.get(height_key, '')
                    if len(attempts) > a:
                        result = attempts[a]
                        if self.verbose:
                            print("  %s %s attempt %d: %s" % (bib, name, a + 1, result))
                        self.bib_trial(bib,result)
            if self.verbose:
                print("rankings at end of %s round" % height)
                self.print_ranking()

        return self

    def _looks_like_height(self, txt:str) -> bool:
        try:
            h = float(txt)
            return True
        except ValueError:
            return False


    def _ensure_dicts_ordered(self, dikts: List[Dict[str, str]]) -> None:
        """Ensure they each have an 'order' attribute in which they jump

        If partially present, respect ordered ones first and place others after
        """
        unordered = []
        highest = 0
        for dikt in dikts:
            if 'order' not in dikt:
                unordered.append(dikt)
            else:
                i = dikt['order']
                try:
                    i = int(i)
                    highest = max(highest, i)
                except:
                    i = i.upper()
                    if i not in ('DQ','DNS'):
                        raise ValueError('Invalid order %r' % i)

        for u in unordered:
            highest += 1
            u['order'] = highest

    def print_ranking(self):
        "Debugging utility to show who's leading at a point in time"
        for r in self.ranked_jumpers:
            print(r.place, r.bib, r.first_name, r.last_name, r.ranking_key)

    def from_actions(self, actions: List[Tuple] = None) -> HighJumpCompetition:
        if actions is None: actions = self.actions
        hj = self.__class__()
        for a, v in actions:
            m = getattr(hj,a)
            if isinstance(v,dict):
                m(**v)
            else:
                m(v)
        return hj

    def to_matrix(self, keys: List[str] = []) -> List[List[str]]:
        if 'bib' not in keys: keys.insert(0, 'bib')
        R = [keys + ['%.2f'%h for h in self.heights]]
        J = sorted([([getattr(j,k) for k in keys],j) for j in self.ranked_jumpers])
        for j in J:
            R.append(j[0]+j[1].attempts_by_height)
        return R

    @property
    def is_finished(self) -> bool:
        return self.state in ('finished','won','drawn')

    @property
    def is_running(self) -> bool:
        return self.state in ['started','jumpoff']
