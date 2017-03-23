
Schemas
=======


We'll start documenting the different schemas here.

We could use schemas for
 * fixtures - a list of meetings
 * full meeting results
 * programme and structure of meeting



At the moment, we're just fiddling around with reStructuredText to find a way to lay out attributes with minimal typing. Tables are a pain to type.  What follows is an example.

Competitions
------------

Competitions are defined by `name`, there may be a `shortName` and it may be part of a `series`. Useful additonal data includes location, and the timeperiod defined in iso-date format by `startDate` and `endDate`.

| {
|  	"competition": "Rio Olympics 2016",
|	"shortName": "OG16"
|  	"startDate": "2016-08-12",
|  	"endDate": "2016-08-21", 
|  	"city": "Rio de Janeiro", 
|  	"country": "BRA",
|	"series": "olympics"
| }


There are variety of fields that help us analyse the results, these may be more relevant for higher level competions. (is this at an event level or competion ?)

:matchReferee: is the individual that has approved the results and the contact to whom querries should be addressed.
:drugTesting: is drug testing present.
:drugTestingBody: who is carying out that testing.

Events
------

Within a competiton, there may be a single event or many. As described in the vocaulary, events are defined in terms of an `eventCode`, which specifies the form of athletic competion from a pre-defined list, e.g JT for Javelin throw. The event may be a heat or a final,


| {
|	"event": "M45 Javelin",
|	"eventCode": "JT",
|	"sex": "M",
|	"ageGroup": "V45",    -  how do we classify ageGroups?
|	"roundName": "final"
| }

At larger events we obviously have different rounds of competition. 

:roundName: shows the level of the round and identifies the members of that round with an integer. Typical values could be "heat6","quarter2","semi1", "prelim3" or "final". An empty field signifies a final.
:nextRound: is the round to which the successful athlete progresses. No integers required.
:qualCriteria: details what an athlete has to do to get to the next round, for example the first 2 in each heat + the 2 fastest losers is "2,2".
:multiEvent: is a boolean that signifies if the event is part of multi event such as a heptathalon. Default = false.
:relay: is a boolean that signifies the event is a relay. Default = false. ( Please note `multiEvent` AND `relay` = FALSE.)
:indoor: is a boolean that shows whether the event is held indoors. Default is false.
:programmeCode: is an id for the event.
:prizeCategories: a list of categories, into which the results may have to be split for the awarding of prizes.

The time/date of the event can be specified especially if the competion has a multi-day or multi-session format. Similarly, in multi-location competitions, the location of the event can be given. The absence of this data implies that it is the same as the competition.

:date: the iso-format date of the event
:time: the local time of the event 
:session: the morning, afternoon or evening (as defined in local time) session in which the event appears.
:location: location of the event, e.g. Ern Clark Athletic Centre, Perth.



Results
-------

This is usually a two-level, nested structure.  At the top level we have information about the race.  Nested within it, there will be a number of distinct `events`.  These will come in different flavours for running events, horizontal jump and throw events, and vertical jump events.

The `results` schema should also allow team scores to be held and displayed.  When a team competition takes place, the main thing people want to know is who is winning the match.


List of runners.

The following fields are required:

:bib:  text or numeric.  The race number worn by the athlete
:rank:	the runner's finishing position.  numeric.  If two runners place equal, they may both be give e.g. `1`, but the next runner should be given `3`

:givenName:  first name, in Western languages. In Roman script.
:familyName:  surname, in Western languages.
:dateOfBirth: d-o-b
:category:  this may be used for non-overlapping prize categories, such as "Senior Men", "Women over 40".  It is common to produce a listing of the leaders in each category, or to offer prizes.  Categories are often, but not always, aligned with age groups and genders.
:eventPerformance:  the finishing time or best distance, represented in hours/minutes/seconds or metres as text e.g. "35:24"
( or do we want `performance` and `attempt` vs `eventPerfrmance` and `performance`)

For team competitions, we have some different concepts.

:points:  if scoring, the number of points earned by the runner.
:ctry: the country that the athlete is representing.
:clubName: the athletics club the athlete is representing or typically represents as first claim if an international fixture.
:clubCode: we will allow clubs to chose a shorter codified version of their club name, e.g. `THH`. This will typically used in the presentation of results.

:teamName: the points earned will be allocated to a team. This could be the country or local club.
:teamCode: the iso code for the country or the `clubCode`.


Some optional fields that help define team competitions:

:secondClaim: boolean that shows if an athlete is competing for a club other than their main one.
:nonScorer: another boolean that shows if an athlete is to be excluded from team scoring.
:subTeam: an aditional descriptor that allows a club to have multiple teams in an event, e.g. A or B.



Higher level competitions, where there is a need to comunicate with the media may also use some of the following:

:usedGivenName:  for example the current preseident of the IAAF was more commonly known as Seb.
:localFamilyNam:  this allows names to be stored in local scripts for publication or results.
:localGivenName:  This allows names to be stored in local scripts.
:ctryOfBirth: if different from the representing country or team.
:placeOfBirth: the city or region that the athlete comes from.
:PB SB: personal and season's bests for the given event.
:height weight: descriptive information for the athlete.


How to identify an athlete. National federation ID's should be unique and can hopefully be checked with a combination of name, d-o-b and club. Other systems can assign their ID's, which may have to be exchanged.

:nationalID: the Id given by the national federation.
:nationalFed: an ISO code for the athletics Federation. (UK vs Scotland?)


Optional fields for road races

:chipNumber: an optional field for events with chiptiming.
:startWave: the wave that an athletes starts in, used for very large road races.

The `performance` is the final recorded time or distance of the athlete. For track and field events there is much more information that can be recorded. For field events the performance is the best distance recorded, but we should try and store the other attempts. Attached to the bestPerformance we should display an array with a set of entries for each round:


:round: the number of the round
:performance: the distance recorded, numeric or text for `pass` or `false`
:wind: the wind speed for horizontal jumps in m per s, + showing a trailing wind.
:recordFlag: cumulative string that display whether prformance has become a new SB PB event or regional record - Mirko's notation - may not be needed in a standard


Vertical jumps have a slightly different array consisting of


:jumpHeight: height attempted
:performance: success "O" or failure "X", upto 3 characters. Three successive "X"'s indicate the end of that athlete's competition.
:recordFlag: cumulative string that display whether prformance has become a new SB PB event or regional record - Mirko's notation - may not be needed in a standard

or do we want a longer array with one entry per jump rather than per height attempted. Might make describing a medal jump off easier as the heights can go up and down.












