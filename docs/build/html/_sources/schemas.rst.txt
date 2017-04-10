
Schemas
=======


We'll start documenting the different schemas here.

We could use schemas for
 * fixtures - a list of meetings
 * full meeting results
 * programme and structure of meeting


The basic requirement of data transfer within athletics is to send results in a consistent and compact manner. The basic building block of this data is an `event`. To be useful an event must have some descriptive data and a set of results. 
To analyse results as the simplest level we just need a means of identifying an athlete, their performance and a ranking. In this document we show a json schema to standardise this transfer.


Competitions
------------

Most events are part of a bigger meeting, or `competition`.
Competitions are defined by `name`, there may be a `shortName` and it may be part of a `series`. Useful additonal data includes location, and the timeperiod defined in iso-date format by `startDate` and `endDate`. The absence of an `endDate` signifies a single day format.

.. code-block:: javascript

  {
    "name": "Rio Olympics 2016",
    "organiserId": "IOC",
    "shortName": "OG16",
    "startDate": "2016-08-12",
    "endDate": "2016-08-21", 
    "city": "Rio de Janeiro", 
    "country": "BRA",
    "series": "olympics",
    "events": [ ... ]
  } 


Attached to a competition is an event or more likely multiple `events`.There are variety of fields that help us analyse the results, these may be more relevant for higher level competitions. (is this at an event level or competition ?)

:matchReferee: is the individual that has approved the results and the contact to whom querries should be addressed.
:drugTesting: is drug testing present.
:drugTestingBody: who is carying out that testing.

Events
------

Within a competition, there may be a single event or many. We propose that each is assigned a unique text
ID, or ``programmeCode``, within the competition.  A simple scheme might be to number the events - e.g. T01, T02, T02 for track
events and F01, F02 for field.

As described in the vocabulary, events should always have an ``eventCode``. The event may be a heat or a final as defined by ``roundName``.


::

  {
    "programmeCode": "F34",  # 34th field event in the competition
    "eventName": "M45 Javelin",
    "eventCode": "JT",
    "sex": "M",
    "ageGroups": "V45",  
    "roundName": "final",
    "result": [...... ]
  }


At larger events we obviously have different rounds of competition.  And if our goal is programme planning or understanding the structure, we need to know a lot more about which events feed into which, how many qualify, points for league scoring and more.

:roundName: shows the level of the round and identifies the members of that round with an integer. Typical values could be "heat6","semi2" "prelim3" or "final". An empty field signifies a final.
:round: the broad tier of competition, e.g. PRELIM,HEAT,SEMI or FINAL. The qualification round for field events is called "PRELIM"
:nextRound: is the round to which the successful athlete progresses.
:qualCriteria: details what an athlete has to do to get to the next round, for example the first 2 in each heat + the 2 fastest losers is "2,2".

Other qualifiers help us define some of the more specialised events.

:multiEvent: is a boolean that signifies if the individual event is part of multi event such as a heptathlon. Default = false.
:numberEvents: how many events are in the parent multi-event event, e.g. Decathlon it is 10.



Relays
------
:eventCode: For the classic track relays, 4x100, 4x400 we will use the obvious event codes. Other relays need more detail and we use the label "12xRELAY", for a 12 athlete event over a non-standard distance. The number of athletes in each relay team is specified in the event code, we may want to specify the distance run,

:legLengths: either a single value for equal length relays (e.g 4x1500m) or an array of size equal to number or athletes with the different leg lengths for an Ekiden or a medley relay on the track.

:indoor: is a boolean that shows whether the event is held indoors. Default is false.
:discipline: an either be empty or "track", "xc", "fell" or "road", "track" is the default. This specifies the governing body and the surface upon which the athletes compete.
:programmeCode: is an id for the event.
:prizeCategories: a list of categories, into which the results may have to be split for the awarding of prizes.


The time/date of the event can be specified especially if the competition has a multi-day or multi-session format. Similarly, in multi-location competitions, the location of the event can be given. The absence of this data implies that it is the same as the competition.

:date: the iso-format date of the event
:time: the local time of the event 
:session: the morning, afternoon or evening (as defined in local time) session in which the event appears.
:location: location of the event, e.g. Ern Clark Athletic Centre, Perth.



Results
-------

This is usually the second stage of a  two-level, nested structure.  At the top level we have information about the competition.  

Nested within it, there will be a number of distinct `events`.  The results for each of these will come in different flavours for running events, horizontal jump, throw events, and vertical jump events .

At its simplest an array of `result` links the `ids` of the athletes and performances with a ranking.

