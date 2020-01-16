"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main

from athlib import get_implement_weight as weight, get_specific_event_code as specify

class WeightTests(TestCase):
    """Test suite for implement canned data."""

    def test_a_few_uka_weights(self):
        self.assertEquals(weight("JT", "M", "SEN"), "800")
        self.assertEquals(weight("JT", "F", "V80"), "400")


    def test_malta_juniors(self):
        self.assertEquals(weight("JT", "M", "U14"), "500")
        self.assertEquals(weight("DT", "F", "U14"), "0.75")

    def test_unknown_implement(self):
        self.assertEquals(weight("OT", "M", "50"), "")

    def test_masters_weights(self):
        self.assertEquals(weight("JT", "M", "V70"), "500")
        self.assertEquals(weight("JT", "F", "V70"), "500")
        self.assertEquals(weight("JT", "F", "V90"), "400")

        self.assertEquals(weight("SP", "F", "V40"), "4.00")
        self.assertEquals(weight("SP", "F", "V50"), "3.00")


    def test_specific_codes(self):
        self.assertEquals(specify("JT", "M", "V70"), "JT500")
        self.assertEquals(specify("JT", "M", "SEN"), "JT800")
        self.assertEquals(specify("JT", "M", "U13"), "JT400")

        self.assertEquals(specify("SP", "M", "SEN"), "SP7.26K")
        self.assertEquals(specify("SP", "F", "SEN"), "SP4K")

        self.assertEquals(specify("WT", "M", "SEN"), "WT15.88K")
        self.assertEquals(specify("WT", "F", "SEN"), "WT9.08K")

        self.assertEquals(specify("SP", "M", "V50"), "SP6K")


if __name__ == '__main__':
    main()
