"""Unit tests for iaaf_score.py."""

from unittest import TestCase, main
from athlib.utils import get_distance
from athlib.utils import sort_by_discipline



class UtilsTests(TestCase):
    """Test suite for the IAAF score calculation module."""
    def test_track_sorting(self):
        """Verify that it sorts things into the standard order
        """

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
        ]

        ordered = sort_by_discipline(stuff, attr="e")

        ordered_events = [d["e"] for d in ordered]
        self.assertEquals(
            ordered_events, 
            ['100', '400', '1500', '400H', '3000SC', 'PV', 'TJ', 'HT', '4x100']
            )


    def test_get_distance(self):
        "Extract distance in metres from discipline codes"

        self.assertEquals(get_distance("100"), 100)
        self.assertEquals(get_distance("110mH"), 110)
        self.assertEquals(get_distance("5K"), 5000)
        self.assertEquals(get_distance("MILE"), 1609)
        self.assertEquals(get_distance("5M"), 8045)
        self.assertEquals(get_distance("HM"), 21098)
        self.assertEquals(get_distance("MAR"), 42195)



if __name__ == '__main__':
    main()
