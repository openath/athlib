

from unittest import TestCase, main
from athlib.bulgarian_score import score

class BulgarianUnder16Test(TestCase):

    def test_scores(self):

        tests = [
                ('U16', 'M', '60', 9.46, 35),
                ('U16', 'M', '60', 12.50, 0), # too slow for points
                ('U16', 'M', '60', 6.50, 150), # too slow for points
                # add more here.
                # test bad inputs, null inputs, end ranges
            ]

        for test in tests:
            (ag, gender, event_code, performance, points) = test
            self.assertEqual(
                score(ag, gender, event_code, performance), 
                points
                )


if __name__ == '__main__':
    main()