The `results` schema should also allow team scores to be held and displayed.  When a team competition takes place, the main thing people want to know is who is winning the match.


To identify the runner  the following fields may be required:

:bib:  text or numeric.  The race number worn by the athlete
:rank:  the runner's finishing position.  numeric.  If two runners place equal, they may both be give e.g. `1`, but the next runner should be given `3`

:givenName:  first name, in Western languages. In Roman script.
:familyName:  surname, in Western languages.
:dateOfBirth: d-o-b in iso-date format.

For example, an athlete can be identified as follows. This also is sufficient information to produce a programme or display results
::

  {
    "givenName": "Andrew",
    "familyName": "Weir",
    "dateOfBirth": "1990-04-01",
    "clubCode": "THH"
  }

Alternatively, if we are transferring between databases it may be simpler to use a preassigned Id from a recognised system or provider.
::
 
    "otAthleteId": "1066-1415-1745-1815",
    "tpAthleteId": "15120"
 
:category:  this may be used for non-overlapping prize categories, such as "Senior Men", "Women over 40".  It is common to produce a listing of the leaders in each category, or to offer prizes.  Categories are often, but not always, aligned with age groups and genders.
:performance:  the finishing time or best distance, represented in hours/minutes/seconds or metres as text e.g. "35:24"



Higher level competitions, where there is a need to communicate with the media may also use some of the following:

:usedGivenName:  for example the current president of the IAAF was more commonly known as Seb.
:localFamilyNam:  this allows names to be stored in local scripts for publication or results.
:localGivenName:  This allows names to be stored in local scripts.
:ctryOfBirth: if different from the representing country or team.
:placeOfBirth: the city or region that the athlete comes from.
:PB SB: personal and season's bests for the given event.
:height weight: descriptive physical information for the athlete.



Optional fields for road races

:chipNumber: an optional field for events with chip-timing.
:startWave: the wave that an athletes starts in, used for very large road races.

The `performance` is the final recorded time or distance of the athlete and has an attached `rank`, signifying where that athlete has finished in the competition. For most running events this is sufficient to complete the results. Here we see the Gold medal winning performance from Rio.

::


       {
          "recordFlag": "SB", 
          "country": "JAM", 
          "reactionTime": "0.155", 
          "familyName": "Bolt", 
          "rank": "1", 
          "performance": "9.81", 
          "tpAthleteId": "45032", 
          "givenName": "Usain"
        }, 
    


For track and field events there is much more information that can be recorded.

Track Races
-----------

Track races clearly do not have multiple attempts but it is useful to store the reaction times of the athletes, any false starts and the lane order.

:reactionTime: time in seconds
:laneNumber: integer showing start lane or start order in longer distance events with more athletes than lanes. 1 is the inside position.
:dqReason: if performance="DQ", then this optional field can give reason why, `false start` or `out of lane` could be examples.
:wind: the wind-speed need only be recorded at the event level as it i the same for all athletes.

Field Events
------------

For field events the `performance` is the best distance recorded, but we should try and store the other attempts or trials. Attached to the performance we should display an array of `attempts` with a set of entries for each round:

:attempts: the array of attempts/trials
:round: the number of the round
:performance: the distance recorded, numeric or text with `P` for a pass and `X` for a foul.
:wind: the wind speed for horizontal jumps in m/sec, a positive number shows a trailing wind, this must be recorded for each attempt in the horizontal jumps.
:recordFlag: list of certain keywords that show if that performance is significant, examples are SB, PB, WL, WR, NR, with the potential for a "=" to signifying equaling a record. This should be shown at bot the `round` and overall `performance` level. Default is no that no records have been broken.

Optional fields could include

:distanceBoard: for horizontal jump events, modern camera technology can measure how close to the board the take off foot was.
:athleteOrder: is an integer showing the order in which the athletes threw or jumped in the first round.
:time: is the local time when the attempt took place.

::

        {
          "recordFlag": "PB", 
          "country": "RSA", 
          "familyName": "Manyonga", 
          "rank": "2", 
          "attempts": [
            {
              "performance": "8.16", 
              "round": 1, 
              "wind": "0.5"
            }, 
            {
              "performance": "X", 
              "round": 2, 
              "wind": "-0.5"
            }, 
            {
              "performance": "X", 
              "round": 3, 
              "wind": "0.3"
            }, 
            {
              "performance": "8.28", 
              "round": 4, 
              "wind": "-0.2"
            }, 
            {
              "performance": "8.37", 
              "recordFlags": [
                "PB"
              ], 
              "round": 5, 
              "wind": "-0.3"
            }, 
            {
              "performance": "X", 
              "round": 6, 
              "wind": "-0.2"
            }
          ], 
          "performance": "8.37", 
          "tpAthleteId": "115821", 
          "givenName": "Luvo", 
          "wind": "-0.3"
        }, 

