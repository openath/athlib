
Codes and Representation
========================

We want to set unambiguous codes for the "things" use to build databases and systems.  This section is about the values which might appear inside our data structures and variables.  It's general if the codes and values can be used in 
 * columns in Excel
 * parameters to URL requests
 * parts of filenames.

For this reason we avoid special characters (avoiding '?', '/', '&lt;', '&gt;'' and '&amp;'). It is also useful if they are not case-sensitive.  There are workarounds for all of these things, but let's just avoid as many as we can.  


Gender Codes
------------

Let's warm up with something simple::

    M = Male
    F = Female

If the 1976 Olympic Decathlon champion decides to make a comeback, we can discuss complicating things then.

Thus, if exchanging athlete data, we might have a JSON document like this::

    {"firstName": "Fred", "lastName": "Bloggs", "gender": "M"}

...and in a spreadsheet, we would have a column with "M" or "F"


Country codes
-------------

Three-letter ISO codes are preferred::

    GBR, FRA, ESP, DEU

Great Britain has some "history" here - competition records going back 100+ years - to make life more complex, so we allow for some "pseudo-countries"::

    ENG, SCO, WAL, NIR

Similarly we might introduce 
It may also be valuable to have placeholder for international entities::

    INT, EUR

Note that the codes used by the IOC, European Athletics, WMA and EMA often have slight historical differences.  <insert wikipedia reference>.  For example, in sports, Germany is often `GER` rather than `DEU`.  We can provide code to do the mappings, but we should stick to the ISO 




Dates
-----

We aim to be guided by <a href="https://en.wikipedia.org/wiki/ISO_8601">ISO 8601</a>

Databases and programming languages have rich ways to store dates, date-times and times, complete with time zone information.  In athletics this can be troublesome, unless you are very careful.  For example, you set up your county championships timetable in some detail in March, then the clocks change, and you find the computer assumed GMT when you entered in, and everyone shows up an hour off; or that you are advertising the wrong start time for an early-autumn cross country race.  (Yes, this has happened!)

There are also many, many ways for beginning programmers to shoot themselves in the foot when working with dates in Javascript.  For example, if you use a Date object to store the (midnight) closing date of a competition, it will do so down to the millisecond, and adapt to the browser's time zone, resulting in people seeing the wrong day.

For these reasons, we prefer to store dates and event times as text::

    "2015-10-17"  - use for dates, the ISO standard.  (Excel will differ)
    "14:35"       - use for the start time of an event, for historic or programme purposes

When describing programmes or sets of results, we also recommend separating the dates and times. 

Full timestamps should be reserved for when they are needed, such as recording the time the gun actually went off (which you might want to use as an index into a video recording)

**Dates in Excel and user interfaces**

Pasting or importing of dates and times from Excel is risky.  Spreadsheets understand dates, but if you go via a clipboard or to CSV/text, there is the risk of muddling days and months.   Within a spreadsheet, dates should be proper dates.

User input is however best done in the format that users are familiar with, even though the date is stored internally in a proper, unambiguous format. Thus UK users would prefer 25/12/2014.  This could be made configurable by taking the date format from their international settings.  System output is also prescribed sometimes e.g. consistency with external sources. In this case the date format should be configurable according to the purpose of the output.  

Performances, time and distance
-------------------------------

In results, we need to record the time or distance.  This is different from recording the start time of an event.  

Times should be passed in a decimalized text format and interpreted as a number of seconds, so we know the precision that was given. If one colon is present, it denotes minutes and seconds; two colons are hours/minutes/seconds.  Ultra runners going beyond 24 hours will have to count in hours, to keep life simple for the rest of us!  Examples::

    9.58
    58.5
    63.5
    1:03.5   - equivalent to 63.5, first digit assumed to be minutes
    2:03     - assumed to be an 800m time of 2 minutes, and not a Marathon, because only one colon
    2:02:57  - the marathon world record, two colons so contains hours
    73:15    - a half marathon time, equivalent to 1:03:15

Distances for jumps and throws can be stored as decimal numbers.

There are some standard suffixes which are commonly used in results and rankings:  10.3i to denote indoors, 10.3w to suggest wind-assisted. We see this as a presentation layer problem; a good database or rankings system would decompose this to have an 'indoor' or 'wind-assisted' flag.


.. _eventCode:

Event Codes
-----------
If we are exporting the data from an online entry system, or the results of a meeting, we want to use common codes, so that the 400m is always represented the same way.

    | *There are only two hard problems in computer science - cache invalidation and naming things*
    | *- Phil Karlton*


Never mind the first one - it's really hard to pick names. Especially, it's hard to pin down the word "Event".  BY popular consensus we are calling these things "event codes".  

If you are looking at a programme, the "U13 Girls High Jump first round, Sat 10:35" is more of an "event", in the sense of "something that happens at a point in time".  We might call the latter 'CompEvent' or 'ProgEvent' (to be discussed)

Our "first stab" is based on the codes from Power of Ten, which appear in the URL search parameters. However, we have introduced some slight changes.  In particular, we don't want the interpretation to depend on the case of a letter.  So 'm' meaning both Metre and Mile is dangerous::


    HJ, PV, LJ, TJ, SP, DT, HT, JT, WT               - field events
    60, 100, 200, 400, 800, 1500, 3000, 5000, 10000  - track (and other distances for junior races)
                                                     - Any raw number is assumed to be a number in metres

    60H, 80H, 100H, 110H, 200H, 300H, 400H           - number + 'H' denotes hurdles
    2000SC, 3000SC                                   - steeplechase
    DEC, HEP, HEPI, PEN, PENWT                       - multi-events.  Case variations acceptable. 
    20KW, 50KW                                       - walks
    4x100, 4x400                                     - track relays.  

For field events, there is usually a default weight for a given age group and gender, but we can indicate a specific weight of implement as follows.  (We followed Power of Ten, who use these for filter parameters in URLs)::

    SP7.26k, SP6K, SP5K, SP4K, SP3K
    DT2K, DT1.75K, DT1.5K, DT1K
    JT800, JT700, JT600, JT500, JT400
    HT7.26K, HT6k, HT5k, HT4k, HT3k
    WT15.88K, WT11.34K, WT9.08K, WT7.26K, WT5.45K

Hurdles have adjustable heights, defined originally in 3 inch increments (but usually described in millimetres).  Usually, this does not need to be given, because it's a standard.  However, for some Masters and younger competitions, hurdles may be lowered.   If it is necesssary to disambuguate, we can use two digits for "feet and inches". This gives much simpler numbers than the metric equivalents.  For example::

    110H36  - 3'6" or 1.067  - normal men's hurdle height
    110H33  - 3'3" or 0.991  - used for some masters' competitions.

*Discuss* - do we use inches, which are simple, or cm/mm because the world is metric?


Some events, such as the <a href="http://www.dailymail.co.uk/news/article-3671604/Couples-test-strength-marriages-2016-World-Wife-Carrying-Championships.html">Finnish Wife-Carrying championships</a>, are harder to standardise so will be left for a future version.

The mile is special and of historic importance.  So, in a programme or set of entries, we suggest to allow::

    MILE  - as it says.

Moving onto road and cross country, we'd like to suggest an open-ended standard: a combination of a rough distance measure and a suffix which shows the units::

    2K, 5k, 10K, 4.5K  - distance in kilometers
    5M, 10M, 2.2M      - distance in miles  (NOT metres!)
    MAR                - marathon
    HM                 - half marathon
    
    5MXC               - any of the above plus "XC" denotes cross country.

It is not necessary to add an XC suffix; this depends on the context.  

As an example, we're taking entries now for a school fundraiser with three races.  We call them "2K", "5K" and "10K" in the database, and will use those codes as field IDs in the web form, or in a spreadsheet summarising the entries.  We don't need to add "XC", because they all are.  They can have more expansive display names like "2K jog-with-the-dog" if desired.

The advantage of this is that one can compute a very rough speed and thus check if the input given is realistic.  For example, if you are taking online entries and your code for the Masters XC race is just "XC", you have no way to know if a predicted or actual time of "30.15" is realistic.  But if you know you are talkin about a 5 mile race, it's pretty clear that 30:15 was intended, and you can either reject or "fix" the input depending on your philosophy.

The `IAAF web site <http://www.iaaf.org/records/toplists/>`_ uses 'slugs' - URL components - such as 'one-mile' and 'high-jump'.  These are certainly useful and could be added to a standard.

The short codes will be OK for results but not for instance in competition programmes.  There it might be better to have standard short descriptions e.g. Shot Put, 100m Hurdles 

Ordering of events
------------------

There is a "natural order" which people expect to see on entry forms, in dropdowns and in statistics.  For a track meeting, it is as follows:

    1. Track events, increasing distance
    2. Hurdles, increasing distance
    3. Steeplechases
    4. Field events:  HJ PV LJ TJ SP DT HT JT
    5. Relays, increasing distance

`athlib` provides sorting functions in Python and Javascript to implement this.

Age Group codes
---------------
When dealing with entries and results, it's common to have a column showing the age groups.

The IAAF has a very simple scheme.  The age group is based on one's age at New Year, with the following groups::

    U14, U16, U18, U20, U23, SEN

UKA has well defined age group codes:  U13, U15, U17, U20, U23 (rarely used), SEN.  The definition depends on the discipline (Road, XC, Track and Field), the date of birth of the athlete and the start date of the competition.  Again we provide code to work this out.

It is very common in results and entries to conflate the age and gender.   Eveen more annoyingly for programmers, in the UK we tend to add an age-dependent suffix - 'B' for Boys, 'G' for girls, 'M' for Men and 'W' for women.  Thus, a county or national programme would list U13B, U15B, U17M, U20M.

Masters go in 5 year bands:  V35, V40, V45 etc.   This is a global standard set by WMA. It is commonly conflated with gender e.g. M45, W50.

Schools are commonly referred to be year in the UK, so we suggest  YEAR1...YEAR11.  (Would YEAR01, YEAR02...YEAR11 be better so they always sort in order?)

Different countries are expected to have different age group coding systems and cutoff rules.  Therefore, a well designed library would have 'namespaced' packages for countries or organising bodies with equivalent, swappable functions::

    from athlib.uka import age_group
    from athlib.wma import age_group


