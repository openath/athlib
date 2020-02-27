"""Unit tests for qkids_score.py."""

from unittest import TestCase, main
from athlib import qkids_score


class QKidsScoreTests(TestCase):
    """Test suite for the qkids score calculation module."""

    def test_performance(self):
        """
        test returned points.  Input string or float perfprmance
        """
        bad = [].append
        for ct, event, perf, expected in [
                ('QuadKids Secondary', '100', 18, 25),
                ('QuadKids Secondary', '100', 18.1, 24),
                ('QuadKids Secondary', '100', 18.2 , 23),
                ('QuadKids Secondary', '100', 18.3, 22),
                ('QuadKids Secondary', '100', 18.4, 21),
                ('QuadKids Secondary', '100', 18.5, 20),
                ('QuadKids Secondary', '100', 18.6, 19),
                ('QuadKids Secondary', '100', 18.7, 18),
                ('QuadKids Secondary', '100', 18.8, 17),
                ('QuadKids Secondary', '100', 18.9, 16),
                ('QuadKids Secondary', '100', 19,   15),
                ('QuadKids Secondary', '100', 19.1, 14),
                ('QuadKids Secondary', '100', 19.2, 13),
                ('QuadKids Secondary', '100', 19.3, 12),
                ('QuadKids Secondary', '100', 19.4, 11),
                ('QuadKids Secondary', '100', 20.1, 10),
                ('QKSEC', '100', 9, 100),
                ('QuadKids Secondary', '100', 19.03, 14),
                ('QuadKids Primary', 'SLJ', 1.82, 50),
                ('QuadKids Primary', '4x100', '74.00', 50),
                ('QuadKids Primary', '75', '12.00', 50),
                ('QuadKids Primary', '600', '2:20', 50),
                ('QuadKids Primary', 'ot', '25', 50),
                ('Wessex League','600','1:30',100),
                ('Wessex League (U13)','800','2:20',100),
                ('QKSEC','800','140',100),
                ('QuadKids Primary','600','1:30',100),
                ('QKSTA','400','35',100),
                ('QKCLUB','600','1:30',100),
                ('QKCLU13','800','2:20',100),
                ('QKCLU9','400','40',100),
                ('QKPRE','300','45',100),
                ]:
            r = qkids_score(ct, event, perf)
            if r!=expected:
                bad("qkids_score(%r, %r, %r) returned %r not the expected %r" %(
                        ct, event, perf, r, expected))
        bad = bad.__self__
        self.assertEqual(len(bad),0,"\nnot all qkids_score tests were correct\n%s" % '\n'.join(bad))

if __name__ == '__main__':
    main()