Vertical jumps 
--------------

These have a slightly different array of `heights`, consisting of

:round: round number of number of different heights attempted.
:height: height attempted
:results: success "O" or failure "X", up to 3 characters. Three successive "X"'s indicate the end of that athlete's competition.
:jumpOff: boolean that indicates whether jump is part of a jump off, default="False".

Here is the bronze medal jump from Rio.
::

         {
          "recordFlag": "SB", 
          "country": "CRO", 
          "familyName": "Vla\u0161i\u0107", 
          "rank": "3", 
          "heights": [
            {
              "height": "1.88", 
              "results": "XO"
            }, 
            {
              "height": "1.93", 
              "results": "XO"
            }, 
            {
              "height": "1.97", 
              "results": "XO"
            }, 
            {
              "height": "2.00", 
              "results": "XXX"
            }
          ], 
          "performance": "1.97", 
          "tpAthleteId": "1002546", 
          "givenName": "Blanka"
        }, 


Relay Races
-----------

Relay races are a popular athletic format both on and off the track. They differ from normal events in that multiple athletes take part per team and splits are often recorded. On the track the number of athletes is almost always 4, road relays can have many more and may have different length legs.

We have to specify both the event and the results differently 
:eventCode: For the classic track relays, 4x100, 4x400 we will use the obvious event codes. Other relays need more detail and we use the 12xrelay, for a 12 athlete event over a non-standard distance. 
The number of athletes in each relay team is specified in the event code, we may want to specify the distance run,

:legLengths: if the event is not a 4x100 or 4x400 we can use either a single value for equal length relays (e.g 4x1500m) or an array of size equal to number or athletes with the different leg lengths for an Ekiden or a medley relay on the track.

Each team, defined by ``teamCode`` has a performance which is the aggregate time and a rank driven off this but also is made of an array of..

