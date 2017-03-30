
Schemas
=======


This contains informal documentation on our schemas.
Our first priority is a schema to exchange results of a meeting, once finished.

See :download:`the Rio 2016 Olympics results <../../sampledata/rio2016/rio_athletics_results.json>` as an example of what we propose.  We will keep this maintained and current.  The rest of this page walks through some of the concepts and choices.

This is derived by a script from an XML format developed informally by Tilastopaja, DeltaTre, Omega and others.  The XML "just grew", with certain fields being overloaded, and is not recommended as a starting point; the 
:download:`XML source file<../../sampledata/rio2016/rio_athletics_results.xml>` is here.

Once the first schema is broadly settled, giving us a vocabulary, we'll move on to tackle
 * competition structure - what events are in a competition, relation of heats and finals, who qualifies and so on
 * exchange of start lists and entries
 * in-competition recording details

Preliminary remarks
-------------------
Our aim is to have a standard which is simple.  It should be possible to prepare results in Excel and convert without too much complexity or nesting; and/or to convert the other way and generate HTML, PDF and Excel from the JSON.



Competitions
------------

Competitions are defined by `name`, there may be a `shortName` and it may be part of a `series`. Useful additonal data includes location, and the timeperiod defined in iso-date format by `startDate` and `endDate`. The absence of an `endDate` signifies a single day event.

.. code-block:: js

  {
    "name": "Rio Olympics 2016",
    "shortName": "OG16",
    "startDate": "2016-08-12",
    "endDate": "2016-08-21", 
    "city": "Rio de Janeiro", 
    "country": "BRA",
    "series": "olympics",
    "events": [ ... ]
  } 


There are variety of fields that help us analyse the results, these may be more relevant for higher level competions. (is this at an event level or competion ?)

:matchReferee: is the individual that has approved the results and the contact to whom querries should be addressed.
:drugTesting: is drug testing present.
:drugTestingBody: who is carying out that testing.

Events
------

Within a competition, there may be a single event or many. We propose thateach is assigned a unique text
ID within the competition.  A simple scheme might be to number the events - e.g. T01, T02, T02 for track
events and F01, F02 for field.

As described in the vocabulary, events should always have an :ref:`eventCode <eventCode>`. The event may be a heat or a final

.. code-block:: js

  {
    "id": "F34",  // 34th field event in the competition
    "eventName": "M45 Javelin",
    "eventCode": "JT",
    "sex": "M",
    "ageGroup": "V45",  
    "roundName": "final"
  }

This is a rich subject.  If one is only interested in the individual performances after a match, not much information is needed. At larger events we obviously have different rounds of competition.  And if our goal is programme planning or understanding the structure, we need to know a lot more about which events feed into which, how many qualify, points for league scoring and more.

:roundName: shows the level of the round and identifies the members of that round with an integer. Typical values could be "heat6","quarter2","semi1", "prelim3" or "final". An empty field signifies a final.
:nextRound: is the round to which the successful athlete progresses. No integers required.
:qualCriteria: details what an athlete has to do to get to the next round, for example the first 2 in each heat + the 2 fastest losers is "2,2".

Other qualifiers help us define some of the more specialised events.
:multiEvent: is a boolean that signifies if the individual event is part of multi event such as a heptathalon. Default = false.
:numberEvents: how many events are in the parent multi-event event, e.g. Decathalon it is 10.
:eventList: the list of event codes that makes up the multi-event.

:relay: is a boolean that signifies the event is a relay. Default = false. ( Please note `multiEvent` AND `relay` = FALSE.)
:numberLegs: the number of athletes in each relay team.

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

This is usually a two-level, nested structure.  At the top level we have information about the race.  Nested within it, there will be a number of distinct `events`.  These will come in different flavours for running events, horizontal jump and throw events, and vertical jump events. At its simplest an array of `results` links the `ids` of the athletes and performances with a ranking.

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

  {"ids":{
    "otAthleteId": "1066-1415-1745-1815",
    "tpAthleteId": "15120"
    }
  }

:category:  this may be used for non-overlapping prize categories, such as "Senior Men", "Women over 40".  It is common to produce a listing of the leaders in each category, or to offer prizes.  Categories are often, but not always, aligned with age groups and genders.
:performance:  the finishing time or best distance, represented in hours/minutes/seconds or metres as text e.g. "35:24"



Higher level competitions, where there is a need to comunicate with the media may also use some of the following:

:usedGivenName:  for example the current preseident of the IAAF was more commonly known as Seb.
:localFamilyNam:  this allows names to be stored in local scripts for publication or results.
:localGivenName:  This allows names to be stored in local scripts.
:ctryOfBirth: if different from the representing country or team.
:placeOfBirth: the city or region that the athlete comes from.
:PB SB: personal and season's bests for the given event.
:height weight: descriptive information for the athlete.



Optional fields for road races

:chipNumber: an optional field for events with chiptiming.
:startWave: the wave that an athletes starts in, used for very large road races.

The `performance` is the final recorded time or distance of the athlete and has an attached `rank`, signifying where that athlete has finished in the competition. For most running events this is sufficent to complete the results. Here we see the bronze medal winning performance from Rio.

