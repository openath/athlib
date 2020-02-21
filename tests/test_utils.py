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
        self.assertEqual(
            ordered_events,
            ['100', '400', '1500', '400H', '3000SC', 'PV',
                'TJ', 'HT', '4x100', "", "CHUNDER-MILE"]
        )

        from athlib.utils import text_discipline_sort_key
        self.assertEqual(text_discipline_sort_key("100H"), "2_00100_100H")

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
        self.assertEqual(ordered[0].discipline, "200")
        self.assertEqual(ordered[1].discipline, "HJ")

    def test_get_distance(self):
        "Extract distance in metres from discipline codes"
        from athlib.utils import get_distance
        self.assertEqual(get_distance("100"), 100)
        self.assertEqual(get_distance("110mH"), 110)
        self.assertEqual(get_distance("5K"), 5000)
        self.assertEqual(get_distance("MILE"), 1609)
        self.assertEqual(get_distance("CHUNDER-MILE"), 1609)
        self.assertEqual(get_distance("5M"), 8045)
        self.assertEqual(get_distance("HM"), 21098)
        self.assertEqual(get_distance("MAR"), 42195)
        self.assertEqual(get_distance("XC"), None)
        self.assertEqual(get_distance("HJ"), None)
        self.assertEqual(get_distance("4xrelay"), None)
        self.assertEqual(get_distance("4x100"), 400)
        self.assertEqual(get_distance("4x100H"), 400)
        self.assertEqual(get_distance("3x100h"), 300)
        self.assertEqual(get_distance("4x400"), 1600)
        self.assertEqual(get_distance("7.5M"), 12067)
        self.assertEqual(get_distance("7.5SC"), None)
        self.assertEqual(get_distance("440Y"), 402)
        self.assertEqual(get_distance("3000W"), 3000)
        self.assertEqual(get_distance("3KW"), 3000)
        self.assertEqual(get_distance("3kmW"), 3000)

    def test_normalize_gender(self):
        from athlib.utils import normalize_gender
        self.assertEqual(normalize_gender("Male"), "M")
        self.assertEqual(normalize_gender(" Male "), "M")
        self.assertEqual(normalize_gender("fEMale"), "F")
        self.assertEqual(normalize_gender(" fEMale "), "F")
        self.assertRaises(ValueError, normalize_gender, "  ")
        self.assertRaises(ValueError, normalize_gender, " tranny ")
        self.assertRaises(ValueError, normalize_gender, "")
        self.assertRaises(ValueError, normalize_gender, 100)

    def test_normalize_event_code(self):
        from athlib.utils import normalize_event_code
        tests = [
                ['400H 67.2cm 9.5m 9m', '400H67.2cm9.5m9m'],
                ['400H 67.20cm 9.50m 9.0m', '400H67.2cm9.5m9m'],
                ['400H 67.00cm 9.50m 9.0m', '400H67cm9.5m9m'],
                ['400H 67.00cm 9.50m 9.0m ', '400H67cm9.5m9m'],
                [' 400H 67.2cm 9.5m 9m', '400H67.2cm9.5m9m'],
                [' 400H 67.20cm 9.50m 9.0m', '400H67.2cm9.5m9m'],
                [' 400H 67.00cm 9.50m 9.0m', '400H67cm9.5m9m'],
                [' 400H 67.00cm 9.50m 9.0m ', '400H67cm9.5m9m'],
                ['DT 1.5 Kg ', 'DT1.5K'],
                ['DT1.5 Kg', 'DT1.5K'],
                ['DT 1.5Kg', 'DT1.5K'],
                [' DT 1.5 Kg ', 'DT1.5K'],
                [' DT1.5 Kg', 'DT1.5K'],
                [' DT 1.5Kg', 'DT1.5K'],
                ]
        for evc, xevc in tests:
            r = normalize_event_code(evc)
            self.assertEqual(r,xevc,
                "normalize_event_code(%r) is %r not expected %r" % (evc, r,xevc))

    def test_str2num(self):
        from athlib.utils import str2num
        self.assertEqual(str2num("27"), 27)
        self.assertEqual(str2num("27.3"), 27.3)
        self.assertRaises(ValueError, str2num, "slow")
        self.assertRaises(ValueError, str2num, "3:0")

    def test_parse_hms(self):
        from athlib.utils import parse_hms
        self.assertEqual(parse_hms("10"), 10)
        self.assertEqual(parse_hms("1:10"), 70)
        self.assertEqual(parse_hms("1:1:10"), 3670)
        self.assertEqual(parse_hms("1:01:10"), 3670)
        self.assertEqual(parse_hms("1:01:10.1"), 3670.1)

        # floats and ints come through as is
        self.assertEqual(parse_hms(10), 10)
        self.assertEqual(parse_hms(10.1), 10.1)

        self.assertRaises(ValueError, parse_hms, "slow")
        self.assertRaises(ValueError, parse_hms, "3:32.x")

    def test_format_seconds_as_time(self):
        from athlib.utils import format_seconds_as_time
        self.assertEqual(format_seconds_as_time(27.0), "27")
        self.assertEqual(format_seconds_as_time(27.3), "28")
        self.assertEqual(format_seconds_as_time(27.3, prec=1), "27.3")
        self.assertEqual(format_seconds_as_time(27.3, prec=2), "27.30")
        self.assertEqual(format_seconds_as_time(27.3, prec=3), "27.300")

        # precision must be 0 to 3
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, 4)
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, None)
        self.assertRaises(ValueError, format_seconds_as_time, 27.3, "hi")

        self.assertEqual(format_seconds_as_time(63), "1:03")
        self.assertEqual(format_seconds_as_time(7380), "2:03:00")
        self.assertEqual(format_seconds_as_time(3599.1), "1:00:00")
        self.assertEqual(format_seconds_as_time(3599.91, 1), "1:00:00.0")

    def test_checkperf(self):
        from athlib.utils import check_performance_for_discipline as checkperf
        self.assertEqual(checkperf("XC", ""), "")
        self.assertEqual(checkperf("xc", ""), "")
        self.assertEqual(checkperf("HJ", "2.34"), "2.34")
        self.assertEqual(checkperf("HJ", "  2.34  "), "2.34")
        self.assertEqual(checkperf("60m", "7.62"), "7.62")
        self.assertEqual(checkperf("100m", "9.73456"), "9.73")
        self.assertEqual(checkperf("100m", "12"), "12.00")
        self.assertEqual(checkperf("400m", "63.1"), "63.10")
        self.assertEqual(checkperf("400m", "1:03.1"), "1:03.1")
        self.assertEqual(checkperf("800m", "2:33"), "2:33")
        self.assertEqual(checkperf("200", "27,33"), "27.33")    # Correct French commas to decimals
        self.assertEqual(checkperf("800m", "2;33"), "2:33") # Correct semicolons - fail to hit the shift key
        self.assertEqual(checkperf("800", "2.33"), "2:33")      # Correct dots for some events
        self.assertEqual(checkperf("Mar", "2:03:59"), "2:03:59")
        self.assertEqual(checkperf("XC", "27:50"), "27:50"),
        self.assertEqual(checkperf("3000m", "0:11:15"), "11:15")
        self.assertEqual(checkperf("60m", "7:62"), "7.62")
        self.assertEqual(checkperf("5000", "0:14:53.2"), "14:53.2") # Excel can prepend zeroes
        self.assertEqual(checkperf("5000", "00:14:53.2"), "14:53.2")
        self.assertEqual(checkperf("1500", "3:53:17"), "3:53.17")       # Autocorrect 800/1500/3000 submitted as H:M:S
        self.assertEqual(checkperf("DEC", "5875"), "5875")              # Multi-events
        self.assertEqual(checkperf("400", "52:03"), "52.03")            # Correct some common muddles
        self.assertEqual(checkperf("PEN", "0"), "0")                    # low score is allowed
        self.assertEqual(checkperf("3000mW", "0:24:15"), "24:15")
        self.assertEqual(checkperf("3KW", "0:24:15"), "24:15")
        self.assertEqual(checkperf("ST2.1", "15.3"), "15.30")
        self.assertEqual(checkperf("GDT2.2", "15.4"), "15.40")
        self.assertEqual(checkperf("BT1.1", "15.5"), "15.50")
        self.assertEqual(checkperf("WT1.2", "15.6"), "15.60")
        self.assertEqual(checkperf("SWT1.3", "15.7"), "15.70")
        self.assertEqual(checkperf("OT1.4", "15.7"), "15.70")
        self.assertEqual(checkperf("SHJ", "  2.34   "), "2.34")
        self.assertEqual(checkperf("SLJ", "  2.34   "), "2.34")
        self.assertEqual(checkperf("stj", "  2.34   "), "2.34")

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
        self.assertEqual(discipline_sort_key('LJ'),(3, 3, "LJ"))
        self.assertEqual(discipline_sort_key('PV'),(3, 2, "PV"))
        self.assertEqual(discipline_sort_key('100'),(1, 100, "100"))
        self.assertEqual(discipline_sort_key('4x400'),(5, 400, "4x400"))
        self.assertEqual(discipline_sort_key('JT'),(4, 10, "JT"))
        self.assertEqual(discipline_sort_key('200H'),(2, 200, "200H"))
        self.assertEqual(discipline_sort_key('SLJ'),(3, 4, "SLJ"))
        self.assertEqual(discipline_sort_key('SHJ'),(3, 1, "SHJ"))
        self.assertEqual(discipline_sort_key('GDT'),(4, 12, "GDT"))

    def test_text_discipline_sort_key(self):
        '''should see if event ordering will work'''
        from athlib.utils import text_discipline_sort_key
        self.assertEqual(text_discipline_sort_key(''),"6_00000_?")
        self.assertEqual(text_discipline_sort_key('HJ'),"3_00000_HJ")
        self.assertEqual(text_discipline_sort_key('LJ'),"3_00003_LJ")
        self.assertEqual(text_discipline_sort_key('PV'),"3_00002_PV")
        self.assertEqual(text_discipline_sort_key('100'),"1_00100_100")
        self.assertEqual(text_discipline_sort_key('4x400'),"5_00400_4x400")
        self.assertEqual(text_discipline_sort_key('JT'),"4_00010_JT")
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
            {'e':'MILE','a':1609},
            ]
        from athlib.utils import sort_by_discipline
        sevents = [e['a'] for e in sort_by_discipline(events,'e')]
        self.assertEqual(sevents,[1100,1800,2200,30,31,32,47,5400,60,1609])

    def test_event_codes_match_correctly(self):
        from athlib.codes import PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD, \
                PAT_RACES_FOR_DISTANCE, PAT_RELAYS, PAT_HURDLES, PAT_MULTI, PAT_EVENT_CODE
        tpats = [PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD, PAT_RACES_FOR_DISTANCE, PAT_RELAYS, PAT_HURDLES, PAT_MULTI,
                PAT_EVENT_CODE]
        tpatNames = """PAT_THROWS PAT_JUMPS PAT_TRACK PAT_ROAD PAT_RACES_FOR_DISTANCE PAT_RELAYS PAT_HURDLES PAT_MULTI
            PAT_EVENT_CODE""".split()
        codePats = [
                ('100',PAT_TRACK),
                #('110mH',PAT_HURDLES), #Andy Check
                ('1500',PAT_TRACK),
                ('1HR',PAT_RACES_FOR_DISTANCE),
                ('1HW',PAT_RACES_FOR_DISTANCE),
                ('24HR',PAT_RACES_FOR_DISTANCE),
                ('24HW',PAT_RACES_FOR_DISTANCE),
                ('2HR',PAT_RACES_FOR_DISTANCE),
                ('2HW',PAT_RACES_FOR_DISTANCE),
                ('3000SC',[PAT_HURDLES,PAT_TRACK]),
                ('3000W',PAT_TRACK),
                #('3kmW',PAT_ROAD), #Andy check
                ('3KW',PAT_ROAD),
                ('400',PAT_TRACK),
                ('400H',[PAT_TRACK,PAT_HURDLES]),
                ('400H 67.2cm 9.5m',[PAT_TRACK,PAT_HURDLES]),
                ('2000H 67.2cm',[PAT_TRACK,PAT_HURDLES]),
                ('400H 67.2cm 9.5m 10m',[PAT_TRACK,PAT_HURDLES]),
                ('400H 33',[PAT_TRACK,PAT_HURDLES]),
                ('400H 36',[PAT_TRACK,PAT_HURDLES]),
                ('4000H 9.4cm',None),
                ('4000H 0.672m 10.9m',None),
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
                #('CHUNDER-MILE',PAT_TRACK),    #Andy check
                ('HJ',PAT_JUMPS),
                ('SHJ',PAT_JUMPS),
                ('HM',PAT_ROAD),
                ('HT',PAT_THROWS),
                ('BT',PAT_THROWS),
                ('OT',PAT_THROWS),
                ('ST',PAT_THROWS),
                ('SWT',PAT_THROWS),
                ('GDT',PAT_THROWS),
                ('MAR',PAT_ROAD),
                ('MILE',PAT_ROAD),
                ('HM',PAT_ROAD),
                ('LJ',PAT_JUMPS),
                ('SLJ',PAT_JUMPS),
                ('PV',PAT_JUMPS),
                ('TJ',PAT_JUMPS),
                ('STJ',PAT_JUMPS),
                ('XC',PAT_ROAD),
                ]
        errs = []
        show = lambda p: repr(sorted(list(p)))
        for code, goodPat in codePats:
            M = set([tpatNames[tpats.index(pat)] for pat in tpats if pat.match(code)])
            if goodPat is None:
                goodPat = []
            else:
                if not isinstance(goodPat,(list,tuple)):
                    goodPat = [goodPat]
                goodPat.append(PAT_EVENT_CODE)
            ok = set([tpatNames[tpats.index(pat)] for pat in goodPat])
            if M != ok:
                errs.append("%r matched %r should have matched %r" % (code,show(M),show(ok)))
        errs = '\n'.join(errs)
        self.assertEqual(errs,'','event matching failures\n%s\n'%errs)

    def test_round_up_str_num(self):
        from athlib.utils import round_up_str_num
        bad = ['%4s %8s %8s %8s %s' % ('prec', 'text','expected','result','Correct')]
        for prec, v, x in (
            (3, '11.9990', '11.999'),
            (3, '11.9991', '12.000'),
            (3, '11.4502', '11.451'),
            (3, '11.4520', '11.452'),
            (3, '11.4500', '11.450'),
            (3, '11.452', '11.452'),
            (3, '11.450', '11.450'),
            (3, '11.000', '11.000'),
            (3, '11.0001', '11.001'),
            (3, '11.45', '11.450'),
            (3, '11.05', '11.050'),
            (3, '11.4', '11.400'),
            (3, '11.', '11.000'),
            (3, '11', '11.000'),
            (3, '1.9990', '1.999'),
            (3, '1.9991', '2.000'),
            (3, '1.4502', '1.451'),
            (3, '1.4520', '1.452'),
            (3, '1.4500', '1.450'),
            (3, '1.452', '1.452'),
            (3, '1.450', '1.450'),
            (3, '1.000', '1.000'),
            (3, '1.0001', '1.001'),
            (3, '1.45', '1.450'),
            (3, '1.05', '1.050'),
            (3, '1.4', '1.400'),
            (3, '1.', '1.000'),
            (3, '1', '1.000'),
            (3, '0.9990', '0.999'),
            (3, '0.9991', '1.000'),
            (3, '0.4502', '0.451'),
            (3, '0.4520', '0.452'),
            (3, '0.4500', '0.450'),
            (3, '0.452', '0.452'),
            (3, '0.450', '0.450'),
            (3, '0.000', '0.000'),
            (3, '0.0001', '0.001'),
            (3, '0.45', '0.450'),
            (3, '0.05', '0.050'),
            (3, '0.0001', '0.001'),
            (3, '.0001', '0.001'),
            (3, '0.4', '0.400'),
            (3, '.4', '0.400'),
            (3, '0.', '0.000'),
            (3, '0', '0.000'),

            (2, '11.990', '11.99'),
            (2, '11.991', '12.00'),
            (2, '11.4502', '11.46'),
            (2, '11.450', '11.45'),
            (2, '11.4500', '11.45'),
            (2, '11.452', '11.46'),
            (2, '11.000', '11.00'),
            (2, '11.0001', '11.01'),
            (2, '11.45', '11.45'),
            (2, '11.05', '11.05'),
            (2, '11.4', '11.40'),
            (2, '11.', '11.00'),
            (2, '11', '11.00'),
            (2, '1.990', '1.99'),
            (2, '1.991', '2.00'),
            (2, '1.4502', '1.46'),
            (2, '1.450', '1.45'),
            (2, '1.4500', '1.45'),
            (2, '1.452', '1.46'),
            (2, '1.000', '1.00'),
            (2, '1.0001', '1.01'),
            (2, '1.45', '1.45'),
            (2, '1.05', '1.05'),
            (2, '1.4', '1.40'),
            (2, '1.', '1.00'),
            (2, '1', '1.00'),
            (2, '0.990', '0.99'),
            (2, '0.991', '1.00'),
            (2, '0.4502', '0.46'),
            (2, '0.450', '0.45'),
            (2, '0.4500', '0.45'),
            (2, '0.452', '0.46'),
            (2, '0.000', '0.00'),
            (2, '0.0001', '0.01'),
            (2, '.0001', '0.01'),
            (2, '0.45', '0.45'),
            (2, '0.05', '0.05'),
            (2, '0.4', '0.40'),
            (2, '.4', '0.40'),
            (2, '0.', '0.00'),
            (2, '0', '0.00'),

            (1, '11.90', '11.9'),
            (1, '11.91', '12.0'),
            (1, '11.402', '11.5'),
            (1, '11.40', '11.4'),
            (1, '11.4500', '11.5'),
            (1, '11.0', '11.0'),
            (1, '11.450', '11.5'),
            (1, '11.000', '11.0'),
            (1, '11.0001', '11.1'),
            (1, '11.45', '11.5'),
            (1, '11.05', '11.1'),
            (1, '11.4', '11.4'),
            (1, '11.', '11.0'),
            (1, '11', '11.0'),
            (1, '1.90', '1.9'),
            (1, '1.91', '2.0'),
            (1, '1.402', '1.5'),
            (1, '1.40', '1.4'),
            (1, '1.4500', '1.5'),
            (1, '1.0', '1.0'),
            (1, '1.450', '1.5'),
            (1, '1.000', '1.0'),
            (1, '1.0001', '1.1'),
            (1, '1.45', '1.5'),
            (1, '1.05', '1.1'),
            (1, '1.4', '1.4'),
            (1, '1.', '1.0'),
            (1, '1', '1.0'),
            (1, '0.90', '0.9'),
            (1, '0.91', '1.0'),
            (1, '0.402', '0.5'),
            (1, '0.40', '0.4'),
            (1, '0.4500', '0.5'),
            (1, '0.0', '0.0'),
            (1, '0.450', '0.5'),
            (1, '0.000', '0.0'),
            (1, '0.0001', '0.1'),
            (1, '.0001', '0.1'),
            (1, '0.45', '0.5'),
            (1, '0.05', '0.1'),
            (1, '0.4', '0.4'),
            (1, '.4', '0.4'),
            (1, '0.', '0.0'),
            (1, '0', '0.0'),
            (1, '27.3', '27.3'),
            (1, repr(27.3 - 27), '0.3'),

            (0, '11.90', '12'),
            (0, '11.91', '12'),
            (0, '11.402', '12'),
            (0, '11.40', '12'),
            (0, '11.4500', '12'),
            (0, '11.0', '11'),
            (0, '11.450', '12'),
            (0, '11.000', '11'),
            (0, '11.0001', '12'),
            (0, '11.45', '12'),
            (0, '11.05', '12'),
            (0, '11.4', '12'),
            (0, '11.', '11'),
            (0, '11', '11'),
            (0, '1.90', '2'),
            (0, '1.91', '2'),
            (0, '1.402', '2'),
            (0, '1.40', '2'),
            (0, '1.4500', '2'),
            (0, '1.0', '1'),
            (0, '1.450', '2'),
            (0, '1.000', '1'),
            (0, '1.0001', '2'),
            (0, '1.45', '2'),
            (0, '1.05', '2'),
            (0, '1.4', '2'),
            (0, '1.', '1'),
            (0, '1', '1'),
            (0, '0.90', '1'),
            (0, '0.91', '1'),
            (0, '0.402', '1'),
            (0, '0.40', '1'),
            (0, '0.4500', '1'),
            (0, '0.0', '0'),
            (0, '0.450', '1'),
            (0, '0.000', '0'),
            (0, '0.0001', '1'),
            (0, '.0001', '1'),
            (0, '0.45', '1'),
            (0, '0.05', '1'),
            (0, '0.4', '1'),
            (0, '.4', '1'),
            (0, '0.', '0'),
            (0, '0', '0'),
            ):
            r = round_up_str_num(v,prec)
            if r != x:
                bad.append('%4s %8s %8s %8s %s' % (prec, v,x,r,'yes' if r==x else 'no'))
        self.assertEqual(len(bad),1,"\nnot all round_up_str_num examples worked\n%s" % '\n'.join(bad))

if __name__ == '__main__':
    main()
