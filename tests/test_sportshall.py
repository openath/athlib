"""Unit tests for sportshall_score.py."""

from unittest import TestCase, main
from athlib import sportshall_score


class QKidsScoreTests(TestCase):
    """Test suite for the sportshall_score score calculation module."""

    def test_performance(self):
        """
        test returned points.  Input string or float perfprmance
        """
        bad = [].append
        for event, perf, expected in [

            # Basic high-scoring event:
            ('SLJ', '3.00', 90),  # out of range, uses increment
            ('SLJ', '2.80', 80),  # upper boundary of points lookup
            ('SLJ', '2.00', 56),  # mid range, binary search
            ('SLJ', '0.36', 1),   # just above 1-point lower bounds
            ('SLJ', '0.30', 0),   # too low to get any points


            # 70 point level for all events where defined, or one other
            ('SLJ', '2.40', 70),
            ('SHJ', '0.59', 70),
            ('STJ', '6.85', 70),
            ('SP', '9.50', 70),
            ('BAL', '50', 55),
            ('SPB', '70', 70),
            ('TART', '23', 69),
            ('OHT', '10.75', 70),
            ('32H', '12.7', 70),
            ('CHT', '10.5', 70),
            ('100', '26.0', 70),
            ('JT', '23', 69),

            ]:
            r = sportshall_score(event, perf)
            if r!=expected:
                bad("sportshall_score(%r, %r) returned %r not the expected %r" %(
                        event, perf, r, expected))
        bad = bad.__self__
        self.assertEqual(len(bad),0,"\nnot all sportshall_score tests were correct\n%s" % '\n'.join(bad))

if __name__ == '__main__':
    main()
