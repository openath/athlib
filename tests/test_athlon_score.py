"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main
from athlib.athlon_score import performance, scoring_key, score, unit_name
from athlib.implements import get_implement_weight, get_specific_event_code


class MastersImplementWeightTests(TestCase):
    def test_specific_weight(self):
        self.assertEqual(get_implement_weight('JT', 'M', 'V80'), '400')
        self.assertEqual(get_implement_weight('JT', 'M', 'V85'), '400')

class IaafScoreTests(TestCase):
    """Test suite for the IAAF score calculation module."""

    def test_performance(self):
        """
        Test the function to calculate the required performance for a given
        score.
        """
        self.assertEqual(performance("F", "10000", 915), 2400.73)
        self.assertEqual(performance("M", "110H", 973), 14.01)
        self.assertEqual(performance("M", "110H", 974), 14)
        self.assertEqual(performance("F", "HJ", 1000), 1.82)
        self.assertEqual(performance("M", "WT", 1), 1.53)
        self.assertEqual(performance("F", "JT", 700), 41.68)
        self.assertEqual(performance("M", "PV", 1284), 6.16)

        # You need 1m to score 0, so that's what you get back
        self.assertEqual(performance("M", "PV", 0), 1.0)
        self.assertEqual(performance("M", "PV", -100), 1.0)
        self.assertEqual(performance("M", "NA", 500), None)

    def test_scoring_key(self):
        """
        Test the function to calculate the scoring key from the gender and
        event code.
        """
        self.assertEqual(scoring_key("m", "100"), "M-100")
        self.assertEqual(scoring_key("f", "400h"), "F-400H")
        self.assertEqual(scoring_key("M", "3000SC"), "M-3000SC")
        self.assertEqual(scoring_key("F", "lJ"), "F-LJ")
        self.assertEqual(scoring_key("m", "Hj"), "M-HJ")
        self.assertEqual(scoring_key("f", "jt"), "F-JT")
        self.assertEqual(scoring_key("M", "WT"), "M-WT")

    def test_score(self):
        """Test the function to calculate the score for a given performance."""
        self.assertEqual(score("F", "10000", 2400), 915)
        self.assertEqual(score("M", "110H", 14.01), 973)
        self.assertEqual(score("M", "110H", 14), 975)
        self.assertEqual(score("F", "HJ", 1.93), 1145)
        self.assertEqual(score("M", "WT", 1.53), 1)
        self.assertEqual(score("M", "WT", 1), 0)
        self.assertEqual(score("F", "JT", 41.68), 700)
        self.assertEqual(score("M", "PV", 6.16), 1284)

        self.assertEqual(score("M", "LJ", 0.5), 0)
        self.assertEqual(score("M", "100", 45), 0)

        self.assertEqual(score("?", "NA", 42), None)

        self.assertEqual(score("M", "1000", 150), 988)


    def test_unit_name(self):
        """Test the unit names for jumps, throws and track events."""
        self.assertEqual(unit_name("100"), "seconds")
        self.assertEqual(unit_name("200H"), "seconds")
        self.assertEqual(unit_name("3000SC"), "seconds")
        self.assertEqual(unit_name("LJ"), "metres")
        self.assertEqual(unit_name("PV"), "metres")
        self.assertEqual(unit_name("SP"), "metres")
        self.assertEqual(unit_name("WT"), "metres")

    def test_wma_adjusted_score(self):
        "Extra bonus for being old, used by WMA"
        self.assertEqual(score("M", "60H", 10.58), 437)


        self.assertEqual(score("M", "60H", 11.85, 50), 437)
        self.assertEqual(score("M", "LJ", 4.53, 50), 494)
        self.assertEqual(score("M", "800", 156, 75), 1035)

        # Javelin for different ages
        self.assertEqual(score("M", "JT", 30.0), 299) # senior
        self.assertEqual(score("M", "JT", 30.0, 50), 396) # M50
        self.assertEqual(score("M", "JT", 30.0, 80), 781) 
        self.assertEqual(score("M", "JT", 30.0, 85), 937) 

        
        # needs work, we need full weight event code in age factors e.g. SP6K,
        # but simple code e.g. SP in points calculation
        self.assertEqual(score("M", "SP", 8.05, 50), 451)

        self.assertEqual(score("F", "60H", 10.59, 53), 883)
        self.assertEqual(score("F", "HJ", 1.38, 53), 842)

        # PK's tests from BMAF events in June 2021
        self.assertEqual(score("M", "LJ", 5.0, 60), 821)
        # self.assertEqual(score("F", "80H", 12.0, 45), 1270)
        self.assertEqual(score("F", "HJ", 1.50, 70), 1741)
        self.assertEqual(score("M", "SP", 10.0, 70), 655)
        self.assertEqual(score("M", "SP", 10.0, 85), 904)
        self.assertEqual(score("M", "WT", 12.0, 85), 869)
        self.assertEqual(score("F", "SP", 7.0, 75), 715)
        self.assertEqual(score("F", "DT", 25.0, 75), 928)
        # self.assertEqual(score("F", "HJ", 1.50, 70), 1741)
        # self.assertEqual(score("F", "HJ", 1.50, 70), 1741)

    def test_esaa_adjusted_score(self):
        # Tha famous boys 800 issue.
        self.assertEqual(score("M", "800", 120, esaa=True), 769)





if __name__ == '__main__':
    main()
