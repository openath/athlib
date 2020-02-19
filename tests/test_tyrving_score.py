
"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main
from athlib import tyrving_score


class TyrvingScoreTests(TestCase):
    """Test suite for the IAAF score calculation module."""

    def test_performance(self):
        """
        test returned points
        """
        for gender, age, event, performance, expected in [
                ('M', 12, '1500', '4:32', 1154),
                ('M', 12, '1000W', '280.3', 1137),
                ('M', 12, '200H68.0cm18.29m', '30.5', 1138),
                ('M', 12, 'PV', '2.5', 965),
                ('M', 12, 'SP3Kg', '5', 379),
                ('M', 12, 'SP3Kg', '10', 922),
                ('M', 12, 'SP3Kg', '16', 1141),
                ('M', 12, 'HJ', '1.5', 1000),
                ('M', 12, 'HJ', '1.6', 1070),
                ('M', 14, 'HJ', '1.5', 846),
                ('M', 14, 'SHJ', '1.6', 1195),
                ('F', 15, '100', '12.5', 1064),
                ('F', 15, '1000W', '300', 825),
                ('F', 15, '200h76.2cm19m', '30', 1050),
                ('F', 15, '1500SC', 311.8, 1083),
                ('F', 15, 'JT500', 30, 790),
                ]:
            self.assertEqual(tyrving_score(gender, age, event, performance), expected,
                    "tyrving_score(%r, %r, %r, %r) returned %r not the expected %r" %(
                        gender, age, event, performance,
                        tyrving_score(gender, age, event, performance), expected,
                        ))

if __name__ == '__main__':
    main()
