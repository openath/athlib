"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main

from athlib import get_implement_weight as weight

class WeightTests(TestCase):
    """Test suite for implement canned data."""

    def test_a_few_uka_weights(self):
        self.assertEquals(weight("JT", "M", "SEN"), "800")
        self.assertEquals(weight("JT", "F", "V80"), "400")


    def test_malta_juniors(self):
        self.assertEquals(weight("JT", "M", "U14"), "500")
        self.assertEquals(weight("DT", "F", "U14"), "0.75")

if __name__ == '__main__':
    main()
