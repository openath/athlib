Python library
==============

The athlib package requires a python >= 3.8.0; attempt to install in lesser pythons will/may result in error messages.

Note that all functions are available in the top
level `athlib` package, even though they may be defined
in submodules.


.. automodule:: athlib
    :members: normalize_gender, str2num, parse_hms, get_distance,
        round_up_str_num, format_seconds_as_time, check_event_code,
        check_performance_for_discipline, discipline_sort_key,
        text_discipline_sort_key, sort_by_discipline, 
        normalize_event_code,
        athlon_score, athlon_performance_needed,
        hungarian_score,
        wma_age_grade, wma_age_factor, wma_world_best, 
        wma_athlon_age_grade, wma_athlon_age_factor, tyrving_score,
        calc_uka_age_group,
        get_implement_weight,
        RuleViolation,
        HighJumpCompetition, Jumper, isStr, nativeStr,
        is_hand_timing, qkids_score, sportshall_score


Codes
-----

.. autoattribute:: athlib.codes.JUMPS
.. autoattribute:: athlib.codes.THROWS
.. autoattribute:: athlib.codes.MULTI_EVENTS
.. autoattribute:: athlib.codes.FIELD_EVENTS
.. autoattribute:: athlib.codes.FIELD_SORT_ORDER
.. autoattribute:: athlib.codes.STANDARD_MALE_TRACK_EVENTS
.. autoattribute:: athlib.codes.STANDARD_FEMALE_TRACK_EVENTS
.. autoattribute:: athlib.codes.PAT_EVENT_CODE
.. autoattribute:: athlib.codes.PAT_FIELD
.. autoattribute:: athlib.codes.PAT_FINISH_RECORD
.. autoattribute:: athlib.codes.PAT_HORIZONTAL_JUMPS
.. autoattribute:: athlib.codes.PAT_HURDLES
.. autoattribute:: athlib.codes.PAT_JUMPS
.. autoattribute:: athlib.codes.PAT_LEADING_DIGITS
.. autoattribute:: athlib.codes.PAT_LEADING_FLOAT
.. autoattribute:: athlib.codes.PAT_LENGTH_EVENT
.. autoattribute:: athlib.codes.PAT_LONG_SECONDS
.. autoattribute:: athlib.codes.PAT_MULTI
.. autoattribute:: athlib.codes.PAT_NOT_FINISHED
.. autoattribute:: athlib.codes.PAT_PERF
.. autoattribute:: athlib.codes.PAT_RELAYS
.. autoattribute:: athlib.codes.PAT_ROAD
.. autoattribute:: athlib.codes.PAT_RUN
.. autoattribute:: athlib.codes.PAT_THROWS
.. autoattribute:: athlib.codes.PAT_TIMED_EVENT
.. autoattribute:: athlib.codes.PAT_TRACK
.. autoattribute:: athlib.codes.PAT_VERTICAL_JUMPS
.. autoattribute:: athlib.codes.AgeGrader
.. autoattribute:: athlib.codes.AthlonsAgeGrader
.. autoattribute:: athlib.codes.aag
.. autoattribute:: athlib.codes.ag
.. autoattribute:: athlib.codes.get_specific_event_code
