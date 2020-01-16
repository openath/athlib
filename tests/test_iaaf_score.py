"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main
from athlib.iaaf_score import performance, scoring_key, score, unit_name


class IaafScoreTests(TestCase):
    """Test suite for the IAAF score calculation module."""

    def test_performance(self):
        """
        Test the function to calculate the required performance for a given
        score.
        """
        self.assertEquals(performance("F", "10000", 915), 2400.73)
        self.assertEquals(performance("M", "110H", 973), 14.01)
        self.assertEquals(performance("M", "110H", 974), 14)
        self.assertEquals(performance("F", "HJ", 1000), 1.82)
        self.assertEquals(performance("M", "WT", 1), 1.53)
        self.assertEquals(performance("F", "JT", 700), 41.68)
        self.assertEquals(performance("M", "PV", 1284), 6.16)

        # You need 1m to score 0, so that's what you get back
        self.assertEquals(performance("M", "PV", 0), 1.0)
        self.assertEquals(performance("M", "PV", -100), 1.0)
        self.assertEquals(performance("M", "NA", 500), None)

    def test_scoring_key(self):
        """
        Test the function to calculate the scoring key from the gender and
        event code.
        """
        self.assertEquals(scoring_key("m", "100"), "M-100")
        self.assertEquals(scoring_key("f", "400h"), "F-400H")
        self.assertEquals(scoring_key("M", "3000SC"), "M-3000SC")
        self.assertEquals(scoring_key("F", "lJ"), "F-LJ")
        self.assertEquals(scoring_key("m", "Hj"), "M-HJ")
        self.assertEquals(scoring_key("f", "jt"), "F-JT")
        self.assertEquals(scoring_key("M", "WT"), "M-WT")

    def test_score(self):
        """Test the function to calculate the score for a given performance."""
        self.assertEquals(score("F", "10000", 2400), 915)
        self.assertEquals(score("M", "110H", 14.01), 973)
        self.assertEquals(score("M", "110H", 14), 975)
        self.assertEquals(score("F", "HJ", 1.93), 1145)
        self.assertEquals(score("M", "WT", 1.53), 1)
        self.assertEquals(score("M", "WT", 1), 0)
        self.assertEquals(score("F", "JT", 41.68), 700)
        self.assertEquals(score("M", "PV", 6.16), 1284)

        self.assertEquals(score("M", "LJ", 0.5), 0)
        self.assertEquals(score("M", "100", 45), 0)

        self.assertEquals(score("?", "NA", 42), None)

    def test_unit_name(self):
        """Test the unit names for jumps, throws and track events."""
        self.assertEquals(unit_name("100"), "seconds")
        self.assertEquals(unit_name("200H"), "seconds")
        self.assertEquals(unit_name("3000SC"), "seconds")
        self.assertEquals(unit_name("LJ"), "metres")
        self.assertEquals(unit_name("PV"), "metres")
        self.assertEquals(unit_name("SP"), "metres")
        self.assertEquals(unit_name("WT"), "metres")

    def test_wma_adjusted_score(self):
        "Extra bonus for being old, used by WMA"
        self.assertEquals(score("M", "60H", 10.58), 437)


        self.assertEquals(score("M", "60H", 11.85, 50), 437)
        self.assertEquals(score("M", "LJ", 4.53, 50), 494)
        
        # needs work, we need full weight event code in age factors e.g. SP6K,
        # but simple code e.g. SP in points calculation
        self.assertEquals(score("M", "SP", 8.05, 50), 451)

        self.assertEquals(score("F", "60H", 10.59, 53), 883)
        self.assertEquals(score("F", "HJ", 1.38, 53), 842)

    def test_esaa_adjusted_score(self):
        # Tha famous boys 800 issue.
        self.assertEquals(score("M", "800", 120, esaa=True), 769)


if __name__ == '__main__':
    main()
