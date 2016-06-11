"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from dateutil.parser import parse as parse_date
from datetime import date

from unittest import TestCase, main

from athlib.uka.agegroups import calc_age_group, prior_date
# from project.reference.trackutils import normalise_club_name
# from .trackutils import check_performance_for_discipline as check_performance
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class AgeGroupTests(TestCase):

    def assertAgeGroup(self, dob, match_date, category, expected):
        ag = calc_age_group(dob, match_date, category)
        self.assertEquals(ag, expected, "Unexpected age group, expected %s but got %s" % (expected, ag))


    def test_cat_check(self):
        self.assertRaises(Exception, calc_age_group, date(1966,1,1), date(2015,1,3), "FOO")

    def test_cutoff_date(self):
        self.assertEquals(
            prior_date(date(2015,1,3), 8, 31),
            date(2014,8,31)
            )

        self.assertEquals(
            prior_date(date(2014,9,30), 8, 31),
            date(2014,8,31)
            )


    def test_vets_xc(self):
        ag = calc_age_group(date(1966,3,21), date(2015,1,3), "XC", vets=False)
        self.assertEquals(ag, "SEN")
        
    def test_no_vets_when_not_required(self):
        self.assertAgeGroup(date(1966,3,21), date(2015,1,3), "XC", "V45")

    
    def test_juniors_xc(self):

        #some simple cases - birthday and match both end of october.
        # an athlete who is 17 on the day was actually 16 when season started
        self.assertAgeGroup(date(2005,10,31), date(2014,10,31), "XC", "U11")
        self.assertAgeGroup(date(2004,10,31), date(2014,10,31), "XC", "U11")
        self.assertAgeGroup(date(2003,10,31), date(2014,10,31), "XC", "U13")
        self.assertAgeGroup(date(2002,10,31), date(2014,10,31), "XC", "U13")
        self.assertAgeGroup(date(2001,10,31), date(2014,10,31), "XC", "U13")
        self.assertAgeGroup(date(2000,10,31), date(2014,10,31), "XC", "U15")
        self.assertAgeGroup(date(1999,10,31), date(2014,10,31), "XC", "U15")
        self.assertAgeGroup(date(1998,10,31), date(2014,10,31), "XC", "U17")
        self.assertAgeGroup(date(1997,10,31), date(2014,10,31), "XC", "U17")
        self.assertAgeGroup(date(1996,10,31), date(2014,10,31), "XC", "U20")
        self.assertAgeGroup(date(1995,10,31), date(2014,10,31), "XC", "U20")
        self.assertAgeGroup(date(1994,10,31), date(2014,10,31), "XC", "U20")
        self.assertAgeGroup(date(1993,10,31), date(2014,10,31), "XC", "SEN")
        


        self.assertAgeGroup(date(1998,9,8), date(2015,9,30), "XC", "U17")
        # self.assertAgeGroup(date(2008,1,3), date(2015,1,3), "XC" , "U11")
        # self.assertAgeGroup(date(2002,10,10),date(2014,1,3), "XC", "U13")

        #two actual errors from Surrey XC where we had a cutoff date of 30 Sep
        self.assertAgeGroup(date(1994,9,29), date(2015,1,3), "XC" , "U20")
        self.assertAgeGroup(date(1997,9,1), date(2015,1,3), "XC" , "U17")


        #30th September is considered start of season
        #29th September is considered end of season

    def test_track_and_field(self):
        "Examples provided by Nicola Fleet of Surrey AAA"
        samples = """
            1/1/1994    14/2/2015   SEN
            31/8/1994   14/2/2015   SEN
            1/9/1994    14/2/2015   SEN
            30/9/1994   14/2/2015   SEN
            1/10/1994   14/2/2015   SEN
            31/12/1994  14/2/2015   SEN
                    
            1/1/1995    14/2/2015   SEN
            31/8/1995   14/2/2015   SEN
            1/9/1995    14/2/2015   SEN
            30/9/1995   14/2/2015   SEN
            1/10/1995   14/2/2015   SEN
            31/12/1995  14/2/2015   SEN
                    
            1/1/1996    14/2/2015   U20
            31/8/1996   14/2/2015   U20
            1/9/1996    14/2/2015   U20
            30/9/1996   14/2/2015   U20
            1/10/1996   14/2/2015   U20
            31/12/1996  14/2/2015   U20
                    
            1/1/1997    14/2/2015   U20
            31/8/1997   14/2/2015   U20
            1/9/1997    14/2/2015   U20
            30/9/1997   14/2/2015   U20
            1/10/1997   14/2/2015   U20
            31/12/1997  14/2/2015   U20
                    
            1/1/1998    14/2/2015   U20
            31/8/1998   14/2/2015   U20
            1/9/1998    14/2/2015   U17
            30/9/1998   14/2/2015   U17
            1/10/1998   14/2/2015   U17
            31/12/1998  14/2/2015   U17
                    
            1/1/1999    14/2/2015   U17
            31/8/1999   14/2/2015   U17
            1/9/1999    14/2/2015   U17
            30/9/1999   14/2/2015   U17
            1/10/1999   14/2/2015   U17
            31/12/1999  14/2/2015   U17
                    
            1/1/2000    14/2/2015   U17
            31/8/2000   14/2/2015   U17
            1/9/2000    14/2/2015   U15
            30/9/2000   14/2/2015   U15
            1/10/2000   14/2/2015   U15
            31/12/2000  14/2/2015   U15
                    
            1/1/2001    14/2/2015   U15
            31/8/2001   14/2/2015   U15
            1/9/2001    14/2/2015   U15
            30/9/2001   14/2/2015   U15
            1/10/2001   14/2/2015   U15
            31/12/2001  14/2/2015   U15
                    
            1/1/2002    14/2/2015   U15
            31/8/2002   14/2/2015   U15
            1/9/2002    14/2/2015   U13
            30/9/2002   14/2/2015   U13
            1/10/2002   14/2/2015   U13
            31/12/2002  14/2/2015   U13
                    
            1/1/2003    14/2/2015   U13
            31/8/2003   14/2/2015   U13
            1/9/2003    14/2/2015   U13
            30/9/2003   14/2/2015   U13
            1/10/2003   14/2/2015   U13
            31/12/2003  14/2/2015   U13
                    
            1/1/2004    14/2/2015   U13
            31/8/2004   14/2/2015   U13
            1/9/2004    14/2/2015   U11
            30/9/2004   14/2/2015   U11
            1/10/2004   14/2/2015   U11
            31/12/2004  14/2/2015   U11
                    
            1/1/2005    14/2/2015   U11
            31/8/2005   14/2/2015   U11
            1/9/2005    14/2/2015   U11
            30/9/2005   14/2/2015   U11
            1/10/2005   14/2/2015   U11
            31/12/2005  14/2/2015   U11
            """
        failures = 0
        messages = []
        for line in samples.strip().split('\n'):
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith('#'):
                continue
            txtdob, txtmatch, expected = trimmed.split()
            date_of_birth = parse_date(txtdob, dayfirst=True).date()
            match_date = parse_date(txtmatch, dayfirst=True).date()


            ag = calc_age_group(date_of_birth, match_date, "TF")
            if ag != expected:
                failures += 1
                msg = "Given '%s', got '%s'" % (trimmed, ag)
                messages.append(msg)

        self.assertEquals(failures, 0, "\n".join(messages))
            #self.assertEquals(ag, expected, "Unexpected age group.  Test case is '%s', got '%s'" % (trimmed, ag))


if __name__=='__main__':
    main()