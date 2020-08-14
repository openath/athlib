"""
This file contains definitions and utility functions for determining IAAF event
scores.   Taken from IAUM site, 
"""
import math

from .codes import PAT_JUMPS, PAT_THROWS
from .wma.agegrader import AthlonsAgeGrader
from .implements import get_specific_event_code

from typing import Union, Optional

# Array of parameters used to determine IAAF scores.
#
# For track events: A * (Z - <seconds>)^X
# For jumps events: A * (<centimetres> - Z)^X
# For throws events: A * (<metres> - Z)^X
#
# All scores are rounded down.
_scoring_table = (
    {"gender": "M", "event_code": "60", "A": 58.015, "Z": 11.5, "X": 1.81},
    {"gender": "M", "event_code": "100", "A": 25.4347, "Z": 18.0, "X": 1.81},
    {"gender": "M", "event_code": "200", "A": 5.8425, "Z": 38.0, "X": 1.81},
    {"gender": "M", "event_code": "400", "A": 1.53775, "Z": 82.0, "X": 1.81},
    {"gender": "M", "event_code": "600", "A": 0.42088, "Z": 94.5, "X": 1.85},  # Welsh Athletics



    {"gender": "M", "event_code": "800", "A": 0.13279, "Z": 235.0, "X": 1.85},
#     English Schools uses this different factor: a:0.232, Z:200, x:1.85
#    {"gender": "M", "event_code": "800", "A": 0.13279, "Z": 235.0, "X": 1.85},
#   We override this at runtime in the calculator function, if you pass in the esaa option


    # 1000m from Peter Kennedy's calculator
    {"gender": "M", "event_code": "1000", "A": 0.08713, "Z": 305.5, "X": 1.85},

    {"gender": "M", "event_code": "1500", "A": 0.03768, "Z": 480.0, "X": 1.85},
    {"gender": "M", "event_code": "3000", "A": 0.0105, "Z": 1005.0, "X": 1.85},
    {"gender": "M", "event_code": "5000", "A": 0.00419, "Z": 1680.0, "X": 1.85},
    {"gender": "M", "event_code": "10000", "A": 0.000415, "Z": 4245.0, "X": 1.9},

    {"gender": "M", "event_code": "60H", "A": 20.5173, "Z": 15.5, "X": 1.92},
    {"gender": "M", "event_code": "110H", "A": 5.74352, "Z": 28.5, "X": 1.92},
    {"gender": "M", "event_code": "200H", "A": 3.495, "Z": 45.5, "X": 1.81},
    {"gender": "M", "event_code": "400H", "A": 1.1466, "Z": 92.0, "X": 1.81},
    {"gender": "M", "event_code": "3000SC", "A": 0.00511, "Z": 1155, "X": 1.9},
    {"gender": "M", "event_code": "LJ", "A": 0.14354, "Z": 220.0, "X": 1.4},
    {"gender": "M", "event_code": "TJ", "A": 0.06533, "Z": 640.0, "X": 1.4},
    {"gender": "M", "event_code": "HJ", "A": 0.8465, "Z": 75.0, "X": 1.42},
    {"gender": "M", "event_code": "PV", "A": 0.2797, "Z": 100.0, "X": 1.35},
    {"gender": "M", "event_code": "SP", "A": 51.39, "Z": 1.5, "X": 1.05},
    {"gender": "M", "event_code": "HT", "A": 13.0449, "Z": 7.0, "X": 1.05},
    {"gender": "M", "event_code": "DT", "A": 12.91, "Z": 4.0, "X": 1.1},
    {"gender": "M", "event_code": "JT", "A": 10.14, "Z": 7.0, "X": 1.08},
    {"gender": "M", "event_code": "WT", "A": 47.8338, "Z": 1.5, "X": 1.05},



    {"gender": "F", "event_code": "100", "A": 17.857, "Z": 21.0, "X": 1.81},
    {"gender": "F", "event_code": "200", "A": 4.99087, "Z": 42.5, "X": 1.81},
    {"gender": "F", "event_code": "400", "A": 1.34285, "Z": 91.7, "X": 1.81},
    {"gender": "F", "event_code": "800", "A": 0.11193, "Z": 254.0, "X": 1.88},
    {"gender": "F", "event_code": "1500", "A": 0.02883, "Z": 535.0, "X": 1.88},
    {"gender": "F", "event_code": "3000", "A": 0.00683, "Z": 1150.0, "X": 1.88},
    {"gender": "F", "event_code": "5000", "A": 0.00272, "Z": 1920.0, "X": 1.88},
    {"gender": "F", "event_code": "10000","A": 0.000369,"Z": 4920.0, "X": 1.88},
    {"gender": "F", "event_code": "100H", "A": 9.23076, "Z": 26.7, "X": 1.835},
    {"gender": "F", "event_code": "200H", "A": 2.975, "Z": 52.0, "X": 1.81},
    {"gender": "F", "event_code": "400H", "A": 0.99674, "Z": 103.0, "X": 1.81},
    {"gender": "F", "event_code": "3000SC", "A": 0.00408, "Z": 1320.0, "X": 1.9},
    {"gender": "F", "event_code": "LJ", "A": 0.188807, "Z": 210.0, "X": 1.41},
    {"gender": "F", "event_code": "TJ", "A": 0.08559, "Z": 600.0, "X": 1.41},
    {"gender": "F", "event_code": "HJ", "A": 1.84523, "Z": 75.0, "X": 1.348},
    {"gender": "F", "event_code": "PV", "A": 0.44125, "Z": 100.0, "X": 1.35},
    {"gender": "F", "event_code": "SP", "A": 56.0211, "Z": 1.5, "X": 1.05},
    {"gender": "F", "event_code": "HT", "A": 17.5458, "Z": 6.0, "X": 1.05},
    {"gender": "F", "event_code": "DT", "A": 12.331, "Z": 3.0, "X": 1.1},
    {"gender": "F", "event_code": "JT", "A": 15.9803, "Z": 3.8, "X": 1.04},
    {"gender": "F", "event_code": "60", "A": 46.0849, "Z": 13.0, "X": 1.81},
    {"gender": "F", "event_code": "60H", "A": 20.0479, "Z": 17.0, "X": 1.835},
    {"gender": "F", "event_code": "WT", "A": 52.1403, "Z": 1.5, "X": 1.05}
)