::

    {
      "performance": "2:10:05", 
      "recordFlag": "PB", 
      "country": "USA", 
      "ids": {
        "tpAthleteId": "51210"},
      "givenName": "Galen",
      "familyName": "Rupp", 
      "rank": "3"
    }, 



For track and field events there is much more information that can be recorded. For field events the performance is the best distance recorded, but we should try and store the other attempts. Attached to the performance we should display an array of `roundResults` with a set of entries for each round:

:roundResults: the array
:round: the number of the round
:attempt: the distance recorded, numeric or text for `pass` or `false`
:wind: the wind speed for horizontal jumps in m per s, + showing a trailing wind.
:recordFlag: cumulative string that display whether prformance has become a new SB PB event or regional record - Mirko's notation - may not be needed in a standard

Optional fields could include

:distanceFromBoard: for long jump events, modern camera technology can measure how close to the board the take off foot was.
:athleteOrder: is an integer showing the order in which the athletes threw or jumped in the first round.
:time: is the local time when the attempt took place.

::

     {
          "performance": "66.73", 
          "country": "FRA", 
          "athleteOrder": 4,
          "ids": {
            "tpAthleteId": "1014456",
            "givenName": "M\u00e9lina",
            "familyName": "Robert-Michon"
          }, 
          "rank": "2", 
          "roundResults": [
            {
              "round": 1,
              "attempt": "65.52"
            }, 
            {
              "round": 2,
              "attempt": "64.83"
            }, 
            {
              "round": 3,            
              "attempt": "65.08"
            }, 
            {
              "round": 4,           
              "attempt": "X"
            }, 
            {
              "round": 5,            
              "attempt": "66.73"
            }, 
            {
              "round": 6,            
              "attempt": "X"
            }
          ], 
     }, 
 

Vertical jumps 
--------------

These have a slightly different array consisting of

:round: round number of number of different heights attempted.
:attempt: (IAAF uses trial)height attempted
:success: success "O" or failure "X", upto 3 characters. Three successive "X"'s indicate the end of that athlete's competition.

Here we see a Chinese athlete qualifying for the final of the Pole Vualt.
::

        {
          "group": "A 2", 
          "performance": "5.70", 
          "country": "CHN",
          "athleteOrder": "3",
          "ids": {
            "tpAthleteId": "97544"
          }, 
          "rank": "4", 
          "roundresults": [
            {
              "success": "O",
              "attempt": "5.45", 
              "round": 1
            }, 
            {
              "success": "O",
              "attempt": "5.60", 
              "round": 2
            }, 
            {
              "success": "xO",
              "attempt": "5.70", 
              "round": 3
            }
          ], 
          "qualification": "q", 
          "givenName": "Changrui ",
          "familyName": "Xue"
        }, 


Track Races
-----------

Track races clearly do not have multiple attempts but it is useful to store the reaction times of the athletes, any false starts and the lane order.

:reactionTime: time in seconds
:laneNumber: integer showing start lane or start order in longer distance events with more athletes than lanes. 1 is the inside position.
:dqReason: if performance="DQ", then this optional field can give reason why, `false start` or `out of lane` could be examples.

Relay Races
-----------

Relay races are a popular athletic format both on and off the track. They differ from normal events in that multiple athletes take part per team and splits are often recorded. On the track the number of athletes is always 4, road relays can have many more and may have different length legs.
::

        {
          "performance": "4:10:34.89", 
          "country": "CAN",
          "team": "Canadian Road Relay",
          "teamCode": "BeerMoose", 
          "rank": "3", 
          "relayRunners": [
            {
              "legNumber": 1,
              "legLength": "6.410"
              "givenName": "Brendon",
              "familyName": "Bitter",
              "ids": {
                "otAthelteId": "1234-4321-1234"
                },
              "split": "23:59.45"
            },
            {
              "legNumber": 2,
              "legLength": "4.205".............
 
            }
          ], 
          "qualification": "Q"
        }, 


So each team is made of an array of

:relayRunners: each athlete has an id and a 
:split: which is an iso-format time for their leg if possible.
:legLength: is important for road relays, though may be better stored in the race definition section.


Multi-event Competitions
------------------------

Multi-events obviously involve the athletes competing in various events, scoring points from a commonly agreed table as a function of their performance for each one.
Each athlete has a record for each event, showing the performance and points displayed in an array `combinedResults`. It is helpful to link the performance to an event stored elsewhere.

::

        {
          "performance": "8893", 
          "country": "USA", 
          "ids": {
            "tpAthleteId": "75823"
          }, 
          "rank": "1", 
          "combinedResults": [
          {
            "eventNum": "1",
            "eventCode": "100",
            "multiPerformance": "10.46",
            "points": "945",
            "programmeCode": "TR00341"
          },
          {
            "eventNum": "2",......

          }
          ], 
         } 

Meanwhile, elsewhere in the file is the following
::

  {
    "event": "M100 Decathalon",
    "eventCode": "100",
    "sex": "M",
    "roundName": "heat1",
    "multiEvent": "True",
    "programmeCode": "TR00341"
    "results": [
      {
      "performance": "10.46",
      "ids": {
                  "tpAthleteId": "75823"
                }

            }, 

    ]
   }


Team Competitons
----------------

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
:subTeam: an aditional descriptor that allows a club to have multiple teams in an event, e.g. A or B.









