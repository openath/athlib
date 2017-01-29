"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main





class UtilsTests(TestCase):
    """Test suite for the IAAF score calculation module."""
    def test_track_sorting(self):
        """Verify that it sorts things into the standard order
        """
        from athlib.utils import sort_by_discipline
        stuff = [
            dict(e="100", name="Jordan"),
            dict(e="PV", name="Bilen"),
            dict(e="4x100", name="Assorted"),
            dict(e="400", name="Adam"),
            dict(e="400H", name="Richard"),
            dict(e="1500", name="Neil"),
            dict(e="3000SC", name="Andy"),
            dict(e="HT", name="Chris"),
            dict(e="TJ", name="Humphrey"),
            dict(e="", name="Nobody"),
            dict(e="CHUNDER-MILE", name="BinMan"),
        ]

        ordered = sort_by_discipline(stuff, attr="e")

        ordered_events = [d["e"] for d in ordered]
        self.assertEquals(
            ordered_events, 
            ['100', '400', '1500', '400H', '3000SC', 'PV', 'TJ', 'HT', '4x100', "", "CHUNDER-MILE"]
            )

        from athlib.utils import text_event_sort_key
        self.assertEquals(text_event_sort_key("100H"), "2_00100_100H")


        #Now sort objects, not dictionaries
        class Foo(object):
            pass
        obj1 = Foo()
        obj1.discipline = "HJ"

        obj2 = Foo()
        obj2.discipline = "200"

        obj3 = Foo()
        obj3.discipline = "4x200"


        stuff = [obj1, obj2, obj3]

        ordered = sort_by_discipline(stuff)
        self.assertEquals(ordered[0].discipline, "200")
        self.assertEquals(ordered[1].discipline, "HJ")

    def test_get_distance(self):
        "Extract distance in metres from discipline codes"
        from athlib.utils import get_distance
        self.assertEquals(get_distance("100"), 100)
        self.assertEquals(get_distance("110mH"), 110)
        self.assertEquals(get_distance("5K"), 5000)
        self.assertEquals(get_distance("MILE"), 1609)
        self.assertEquals(get_distance("5M"), 8045)
        self.assertEquals(get_distance("HM"), 21098)
        self.assertEquals(get_distance("MAR"), 42195)


        self.assertEquals(get_distance("XC"), None)

        self.assertEquals(get_distance("HJ"), None)



    def test_normalize_gender(self):
        from athlib.utils import normalize_gender
        self.assertEquals(normalize_gender("Male"), "M")
        self.assertEquals(normalize_gender("fEMale"), "F")
        self.assertRaises(ValueError, normalize_gender, "tranny")

    def test_str2num(self):
        from athlib.utils import str2num
        self.assertEquals(str2num("27"), 27)
        self.assertEquals(str2num("27.3"), 27.3)
        self.assertRaises(ValueError, str2num, "slow")        

    def test_parse_hms(self):
        from athlib.utils import parse_hms
        self.assertEquals(parse_hms("10"), 10)
        self.assertEquals(parse_hms("1:10"), 70)
        self.assertEquals(parse_hms("1:1:10"), 3670)
        self.assertEquals(parse_hms("1:01:10"), 3670)
        self.assertEquals(parse_hms("1:01:10.1"), 3670.1)

        #floats and ints come through as is
        self.assertEquals(parse_hms(10), 10)
        self.assertEquals(parse_hms(10.1), 10.1)

        self.assertRaises(ValueError, parse_hms, "slow")        
        self.assertRaises(ValueError, parse_hms, "3:32.x")        

    def test_format_seconds_as_time(self):
        from athlib.utils import format_seconds_as_time
        self.assertEquals(format_seconds_as_time(27.3), "27")
        self.assertEquals(format_seconds_as_time(27.3, prec=1), "27.3")
        self.assertEquals(format_seconds_as_time(27.3, prec=2), "27.30")
        self.assertEquals(format_seconds_as_time(27.3, prec=3), "27.300")

        #precision must be 0 to 3
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, 4)
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, None)
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, "hi")

        self.assertEquals(format_seconds_as_time(63), "1:03")
        self.assertEquals(format_seconds_as_time(7380), "2:03:00")


    def test_checkperf(self):
        from athlib.utils import check_performance_for_discipline as checkperf
        self.assertEquals(checkperf("XC", ""), "")
        self.assertEquals(checkperf("xc", ""), "")

        self.assertEquals(checkperf("HJ", "2.34"), "2.34")
        self.assertEquals(checkperf("HJ", "  2.34  "), "2.34")

        self.assertEquals(checkperf("60m", "7.62"), "7.62")

        self.assertEquals(checkperf("100m", "9.73456"), "9.73")
        self.assertEquals(checkperf("100m", "12"), "12.0")

        self.assertEquals(checkperf("400m", "63.1"), "63.1")
        self.assertEquals(checkperf("400m", "1:03.1"), "1:03.1")

        self.assertEquals(checkperf("800m", "2:33"), "2:33")

        #Correct French commas to decimals
        self.assertEquals(checkperf("200", "27,33"), "27.33")

        #Correct semicolons - fail to hit the shift key
        self.assertEquals(checkperf("800m", "2;33"), "2:33")


        self.assertEquals(checkperf("Mar", "2:03:59"), "2:03:59")

        self.assertEquals(checkperf("XC", "27:50"), "27:50"),

        self.assertEquals(checkperf("3000m", "0:11:15"), "11:15")

        self.assertEquals(checkperf("60m", "7:62"), "7.62")

        #Excel can prepend zeroes
        self.assertEquals(checkperf("5000", "0:14:53.2"), "14:53.2")
        self.assertEquals(checkperf("5000", "00:14:53.2"), "14:53.2")


        #Autocorrect 800/1500/3000 submitted as H:M:S
        self.assertEquals(checkperf("1500", "3:53:17"), "3:53.17")



        #Multi-events
        self.assertEquals(checkperf("DEC", "5875"), "5875")

        #Correct some common muddles
        self.assertEquals(checkperf("400", "52:03"), "52.03")



        self.assertRaises(ValueError, checkperf, "DEC", "23")
        self.assertRaises(ValueError, checkperf, "DEC", "10001")
        self.assertRaises(ValueError, checkperf, "DEC", "4:15.8")




        for (discipline, perf) in [
            ("HJ", "Soooo Highhhh!!!"),
            ("HJ", "2:03"),
            ("100m", "9.73w"),  # No wind, indoor figures or suffixes
            ("800m", "2.33"),  # seconds, should have been minutes
            ("XC", "27.50"),
            ("100M", "1:17:42:03"),  #Multi-day not supported
            ("400", "0:103"),  #poor format
            ("100", "8.5"), # > 11.0 metres per second
            ("5000", "3:45:27"), # < 0.5 m/sec
            ]:
            self.assertRaises(ValueError, checkperf, discipline, perf)





if __name__ == '__main__':
    main()
