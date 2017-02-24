from athlib.wma.agegrader import AgeGrader, AthlonsAgeGrader
from athlib.uka.agegroups import calc_uka_age_group
from athlib.iaaf_score import score as athlon_score
from athlib.iaaf_score import performance as athlon_performance_needed
from athlib.utils import (
    normalize_gender,
    str2num,
    parse_hms,
    get_distance,
    format_seconds_as_time,
    check_performance_for_discipline,
    discipline_sort_key,
    text_discipline_sort_key,
    sort_by_discipline,
)
from athlib.codes import (
    JUMPS, THROWS, MULTI_EVENTS, FIELD_EVENTS,
    FIELD_SORT_ORDER, STANDARD_MALE_TRACK_EVENTS,
    STANDARD_FEMALE_TRACK_EVENTS,
)

ag = AgeGrader()

wma_age_grade = ag.calculate_age_grade
wma_age_factor = ag.calculate_factor
wma_world_best = ag.world_best

aag = AthlonsAgeGrader()
wma_athlon_age_grade = aag.calculate_factor

__all__ = filter(None, """
            athlon_performance_needed
            athlon_score
            calc_uka_age_group
            check_performance_for_discipline
            discipline_sort_key
            format_seconds_as_time
            get_distance
            normalize_gender
            parse_hms
            sort_by_discipline
            str2num
            text_discipline_sort_key
            wma_age_factor
            wma_age_grade
            wma_athlon_age_grade
            wma_world_best
            FIELD_EVENTS
            FIELD_SORT_ORDER
            JUMPS
            MULTI_EVENTS
            STANDARD_FEMALE_TRACK_EVENTS
            STANDARD_MALE_TRACK_EVENTS
            THROWS
            """.split())
