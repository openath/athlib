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
        self.assertEquals(performance("F", "HJ", 1000), 182)
        self.assertEquals(performance("M", "WT", 1), 1.53)
        self.assertEquals(performance("F", "JT", 700), 41.68)
        self.assertEquals(performance("M", "PV", 1284), 616)

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
        self.assertEquals(score("F", "HJ", 193), 1145)
        self.assertEquals(score("M", "WT", 1.53), 1)
        self.assertEquals(score("M", "WT", 1), 0)
        self.assertEquals(score("F", "JT", 41.68), 700)
        self.assertEquals(score("M", "PV", 616), 1284)

    def test_unit_name(self):
        """Test the unit names for jumps, throws and track events."""
        self.assertEquals(unit_name("100"), "seconds")
        self.assertEquals(unit_name("200H"), "seconds")
        self.assertEquals(unit_name("3000SC"), "seconds")
        self.assertEquals(unit_name("LJ"), "centimetres")
        self.assertEquals(unit_name("PV"), "centimetres")
        self.assertEquals(unit_name("SP"), "metres")
        self.assertEquals(unit_name("WT"), "metres")


if __name__ == '__main__':
    main()
