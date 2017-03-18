
Identity
=======

A large part of the problem is to agree on a common set of `identifiers` for the main `things` in athletics. When we're exchanging data, we need to know when we are talking about the same competition, organisation, venue or person.

In the securities business, every fund or stock has an `ISIN` - `Individual Security Identification Number`. Without these, financial trade would be impossible.

We propose (in fact, we're working on) the creation of an open, public registry which is free for anyone to use; and some voluntary standards.  The main entities to be tracked are the `big four` - Organisations, Venues, Competitions and People.

We hope to start in a top-down manner by giving national governing bodies the ultimate say over their country.   The key concepts are:

 * an *identity server* - a public web server where all the things can be registered and found.  We'll start at http://data.opentrack.run/, and welcome anyone wanting to set up mirrors.  Data will be available in several formats - browsing by humans, JSON or XML records, and bulk downloads.
  * `Universally Unique IDs` or `UUIDs` for each major thing in the sport (Organisation, Person, Venue, Competition).  UUIDs are big long numbers used in software.  They never clash, so if a system is already giving UUIDs to things (like the Danish competition management system), we can just use theirs
 * human-readable `short codes` or `slugs` which are unique in the country, or possibly year.  These need to be chosen at some point to use our tools
 * a permanent URL or home page for each thing.  For example, the world's oldest running club, Thames Hare and Hounds (usually abbreviated `THH`), can be found at http://data.opentrack.run/o/gbr/thh/.    Anyone else building big athletics databases is invited to use the same codes and relative urls.


On this page we will have a shot, terse record with links to other things.  Humans can see HTML, and API clients can see JSON or XML.  


URL scheme and codes
==========

Organisations
----------
We suggest that all organisations in athletics eventually end up with a code like this:

	/o/<countrycode>/<org-code>/

They can be identified when first discovered with a URL like this

    /o/<uuid>

but the UUIDs are long and painful  Much better for them to choose a code when they want to use the system (e.g. to enter a competition)


<countrycode> is a 3-letter ISO country code (GBR, EST etc).  <org-code> is a code of up to 5 characters which is unique within the country.  5 is long enough to handle abbreviations.
 * Spain has given 5 letter codes to all 250 or so clubs in the country.  
 * The UK has abbreviations used by Athletics Weekly, but these often include spaces, capital, lowercase letters and apostrophes - not good for data interchange.  However, league results often use 3 letter codes.  We have been promoting simpler codes on a first-come-first-served basis, as people enter our systems.
 * Estonia has chosen 4 or 5 letter codes for all their clubs

We might allow longer codes for `universities` - by which we mean any educational institution for young adults (18+) and `schools`.  These compete some of the time, but there are so many schools that it would crowd out the clubs. For example, we believe there are abou 18,000 schools in the UK.    We still don't know how many are named "King Henry VIII", but it's a lot.  One suggestion is a prefix:  "UNI" or "SCH", then a longer mnemomnic.  

If there are good global standards for identifying universities, we'd like to know about it.



Competitions
---------
Competitions are prefixed with 'x'.  We considered 'c', but 'x' is short and has connatations of 'against', so it seems appropriate.

Competitions may choose a `slug` - a URL component - which is unique for the country AND year.  This is because in most cases, they happen year after year.

    /x/<year><countrycode>/<slug>/

    /x/<uuid>

    /x/2017/gbr/lm/    - London Marathon
    /x/2017/gbr/rosenheim-final/  - final match of Rosenheim League
    /x/2017/gbr/hercopen/  - Hercules Open Meeting

    /x/2017/est/ekv-in/  - Estonian Inter-Club Cup (indoors)


For events which recur, we can build up suffixes.  e.g. the Thames Hare and Hounds "Second Sunday" race is monthly, so we can name it
  
    /x/2017/gbr/thhss07    - July (month 17) race in series

And the 3rd of 4 matches in the Surrey League (Men), Division 2, might be

    /x/2017/gbr/slmd1m3  `Surrey League Men, Division 1, Match 3`




Venues
-----

	/v/<country-code>/<venue-code>/

We can start with athletics tracks.  We have found about 4000 in Europe so far by searching OpenStreetMap. We will give them UUIDs as we discover them.

We suggest taking the name normally used by the local athletes, and `slugifying` it - turning it into something URL-safe.  Do NOT use the city name unless there is only one track. Also, pleas do not use sponsors' names (`The HugeCo Stadium`) as these may change.  

	/v/gbr/iffley-road/  - Iffley Road in Oxford, where the four minute mile was run

Naming should be 'first come first served'


People
-----

This is the contentious part, where privacy advocates may scream "what?  another database?"

Our view is that almost every federation and many other bodies are constantly trying to identify people, and this is one of the major bottlenecks in the sport, taking up huge amounts of volunteer time.  In future, it MIGHT make sense to have a global directory.  In the short term, in the countries we operate, it is necessary to give a unique ID to licensed athletes.  


UUIDs will be far more common here, but we could potentially let people who use OpenTrack to register an identity if they wished.  They might do this to correct their date, upload a photo, or link their athletics results to their social media identities.

    /p/<uuid>/

    /p/est/erki-nool/  - the 2000 Olympic Decathlon champion, Erki Nool, from Estonia

Imagine that if you visited the page above, you could see links to Erki Nool's page on the national results, Wikipedia page, and the athlete's page on the IAAF or European Athletics websites.

We would prefer not to encourage anonymous handles like "sprinter123" and must be mindful of clashes.  There are a LOT of people called 'Andy Robinson' in the sport in the UK.

Dealing with duplicates and deletions
-------------

Over time we may discover that people are the same person, and likewise with other records.  In these cases we can update the URL with a `redirect` - if you browse to the page, you will be sent onto a new one.  Similarly, we will create a number of record types for inactive or past entities:  tracks closed, clubs merged.

