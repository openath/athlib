"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main

from athlib import get_implement_weight as weight

class WeightTests(TestCase):
    """Test suite for implement canned data."""

    def test_a_few(self):
        self.assertEquals(weight("JT", "M", "SEN"), "800")
        self.assertEquals(weight("JT", "F", "V80"), "400")

if __name__ == '__main__':
    main()