def scoring_key(gender: str, event_code: str) -> str:
    """Utility function to get the <gender>-<event> scoring key."""
    return ("%s-%s" % (gender, event_code)).upper()


# Lazily evaluated dictionary to map from scoring key to parameters
_scoring_objects = None


def _scoring_objects_create() -> None:
    """Function to handle lazy evaluation of _scoring_objects, which maps from
    scoring key to parameters.
    """
    global _scoring_objects

    if _scoring_objects is None:
        _scoring_objects = {}

        for o in _scoring_table:
            _scoring_objects[scoring_key(o["gender"], o["event_code"])] = o


# lazy global age_grader object
_age_grader = None

def _get_age_grader() -> AthlonsAgeGrader:
    global _age_grader
    if not _age_grader:
        _age_grader = AthlonsAgeGrader()
    return _age_grader

def score(gender: str, event_code: str, value: Union[float, int], age: str = None, esaa: bool = False) -> Optional[int]:
    """Function to determine IAAF score, based on gender, event and performance.
    
    You should only pass the age if you wish to age-adjust in years for WMA events

    ESAA option overrides the factor for boys 800m, which differs historically;
    English Schools AA and the ultra-multi folks invented different factors.

    In the interface, we assume performance is <seconds> for track events,
    and <metres> for throws and jumps. Ihe the Wikipedia-sourced factors,
    jumps are <centimetres>.  Therefore there is a factor of 100 applied at the
    end.
    """
    # Create _scoring_objects (lazily evaluated)
    global _scoring_objects
    _scoring_objects_create()


    ag = _get_age_grader()
    if not age:
        age_factor = 1.00
    else:
        age_group = 'V%d' % age
        specific_event_code = get_specific_event_code(event_code, gender, age_group)
        age_factor = ag.calculate_factor(gender, age, specific_event_code)




    # Drop out if no coefficients defined (e.g. bad event/gender)
    key = scoring_key(gender, event_code)
    if key not in _scoring_objects:
        return None

    coeffs = _scoring_objects[key]

    if (key == "M-800") and esaa:
        coeffs = {
            "gender": "M", 
            "event_code": "800", 
            "A": 0.232, "Z": 200.0, 
            "X": 1.85
        }





    # Handle based on whether jumps, throws or track event
    if PAT_JUMPS.match(event_code):
        # The table is expressed in centimetres in the original source
        value = 0.01 * (math.floor(100* value * age_factor))

        value = value * 100
        if value > coeffs["Z"]:
            points = max(0, int(coeffs["A"] * ((value - coeffs["Z"]) **
                       coeffs["X"])))
        else:
            points =  0
    elif PAT_THROWS.match(event_code):
        value = 0.01 * (math.floor(100* value * age_factor))
        if value > coeffs["Z"]:
            points =  max(0, int(coeffs["A"] * ((value - coeffs["Z"]) **
                       coeffs["X"])))
        else:
            points = 0
    else:
        value = 0.01 * (math.ceil(100* value * age_factor))
        if coeffs["Z"] > value:
            points = max(0, int(coeffs["A"] * ((coeffs["Z"] - value) **
                       coeffs["X"])))
        else:
            points = 0

    
    return points



def unit_name(event_code: str) -> str:
    """Utility function to get the unit name based on event type."""
    if PAT_JUMPS.match(event_code):
        # Used to be cm, but we standardised
        return "metres"
    elif PAT_THROWS.match(event_code):
        return "metres"
    else:
        return "seconds"


def performance(gender: str, event_code: str, score: int) -> Optional[Union[float, int]]:
    """Function to determine performance required to achieve IAAF score, given
    gender and event.

    In the interface, we assume performance is <seconds> for track events,
    and <metres> for throws and jumps. Ihe the Wikipedia-sourced factors,
    jumps are <centimetres>.  Therefore there is a factor of 100 applied at the
    end.
    """
    # Create _scoring_objects (lazily evaluated)
    global _scoring_objects
    _scoring_objects_create()

    if score < 0:
        score = 0

    key = scoring_key(gender, event_code)

    # Drop out if no coefficients defined (e.g. bad event/gender)
    if key not in _scoring_objects:
        return None

    coeffs = _scoring_objects[key]

    if PAT_JUMPS.match(event_code):
        perf = int(math.ceil(((score / coeffs["A"]) **
                             (1.0 / coeffs["X"])) + coeffs["Z"]))
    elif PAT_THROWS.match(event_code):
        perf = (math.ceil(100.0 * (((score / coeffs["A"]) **
                                   (1.0 / coeffs["X"])) + coeffs["Z"])) /
                100.0)
    else:
        perf = (math.floor(100.0 * (coeffs["Z"] - ((score / coeffs["A"]) **
                                                   (1.0 / coeffs["X"])))) /
                100.0)

    if PAT_JUMPS.match(event_code):
        perf = 0.01 * perf

    return perf
