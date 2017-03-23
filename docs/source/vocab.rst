
Vocabulary
==========

The first step towards a standard is a `vocabulary`.  The World Wide Web Consortium (W3C)
have tools for defining these, but we're making a start in plain English, explaining
the words we have chosen.  These will turn up as the names of records, tags and database
tables.

It is important to try to choose unambiguous names.   Words like `event` and `meeting` can be used in too many contexts.  Below is our first attempt, with some notes on other alteratives we considered.



The main *Things* in Athletics
------------------------------

:Competition:  We prefer this term over `meeting` (used in many contexts) or `match` (which implies a team-against-team contest)

:Venue:  where a competition happens.  Venues may be identified in databases, pinpointed by latitude and longitude, and described in different ways, but they are often re-used and so worth identifying.  Venues might include `tracks`, and `courses` used for cross country or road.

:Organisation:  Organisations include Clubs, National Governing Bodies or Federations, International Federations, Regional bodies, Leagues and more.   Organisations can `affiliate` to each other.  This is often recognised by the payment of a fee.  Schools and Universities can also be supported, if they compete actively and regularly.

:Person:  We'll need to refer to people in their many roles:  athletes, coaches, officials, parents, managers and more.

Contexts
--------
There are quite a few  `contexts` where we may wish to exchange information.  The `context` is about the `task we are trying to address`.  We'll have an attempt at naming some of the main ones below.   When we discuss or specify some file format for exchange, the context determines what information is important and needs to be included.

:results: exchange of results, AFTER a competition is finished, when the results are at least broadly realistic and complete.

:recording: what happens DURING a competition - exchange of finish line data, field event measurements. These differ from results in that they have not been certified by the competition referee.

:entries: start lists and data on who entered what, prior to a competition starting.  This may also include exchange of personal data (e.g. email, next of kin contact numbers) and payment information between athlete or team and the organiser, which is not necessarily open to the world.

:membership:  clubs and governing bodies exchanging data to identify athletes, outside of any particular competition.  This will include data to identify the individual, and to describe their membership status in various organisations.

:statistics: exchange of rankings lists, and the performances of individuals: who, when, what event, how fast/high/long?   

:records:  as a subset of `statistics`,  we also often need to exchange "record holders", at many levels:  school, club, county or region, national, area (e.g. Europe), world.  When publishing a programme for a competition, it's common to know what the record is for that meeting.

:fixtures:  exchange of basic information about planned future competitions:  what are they, when and where are they happening?

:programme: the detailed structure of a competition, including (if it's known yet) what's on when during the competition.   The `programme` context relates to setting up the competition, and production of programmes and timetables and other materials

Useful terms
------------

:eventCode: we propose a standard system of codes, covering each standard event in Athletics, as well as an open-ended system to cover races of different lengths.  Examples might include `HJ`, `800` etc.  The coding system gets its own page [here].

We attempted to call this `discipline`, because of the many ways `event` is used, but have been informed very plainly by many leading statisticians and systems builders that this will never be accepted.

:discipline:  we're using this term to refer to the major subdivisions of the sport, using common codes which make sense in English:  ROAD, XC, TF (track and field), WALK, and MTN (mountain or fell running).

:event: we use this to refer to something that takes place within a competition.  If a group of people line up to run, jump or throw at the same time, we choose to call this an `event`.   During a county championships, we might have an 800m race in many age groups for men and women.  Each would be a distinct event, but they would all share an ``eventCode`` of ``800`` 

:ageGroups: `Events` are frequenty broken down into `agegroups` both at the Junior level and the Masters level to enable more even competion. Different countries and even disciplices within a given country have different rules for defining agegroups. Here we will use the local nomenclature, the event will have a given 'discipline' and 'country' so the user can back out the rules that govern the event. An agegroup combned with the `sex` of the athletes often defines the `category` that an event falls into.







