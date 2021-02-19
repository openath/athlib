def __wma_delay__():
    from .wma.agegrader import AgeGrader, AthlonsAgeGrader
    return AgeGrader, AthlonsAgeGrader
from .uka.agegroups import calc_uka_age_group
from .athlon_score import score as athlon_score
from .hungarian_score import score as hungarian_score
from .athlon_score import performance as athlon_performance_needed

__version__ = u'0.6.4'

from .exceptions import RuleViolation

from .utils import (
    normalize_gender,
    str2num,
    parse_hms,
    get_distance,
    round_up_str_num,
    format_seconds_as_time,
    check_performance_for_discipline,
    discipline_sort_key,
    text_discipline_sort_key,
    sort_by_discipline,
    check_event_code,
    normalize_event_code,
    isStr,
    nativeStr,
    is_hand_timing
    )

from .implements import get_implement_weight, get_specific_event_code

from .codes import (
                    JUMPS,
                    THROWS,
                    MULTI_EVENTS,
                    FIELD_EVENTS,
                    STANDARD_MALE_TRACK_EVENTS,
                    STANDARD_FEMALE_TRACK_EVENTS,
                    FIELD_SORT_ORDER,
                    PAT_THROWS,
                    PAT_JUMPS,
                    PAT_TRACK,
                    PAT_ROAD,
                    PAT_RUN,
                    PAT_FIELD,
                    PAT_RELAYS,
                    PAT_HURDLES,
                    PAT_MULTI,
                    PAT_EVENT_CODE,
                    PAT_LEADING_DIGITS,
                    PAT_LEADING_FLOAT,
                    PAT_VERTICAL_JUMPS,
                    PAT_HORIZONTAL_JUMPS,
                    PAT_LENGTH_EVENT,
                    PAT_TIMED_EVENT,
                    PAT_PERF,
                    PAT_LONG_SECONDS,
                    PAT_NOT_FINISHED,
                    PAT_FINISH_RECORD,
                    )

from .highjump import HighJumpCompetition, Jumper

AgeGrader, AthlonsAgeGrader = __wma_delay__()
del __wma_delay__
ag = AgeGrader()

def wma_age_grade(gender, age, event, performance, verbose=False):
    """Return the age grade score (0 to 100ish) for this result."""
    return ag.calculate_age_grade(gender, age,event, performance, verbose=verbose)

def wma_age_factor(gender, age, event, distance=None):
    """Work out 'slowdown factor' for a geezer of this
    age taking part in this event e.g."""
    return ag.calculate_factor(self, gender, age, event, distance=distance)

def wma_world_best(gender, event):
    "The relevant world-record performance on the date stats were compiled"
    return ag.world_best(gender, event)

aag = AthlonsAgeGrader()
def wma_athlon_age_factor(gender, age, event):
    """Work out 'slowdown factor' for a geezer of this
    age taking part in this event e.g."""
    return aag.calculate_factor(gender, age, event)

def wma_athlon_age_grade(gender, age, event, performance, verbose=False):
    """Return the age grade score (0 to 100ish) for this result."""
    return aag.calculate_age_grade(gender, age, event, performance, verbose=verbose)

from .tyrving_score import tyrving_score
from .qkids_score import qkids_score
from .sportshall_score import sportshall_score

def __make_all__():
    return [k for k, v in sorted(globals().items()) if not (k.startswith('__') or v.__class__.__name__== 'module')]

__all__ = __make_all__()
del __make_all__
