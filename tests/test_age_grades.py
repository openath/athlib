"""WMA single event age grades"""

from unittest import TestCase, main
from athlib import wma_age_grade, wma_age_factor, wma_world_best
from athlib.wma.agegrader import AgeGrader


class AgeGraderTests(TestCase):
    def assertBetween(self, a, b, c):
        "b should be between and c"
        if b > a:
            self.assertTrue(b < c)
        else:
            self.assertTrue(c < b)

    def test_interpolate_factors(self):
        # exploring some inner functions.
        ag = AgeGrader(year=2023)
        self.assertEqual(ag.event_code_to_kind("800"), "track")
        self.assertEqual(ag.event_code_to_kind("5M"), "road")

        distance = "2400"

        fac1 = ag.calculate_factor("m", 40, "2000")         
        fac2 = ag.calculate_factor("m", 40, distance)
        fac3 = ag.calculate_factor("m", 40, "3000")

        factors = sorted([fac1, fac2, fac3])

        self.assertEqual(fac2, factors[1]) # should be in the middle

        bestimate = ag.world_best("m", distance)
        # should be around 6 minutes, a bit over 4 laps
        self.assertTrue(bestimate < 400)
        self.assertTrue(bestimate > 300)

        # 6 laps record should be around 5:45, so this will be 95% age grade 
        grade = wma_age_grade("m", 30, str(distance), "6:00")
        self.assertTrue(grade < 1.0)
        self.assertTrue(grade > 0.9)

    def test_interpolate_xc(self):
        ag = AgeGrader(year=2023)
        grade1 = wma_age_factor("m", 50, "10K") # standard
        grade2 = wma_age_factor("m", 50, "11K") # not standard
        grade3 = wma_age_factor("m", 50, "12K") # standard
        ordered = sorted([grade1, grade2, grade3])
        # should be in between the two standard factors
        self.assertEqual(ordered[1], grade2)

        # we should get a grade for a funny distance
        self.assertTrue(wma_age_grade("m", 58, "5.31M", "41:37") > 0)


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


    def test_find_row_by_event(self):
        ag = AgeGrader(year=2023)
        tbl = ag.get_data()["m"]
        self.assertTrue(ag.find_row_by_event("800", tbl) is not None)

    def test_interpolated_distance(self):
        "Example constructed by hand"
        ag = wma_age_grade("f", 60, "5.3M", "40:00")
        self.assertTrue(ag > 0.82)
        self.assertTrue(ag < 0.8202)



        # check interpolation where below the shortest distance - 42 metre sprint
        self.assertEqual(5.54, wma_world_best("m", "42"))
        self.assertEqual(1.0, wma_age_grade("m", 25, "42", 5.54))


        # check interpolation where above the longest distance (200K)
        # very close to Sorokin's actual 24 hour world record!
        best = wma_world_best("m", "200M")
        self.assertTrue((best > 84955) and (best < 84966))



if __name__ == '__main__':
    main()
