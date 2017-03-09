from datetime import date, timedelta
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from athlib.utils import isStr


def prior_date(match_date, cutoff_month, cutoff_day):
    """
    Count back to relevant date.
    e.g. find the 31st August prior to match date
    """
    y = match_date.year
    m = match_date.month
    d = match_date.day
    x = date(y, cutoff_month, cutoff_day)
    if x > match_date:
        x = date(y - 1, cutoff_month, cutoff_day)
    return x


def rule107_agegroups_trackandfield(birth_date,
                                    match_date,
                                    vets=True,
                                    underage=False):
    august_cutoff = date(match_date.year, 8, 31)
    december_cutoff = date(match_date.year, 12, 31)

    if isStr(birth_date):
        birth_date = parse_date(birth_date)

    age_on_31_aug = relativedelta(august_cutoff, birth_date).years
    age_on_31_dec = relativedelta(december_cutoff, birth_date).years
    age_on_match_day = relativedelta(match_date, birth_date).years

    if underage and age_on_31_aug < 9:
        return "U9"

    if age_on_31_aug < 11:
        return "U11"
    elif age_on_31_aug in [11, 12]:
        return "U13"
    elif age_on_31_aug in [13, 14]:
        return "U15"
    elif age_on_31_aug in [15, 16]:
        return "U17"
    else:
        if age_on_31_dec < 20:
            return "U20"
        else:
            if age_on_match_day < 35:
                return "SEN"
            else:
                # V35, V40, V45 etc
                if vets:
                    return "V%02d" % (int(age_on_match_day // 5) * 5)
                else:
                    return "SEN"


def rule507_agegroups_crosscountry(birth_date,
                                   match_date,
                                   vets=True,
                                   underage=True):
    """I can't find any actual differences between road and XC"""
    if isStr(birth_date):
        birth_date = parse_date(birth_date)

    cutoff_date = prior_date(match_date, 8, 31)
    age_on_31_aug = relativedelta(cutoff_date, birth_date).years
    age_on_match_day = relativedelta(match_date, birth_date).years

    if underage and age_on_match_day < 9:
        return "U9"

    if age_on_match_day < 11:
        return "U11"
    elif age_on_31_aug in [10, 11, 12]:
        return "U13"
    elif age_on_31_aug in [13, 14]:
        return "U15"
    elif age_on_31_aug in [15, 16]:
        return "U17"
    elif age_on_31_aug in [17, 18, 19]:
        return "U20"
    else:
        if age_on_match_day < 35:
            return "SEN"
        else:
            # V35, V40, V45 etc
            if vets:
                return "V%02d" % (int(age_on_match_day // 5) * 5)
            else:
                return "SEN"


def calc_uka_age_group(birth_date,
                       match_date,
                       category,
                       vets=True,
                       underage=False):
    """Return UKA age group"""
    if category == 'TF':
        return rule107_agegroups_trackandfield(birth_date,
                                               match_date,
                                               vets=vets,
                                               underage=underage)
    elif category in ['ROAD', 'XC']:
        return rule507_agegroups_crosscountry(birth_date,
                                              match_date,
                                              vets=vets,
                                              underage=underage)
    elif category == 'ESAA':
        # Apparently the English Schools has its own rule, but we haven't done
        # this yet. If still here, raise an exception
        raise NotImplementedError
    else:
        raise ValueError("category must be one of:  TF, ROAD, XC, ESAA")


rules = """
Age Groups
If you are unsure whether you can compete within a certain age group (U11, U13,
U15, U17, U20 etc) then the following guidelines taken from the UK Athletics
Rules for Competition (Rules 107, 207 and 507) will help determine which age
group is applicable.

RULE 107 Age groups - Track and Field
The Competition Year shall extend from 1st October to 30th September in the
following year.
(i) Under 13 Boys and Girls (School Years 6 and 7)
Track and Field competition for Under 13's shall be confined to competitors who
are aged 11 or 12 on the 31st August within the Competition Year, as defined in
(1) above.
(ii) Under 15 Boys and Girls (School Years 8 and 9)
Track and Field events for Under 15's shall be confined to competitors who are
aged 13 or 14 on 31st August within the Competition Year, as defined in (1)
above.
(iii) Under 17 Men and Women (School Years 10 and 11)
Track and Field events for Under 17's shall be confined to competitors who are
aged 15 or 16 on 31st August within the Competition Year, as defined in (1)
above.
(iv) Under 20 Years Junior Men and Women
Track and Field events for Juniors shall be confined to competitors who are 17
or over on 31st August within the Competition Year, as defined in (1) above,
but Under 20 on 31st December in the calendar year of competition.
(v) Seniors Men & Women
A Senior is a competitor who is at least 20 years of age on 31st December in
the calendar year of competition.
(vi) Masters Men & Women
Events for Masters shall be confined to athletes who are at least 35 years of
age on the day of competition.
Notes:
In addition there are some limitations on the number of events allowed on the
same day and on competing in higher age groups.
UK Athletics Rules do not specifically cater for athletes under the age of 11
years.
This does not necessarily preclude provision by organisers of competitions for
events for athletes younger than 11 years, with correspondingly reduced
distances to be run and lighter implements to be used.

RULE 207 Age groups - Road
The Competition Year extends from 1st September to 31st August in the following
year.
(i) Under 13 Boys and Girls (School Years 7&8 and some year 6)
Road Running competitions for Under 13's shall be confined to competitors who
are age 11 on the day of competition, or 12 on 31st August prior to the
commencement of the Competition Year as defined above.
(ii) Under 15 Boys & Girls (School Years 9 & 10)
Road Running competitions for Under 15's shall be confined to competitors who
are aged 13 or 14 on 31st August prior to the commencement of the Competition
Year as defined above.
(iii) Under 17 Men & Women (School Years 11 & 12)
Road Running competitions for Under 17's shall be confined to competitors who
are 15 or 16 on 31st August prior to the commencement of the Competition Year
as defined above.
(iv) Junior Men & Women
Road Running competitions for Junior Men and Women shall be confined to
competitors who are aged 17, 18 or 19 on 31st August prior to the commencement
of the Competition Year as defined above.
(v) Senior Men & Women
For Road Running competitions a Senior is a competitor who is aged at least 20
years on 31st August prior to the commencement of the Competition Year as
defined above. In Road Relay competitions Junior Men and Women, as appropriate,
may compete in Senior events.
(vi) Masters Men and Women
Road Running events for Masters shall be confined to competitors who are at
least 35 years of age on the date of the competition.
Note:
UK Athletics Rules do not specifically cater for athletes under the age of 11
years.
This does not necessarily preclude provision by organisers of competitions for
events for athletes younger than 11 years, with correspondingly reduced
distances to be run.

RULE 507 Age groups - Cross Country
The Competition Year extends from 1st October to 30th September in the
following year.
(i) Under 13 Boys and Girls (School Years 7 and 8 and some Year 6)
Cross Country competitions for under 13's shall be confined to competitors who
are aged 11 on the day of competition or 12 on 31st August prior to the
commencement of the Competition Year as defined above.
(ii) Under 15 Boys and Girls (School Years 9 and 10)
Cross Country competitions for Under 15's shall be confined to competitors who
are aged 13 or 14 on 31st August prior to the commencement of the Competition
Year as defined above.
(iii) Under 17 Men and Women (School Years 11 and 12)
Cross Country competitions for Under 17's shall be confined to competitors who
are aged 15 or 16 on 31 August prior to the commencement of the Competition
Year as defined above.
(iv) Junior Men and Women
Cross Country competitions for Junior Men and Women shall be confined to
competitors who are aged 17, 18 or 19 on 31st August prior to the commencement
of the Competition Year as defined above.
(v) Senior Men and Women
For Cross Country competitions a Senior is a competitor who is aged at least 20
on 31st August prior to the commencement of the Competition Year as defined
above.
Junior Men and Women may compete in Senior events as appropriate and subject to
the maximum distances for their age group not being exceeded.
(vi) Masters Men and Women
Cross Country events for Masters shall be confined to
competitors who are at least 35 years of age on the date of the competition.
Note:
UK Athletics Rules do not specifically cater for athletes under the age of 11
years.
This does not necessarily preclude provision by organisers of competitions for
events for athletes younger than 11 years, with correspondingly reduced
distances to be run.

Age Groups for English Schools AA competition
The age limits for ESAA Cross Country Championships, Track & Field
Championships, and Combined Events Championships are:
Junior 13 years and under 15 years of age on 31st August at the end of the
current school year
Intermediate 15 years and under 17 years of age on 31st August at the end of
the current school year
Senior 17 years and under 19 years of age on 31st August at the end of the
current school year
The age limits for ESAA Schools Cup competitions are:
Junior 12 years and under 14 years of age on 31st August at the end of the
current school year
Intermediate 14 years and under 16 years of age on 31st August at the end of
the current school year


Notes relating to all competitions
The school year is deemed to run from September to July, so August at the end
of the current school year is the August following the end of the summer term,
irrespective of whether some schools actually start their new year in Augusr.
Although the Combined Events Final is held in September it is considered to be
in the same school year as the previous regional rounds which lead up to the
final, thus age limits are those which apply at the time of the regional round.
Athletes may only compete in the age group corresponding to their age. In
particular this means:
- athletes cannot compete in a higher age group
- athletes who are younger than the Junior age group cannot compete
Age Groups for IAAF and IPC competition
(IAAF Rule 141; IPC Rule 4)
The following age groups are recognised by the IAAF and IPC Athletics:
a) Master Men and Women: Any athlete who has reached his/her 35th birthday
b) Junior Men and Women: Any athlete of 18 or 19 years on 31 December in the
year of the competition;
c) Youth Boys and Girls: Any athlete of 16 or 17 years on 31 December in the
year of the competition;
d) Under 16 Boys and Girls: Any athlete of 14 or 15 years on 31 December in the
year of the competition.
Note: An athlete must be 14 by 31 December in the year of competition to
compete in an open event.
"""
