from athlib.wma.agegrader import AgeGrader, AthlonsAgeGrader

ag = AgeGrader()

wma_age_grade = ag.calculate_age_grade
wma_age_factor = ag.calculate_factor
wma_world_best = ag.world_best

aag =AthlonsAgeGrader()
wma_athlon_age_grade = aag.calculate_factor

from athlib.iaaf_score import score as athlon_score
from athlib.iaaf_score import performance as athlon_performance_needed