:runners: in which each athlete has an id and a 
:split: which is an iso-format time for their leg if possible.
 A classic 4x100m would be as follows::

    {
      "roundName": null, 
      "name": "4 x 100 m Men", 
      "eventCode": "4x100", 
      "result": [
        {
          "tpTeamId": "18760", 
          "country": "JAM", 
          "reactionTime": "0.150", 
          "rank": "1", 
          "performance": "37.27", 
          "teamCode": "JAM", 
          "runners": [
            {
              "tpAthleteId": "4109", 
              "givenName": "Asafa", 
              "legNumber": 1, 
              "familyName": "Powell"
            }, 
            {
              "tpAthleteId": "69837", 
              "givenName": "Yohan", 
              "legNumber": 2, 
              "familyName": "Blake"
            }, 
            {
              "tpAthleteId": "79234", 
              "givenName": "Nickel", 
              "legNumber": 3, 
              "familyName": "Ashmeade"
            }, 
            {
              "tpAthleteId": "45032", 
              "givenName": "Usain", 
              "legNumber": 4, 
              "familyName": "Bolt"
            }
          ], 
          "recordFlags": [
            "WL", 
            "SB"
          ]
        }, 
        {
          "tpTeamId": "22756", 
          "country": "JPN", 
          "reactionTime": "0.144", 
          "rank": "2", 


A slightly lower key road-relay could be as follows, note the `performance` and `rank` each leg refer to the cumulative time. The `split` is optional and is merely the difference between the 2 leg performance times. The `legRank` is the ranking of the split on that leg::

    {
    	eventCode: "12xrelay",
    	eventName: "Southern 12 stage",
    	legLenths:{
    		6.4,4.2,6.4,4.2,6.4,4.2,6.4,4.2,6.4,4.2,6.4,4.2
    	},
    	discipline: "road",
    	result :[
        	{
          	"performance": "4:10:34.89", 
          	"country": "GBR",
          	"team": "Thames Hare and Hounds",
          	"teamCode": "THH", 
          	"rank": "3", 
          	"runners": [
            	{
                  "legNumber": 1,
                  "givenName": "Brendon",
                  "familyName": "Bitter",
                  "otAthelteId": "1234-4321-1234",
                  "split": "23:59",
                  "legRank": "4",
                  "performance": "23:59",
                  "rank": "4"
            	},
            	{
                  "legNumber": 2,
                  "split": "10:00",
                  "legRank": "2",
                  "performance": "33:59".
                  "rank": "3"...
              	},.....
            ],
            "qualification": "Q"
            },.....
        ]
    }

Multi-event Competitions
------------------------

Multi-events obviously involve the athletes competing in various events, scoring points from a commonly agreed table as a function of their performance for each one.
Each athlete has a record for each event, showing the performance and points displayed in an array `results`. It is helpful to link the performance to an event stored elsewhere.

::

    {
      "roundName": null, 
      "name": "Decathlon Men", 
      "eventCode": "DEC", 
      "result": [
        {
          "country": "USA", 
          "familyName": "Eaton", 
          "results": [
            {
              "performance": "10.46", 
              "eventNo": 1, 
              "points": 985, 
              "wind": "-0.1", 
              "eventCode": "100"
            }, 
            {
              "performance": "7.94", 
              "eventNo": 2, 
              "points": 1045, 
              "wind": "1.7", 
              "eventCode": "LJ"
            }, 
            {
              "performance": "14.73", 
              "eventNo": 3, 
              "points": 773, 
              "eventCode": "SP"
            }, 
            {
              "performance": "2.01", 
              "eventNo": 4, 
              "points": 813, 
              "eventCode": "HJ"
            }, 
            {
              "performance": "46.07", 
              "eventNo": 5, 
              "points": 1005, 
              "eventCode": "400"
            }, 
            {
              "performance": "13.80", 
              "eventNo": 6, 
              "points": 1000, 
              "wind": "0.7", 
              "eventCode": "110H"
            }, 
            {
              "performance": "45.49", 
              "eventNo": 7, 
              "points": 777, 
              "eventCode": "DT"
            }, 
            {
              "performance": "5.20", 
              "eventNo": 8, 
              "points": 972, 
              "eventCode": "PV"
            }, 
            {
              "performance": "59.77", 
              "eventNo": 9, 
              "points": 734, 
              "eventCode": "JT"
            }, 
            {
              "performance": "4:23.33", 
              "eventNo": 10, 
              "points": 789, 
              "eventCode": "1500"
            }
          ], 
          "rank": "1", 
          "performance": "8893", 
          "tpAthleteId": "75823", 
          "givenName": "Ashton", 
          "recordFlags": [
            "WL", 
            "SB"
          ]
        }, 

Meanwhile, elsewhere in the file is the following
::

    {
      "roundName": "Heat 4", 
      "name": "100 m Men", 
      "eventCode": "100", 
      "multiEvent": "True",
      "result": [
        {
          "country": "CAN", 
          "reactionTime": "0.138", 
          "familyName": "Warner", 
          "rank": "1", 
          "performance": "10.30", 
          "tpAthleteId": "94840", 
          "givenName": "Damian"
        }, 
        {
          "country": "USA", 
          "reactionTime": "0.147", 
          "familyName": "Eaton", 
          "rank": "2", 
          "performance": "10.46", 
          "tpAthleteId": "75823", 
          "givenName": "Ashton"
        }, ....


  

Team Competitions
-----------------

For team competitions, we have some different concepts.

:points:  if scoring, the number of points earned by the runner.
:country: the country that the athlete is representing.
:clubName: the athletics club the athlete is representing or typically represents as first claim if an international fixture.
:clubCode: we will allow clubs to chose a shorter codified version of their club name, e.g. `THH`. This will typically used in the presentation of results.

:teamName: the points earned will be allocated to a team. This could be the country or local club.
:teamCode: the iso code for the country or the `clubCode`.


Some optional fields that help define team competitions:

:secondClaim: boolean that shows if an athlete is competing for a club other than their main one. Default = false.
:nonScorer: another boolean that shows if an athlete is to be excluded from team scoring. Default = false.
:subTeam: an additional descriptor that allows a club to have multiple teams in an event, e.g. A or B.



Time stamping data
==================

Results can change through time, athletes' performances may be mis-measured or at the more senior level athletes may be retrospectively banned. It is important that the original data is not lost, it is also vital that rankings are updated. To this end, we propose a form of time stamping. The event dates are known, we should add to this when the data was last modified,

:lastModified: iso date string, showing last modification date, default=eventEndDate. This should be clearly displayed at the competition level.

In the events where there have been changes, each athlete should have the ``originalRank`` and ``originalPerf`` stored as well as having ``rank`` and ``performance`` updated. Here we have a rounding adjustment to some electronic timing.

::

       {
          "country": "CAN", 
          "reactionTime": "0.138", 
          "familyName": "Warner", 
          "rank": "1",
          "originalRank": "1" 
          "performance": "10.29",
          "originalPerf": "10.30", 
          "tpAthleteId": "94840", 
          "givenName": "Damian"







