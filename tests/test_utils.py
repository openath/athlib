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
            ['100', '400', '1500', '400H', '3000SC', 'PV',
                'TJ', 'HT', '4x100', "", "CHUNDER-MILE"]
        )

        from athlib.utils import text_discipline_sort_key
        self.assertEquals(text_discipline_sort_key("100H"), "2_00100_100H")

        # Now sort objects, not dictionaries
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
        self.assertEquals(get_distance("4xrelay"), None)
        self.assertEquals(get_distance("4x100"), 400)
        self.assertEquals(get_distance("4x400"), 1600)
        self.assertEquals(get_distance("7.5M"), 12067)
        self.assertEquals(get_distance("7.5SC"), None)
        self.assertEquals(get_distance("440Y"), 402)
        self.assertEquals(get_distance("3000W"), 3000)
        self.assertEquals(get_distance("3KW"), 3000)
        self.assertEquals(get_distance("3kmW"), 3000)

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

        # floats and ints come through as is
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

        # precision must be 0 to 3
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
        self.assertEquals(checkperf("100m", "12"), "12.00")
        self.assertEquals(checkperf("400m", "63.1"), "63.10")
        self.assertEquals(checkperf("400m", "1:03.1"), "1:03.1")
        self.assertEquals(checkperf("800m", "2:33"), "2:33")
        self.assertEquals(checkperf("200", "27,33"), "27.33")   # Correct French commas to decimals
        self.assertEquals(checkperf("800m", "2;33"), "2:33")    # Correct semicolons - fail to hit the shift key
        self.assertEquals(checkperf("800", "2.33"), "2:33")     # Correct dots for some events
        self.assertEquals(checkperf("Mar", "2:03:59"), "2:03:59")
        self.assertEquals(checkperf("XC", "27:50"), "27:50"),
        self.assertEquals(checkperf("3000m", "0:11:15"), "11:15")
        self.assertEquals(checkperf("60m", "7:62"), "7.62")
        self.assertEquals(checkperf("5000", "0:14:53.2"), "14:53.2")    # Excel can prepend zeroes
        self.assertEquals(checkperf("5000", "00:14:53.2"), "14:53.2")
        self.assertEquals(checkperf("1500", "3:53:17"), "3:53.17")      # Autocorrect 800/1500/3000 submitted as H:M:S
        self.assertEquals(checkperf("DEC", "5875"), "5875")             # Multi-events
        self.assertEquals(checkperf("400", "52:03"), "52.03")           # Correct some common muddles
        self.assertEquals(checkperf("PEN", "0"), "0")                   # low score is allowed
        self.assertEquals(checkperf("3000mW", "0:24:15"), "24:15")
        self.assertEquals(checkperf("3KW", "0:24:15"), "24:15")

    def test_checkperf_raises(self):
        from athlib.utils import check_performance_for_discipline as checkperf
        #self.assertRaises(ValueError, checkperf, "DEC", "23") #lower limit no longer enforced
        self.assertRaises(ValueError, checkperf, "DEC", "10001")
        self.assertRaises(ValueError, checkperf, "DEC", "4:15.8")
        self.assertRaises(ValueError, checkperf, "HJ", "25"),
        self.assertRaises(ValueError, checkperf, "HJ", "Soooo Highhhh!!!"),
        self.assertRaises(ValueError, checkperf, "HJ", "2:03"),
        self.assertRaises(ValueError, checkperf, "100m", "9.73w"),  # No wind, indoor figures or suffixes
        #self.assertRaises(ValueError, checkperf, "800m", "2.33"),  # seconds, should have been minutes dot converted
        self.assertRaises(ValueError, checkperf, "XC", "27.50"),
        self.assertRaises(ValueError, checkperf, "100M", "1:17:42:03"),  # Multi-day not supported
        self.assertRaises(ValueError, checkperf, "400", "0:103"),  # poor format
        self.assertRaises(ValueError, checkperf, "100", "8.5"),  # > 11.0 metres per second
        self.assertRaises(ValueError, checkperf, "5000", "3:45:27"),  # < 0.5 m/sec
        self.assertRaises(ValueError, checkperf, "3KW", "2:34")

    def test_discipline_sort_key(self):
        '''should see if event ordering will work'''
        from athlib.utils import discipline_sort_key
        self.assertEqual(discipline_sort_key(''),(6, 0, "?"))
        self.assertEqual(discipline_sort_key('HJ'),(3, 0, "HJ"))
        self.assertEqual(discipline_sort_key('LJ'),(3, 2, "LJ"))
        self.assertEqual(discipline_sort_key('PV'),(3, 1, "PV"))
        self.assertEqual(discipline_sort_key('100'),(1, 100, "100"))
        self.assertEqual(discipline_sort_key('4x400'),(5, 400, "4x400"))
        self.assertEqual(discipline_sort_key('JT'),(4, 7, "JT"))
        self.assertEqual(discipline_sort_key('200H'),(2, 200, "200H"))

    def test_text_discipline_sort_key(self):
        '''should see if event ordering will work'''
        from athlib.utils import text_discipline_sort_key
        self.assertEqual(text_discipline_sort_key(''),"6_00000_?")
        self.assertEqual(text_discipline_sort_key('HJ'),"3_00000_HJ")
        self.assertEqual(text_discipline_sort_key('LJ'),"3_00002_LJ")
        self.assertEqual(text_discipline_sort_key('PV'),"3_00001_PV")
        self.assertEqual(text_discipline_sort_key('100'),"1_00100_100")
        self.assertEqual(text_discipline_sort_key('4x400'),"5_00400_4x400")
        self.assertEqual(text_discipline_sort_key('JT'),"4_00007_JT")
        self.assertEqual(text_discipline_sort_key('200H'),"2_00200_200H")

    def test_sort_by_discipline(self):
        '''sort a list of pseudo-events'''
        events = [
            {'e':'','a':60},
            {'e':'HJ','a':30},
            {'e':'LJ','a':32},
            {'e':'PV','a':31},
            {'e':'100','a':1100},
            {'e':'800','a':1800},
            {'e':'4x400','a':5400},
            {'e':'JT','a':47},
            {'e':'200H','a':2200},
            ]
        from athlib.utils import sort_by_discipline
        sevents = [e['a'] for e in sort_by_discipline(events,'e')]
        self.assertEqual(sevents,[1100,1800,2200,30,31,32,47,5400,60])

    def test_event_codes_match_correctly(self):
        from athlib.codes import PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD, \
                PAT_RACES_FOR_DISTANCE, PAT_RELAYS, PAT_HURDLES, PAT_MULTI, PAT_EVENT_CODE
        tpats = [PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD, PAT_RACES_FOR_DISTANCE, PAT_RELAYS, PAT_HURDLES, PAT_MULTI,
                PAT_EVENT_CODE]
        tpatNames = """PAT_THROWS PAT_JUMPS PAT_TRACK PAT_ROAD PAT_RACES_FOR_DISTANCE PAT_RELAYS PAT_HURDLES PAT_MULTI
            PAT_EVENT_CODE""".split()
        codePats = [
                ('100',PAT_TRACK),
                ('110mH',PAT_HURDLES),
                ('1500',PAT_TRACK),
                ('1HR',PAT_RACES_FOR_DISTANCE),
                ('1HW',PAT_RACES_FOR_DISTANCE),
                ('24HR',PAT_RACES_FOR_DISTANCE),
                ('24HW',PAT_RACES_FOR_DISTANCE),
                ('2HR',PAT_RACES_FOR_DISTANCE),
                ('2HW',PAT_RACES_FOR_DISTANCE),
                ('3000SC',PAT_TRACK),
                ('3000W',PAT_TRACK),
                ('3kmW',PAT_ROAD),
                ('3KW',PAT_ROAD),
                ('400',PAT_TRACK),
                ('400H',PAT_HURDLES),
                ('440Y',PAT_TRACK),
                ('4x100',PAT_RELAYS),
                ('4x100',PAT_RELAYS),
                ('4x400',PAT_RELAYS),
                ('4xrelay',PAT_RELAYS),
                ('5K',PAT_ROAD),
                ('5M',PAT_ROAD),
                ('7.5M',PAT_ROAD),
                ('BT',PAT_THROWS),
                ('BT1.5K',PAT_THROWS),
                ('BT2K',PAT_THROWS),
                ('CHUNDER-MILE',PAT_TRACK),
                ('HJ',PAT_JUMPS),
                ('HM',PAT_ROAD),
                ('HT',PAT_THROWS),
                ('MAR',PAT_ROAD),
                ('MILE',PAT_ROAD),
                ('HM',PAT_ROAD),
                ('LJ',PAT_JUMPS),
                ('PV',PAT_JUMPS),
                ('TJ',PAT_JUMPS),
                ('XC',PAT_ROAD),
                ]
        errs = []
        show = lambda p: repr(sorted(list(p)))
        for code, goodPat in codePats:
            M = set([tpatNames[tpats.index(pat)] for pat in tpats if pat.match(code)])
            if not isinstance(goodPat,(list,tuple)):
                goodPat = [goodPat]
            goodPat.append(PAT_EVENT_CODE)
            ok = set([tpatNames[tpats.index(pat)] for pat in goodPat])
            if M != ok:
                errs.append("%r matched %r should have matched %r" % (code,show(M),show(ok)))
        errs = '\n'.join(errs)
        self.assertEqual(errs,'','event matching failures\n%s\n'%errs)

if __name__ == '__main__':
    main()
