
Schemas
=======


We'll start documenting the different schemas here.

We could use schemas for
 * fixtures - a list of meetings
 * full meeting results
 * programme and structure of meeting



At the moment, we're just fiddling around with reStructuredText to find a way to lay out attributes with minimal typing. Tables are a pain to type.  What follows is an example.

Results
-------

This is usually a two-level, nested structure.  At the top level we have information about the race.  nested within it, there will be a number of 


List of runners

:bib:  text or numeric.  The race number worn by the athlete
:rank:	the runner's finishing position.  numeric.  If two runners place equal, they may both be give e.g. `1`, but the next runner should be given `3`
:givenName:  first name, in Western languages.
:familyName:  surname, in Western languages
:points:  if scoring, the numner of points earned by the runner
:category:  this may be used for non-overlapping prize categories, such as "Senior Men", "Women over 40".  It is common to produce a listing of the leaders in each category, or to offer prizes.  Categories are often, but not always, aligned with age groups and genders.
:performance:  the finishing time, represented in hours/minutes/seconds as text e.g. "35:24"