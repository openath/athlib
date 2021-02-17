

from unittest import TestCase, main
from athlib.hungarian_score import get_lookup_table, score

class HunTest(TestCase):

    def test_table_lookup(self):
        """Just verify we pasted the right factors, some sources are rounded off"""

        tbl = get_lookup_table()
        inputs = ('M', 'OUT', '200')
        values = tbl[inputs]
        self.assertEquals(values, (5.08, -35.5, 0))


    def test_scores(self):

        tests = [
                ('M', 'OUT', '100', 9.46, 1400),
                ('M', 'OUT', 'MILE', 240, 1074),
                ('F', 'OUT', 'LJ', 7.50, 1329) 
            ]

        for test in tests:
            (gender, inout, event_code, performance, points) = test
            self.assertEquals(
                score(gender, inout, event_code, performance), 
                points
                )


if __name__ == '__main__':
    main()

