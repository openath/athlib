"""WMA single event age grades"""

from unittest import TestCase, main
from athlib import wma_age_grade, wma_age_factor, wma_world_best


class AgeGrade2015FactorTests(TestCase):
    def test_mens_100(self):
        self.assertEqual(0.5344, wma_age_factor("m", 5, "100", year="2015"))
        self.assertEqual(1.0, wma_age_factor("m", 30, "100", year="2015"))
        # self.assertEqual(0.9999, wma_age_factor("m", 35, "100", year="2015"))
        # self.assertEqual(0.8978, wma_age_factor("m", 50, "100", year="2015"))

class AgeGrade2023FactorTests(TestCase):
    def assertAlmostEqual(self, a, b, digits):
        delta = abs(a - b)
        epsilon = 10 ** -digits
        self.assertTrue(delta < epsilon)

    def test_find_by_distance(self):
        "Can look up a factor by distance as well as by event code"
        pass

    def test_mens_100(self):
        self.assertEqual(0.5344, wma_age_factor("m", 5, "100", year="2023"))
        self.assertEqual(1.0, wma_age_factor("m", 30, "100", year="2023"))
        self.assertEqual(0.9999, wma_age_factor("m", 35, "100", year="2023"))
        self.assertEqual(0.9031, wma_age_factor("m", 50, "100", year="2023"))


        self.assertEqual(1.0, wma_age_grade("m", 30, "100", "9.58", year="2023"))
        
        self.assertAlmostEqual(0.8064, wma_age_grade("m", 58, "100", "13.9", year="2023"),2)



    def test_womens_200(self):
        self.assertEqual(0.8454, wma_age_factor("f", 58, "200", year="2023"))
        self.assertAlmostEqual(91.38, wma_age_grade("f", 58, "200", "27.87", year="2023"))


    def test_womens_200(self):
        self.assertEqual(0.8454, wma_age_factor("f", 58, "200", year="2023"))


    def test_mldr_2020_factors(self):
        "Road stuff, from different parts of the table"
        self.assertEqual(0.9006, wma_age_factor("m", 47, "5K", year="2023"))
        self.assertEqual(0.9225, wma_age_factor("f", 47, "5K", year="2023"))


        self.assertEqual(1430.0, wma_world_best("f", "5M"))


        self.assertAlmostEqual(1.0092, wma_age_grade("f", 60, "5M", "30:00", year="2023"), 2)

    def test_interpolated_distance(self):
        "Not implemented yet but should be easy enough"
        # ag = wma_age_grade("f", 60, "5.31M", "40:00")
        pass



if __name__ == '__main__':
    main()
