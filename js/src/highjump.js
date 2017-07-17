// direct copy of Andy's highjump.py

function Jumper(kwds) {
  const obj = {
    __init__(_options) {
      // Allow option setup
      this.order = 1; // if we get only one, I guess they jump first
      this.place = 1; // if we only get one, I guess they are winning

      // list of strings containing '', 'o', 'xo', 'xxo', 'xxx', 'x', 'xx'
      this.attemptsByHeight = [];
      this.highestCleared = 0;
      this.failuresAtHeight = 0;
      this.consecutiveFailures = 0;
      this.totalFailures = 0;
      this.eliminated = false;  // still in the competition?
      const defaults = [
        'first_name', 'unknown',
        'last_name', 'athlete',
        'bib', '0',
        'team', 'GUEST',
        'gender', 'M',  // sexist but valid
        'category', 'OPEN',
      ];

      const options = _options || {};
      for (let i=0; i<defaults.length; i+=2) {
        const arg = defaults[i];
        let value = options[arg];
        if (typeof value==='undefined') value=defaults[i+1];
        if (arg==='bib') value = `${value}`;
        this[arg] = value;
      }
    },

    _setJumpArray(heightCount) {
      const atts = this.attemptsByHeight;
      // Ensure they have one string for each height in the competition
      // Jumpers can miss out heights.
      if (heightCount<=0) throw new Error('Start at height number 1, not 0');
      // they may have skipped some, pas with empty strings
      while (atts.length < heightCount) atts[atts.length] = '';
    },

    rankingKey() {
      // Return a sort key to determine who is winning"""
      return [-this.highestCleared, this.failuresAtHeight, this.totalFailures];
    },

    cleared(heightCount, height) {
      // Add a clearance at the current bar position
      // First round is index zero
      if (this.eliminated) throw new Error('Cannot jump after being eliminated');
      this._setJumpArray(heightCount);
      // Holds their pattern of 'o' and 'x'
      let cur = this.attemptsByHeight[this.attemptsByHeight.length-1];
      cur += 'o';
      this.attemptsByHeight[this.attemptsByHeight.length-1] = cur;
      if (cur.length > 3) throw new Error(`Can attempt a maximum of ${cur.length} times`);
      this.highestCleared = height;
      this.failuresAtHeight = 0;
      this.consecutiveFailures = 0;
    },

    failed(heightCount, height) {
      // Add a failure at the current bar position
      if (this.eliminated) throw new Error('Cannot jump after being eliminated');
      this._setJumpArray(heightCount);

      // Holds their pattern of 'o' and 'x'
      let cur = this.attemptsByHeight[this.attemptsByHeight.length-1];
      cur += 'x';
      this.attemptsByHeight[this.attemptsByHeight.length-1] = cur;
      if (cur.length>3) throw new Error('More than 3 attempts at height');
      this.failuresAtHeight += 1;
      this.consecutiveFailures += 1;
      this.totalFailures += 1;
      if (this.consecutiveFailures===3) this.eliminated=true;
    },

    retired(heightCount, height) {
      // Competitor had enough, or pulls out injured
      if (this.eliminated) throw new Error('Cannot retire after being eliminated');
      this._setJumpArray(heightCount);
      // Holds their pattern of 'o' and 'x'
      const atts = this.attemptsByHeight;
      let cur = atts[atts.length-1];
      cur += 'r';
      this.attemptsByHeight[this.attemptsByHeight.length-1] = cur;
      if (cur.length>3) throw new Error('More than 3 attempts at height');
      this.eliminated = true;
    },
    displayHeight() {
      return parseFloat(Math.round(this.height * 100) / 100).toFixed(2);
    },
  }
  obj.__init__(kwds);
  return obj;
}

function HighJumpCompetition() {
  // Simulation of a HighJump competition in progress.
  // This is a small "state machine" which respons to things like
  // "raise the bar", "do a jump", and aims to tell you who is leading
  // at any point.
  const obj = {
    __init__() {
      this.jumpers = [];
      this.jumpersByBib = {};
      this.rankedJumpers = [];
      this.barHeight = 0;
      this.trials = [];
      this.heights = [];  // sequence of heights so far
      this.inJumpOff = false;
      this.actions = [];  // log for replay purposes.
    },

    addJumper(kwds) {
      // Add one more person to the competition
      // Normally we add them first, but can arrive mid-competition.
      // If so, they are in last place until they clear a height.
      const j = Jumper(kwds);
      j.place = this.jumpers.length + 1;

      this.jumpersByBib[j.bib] = j;
      this.jumpers[this.jumpers.length]=j;
      this.rankedJumpers[this.rankedJumpers.length] = j;

      // record what happened
      this.actions[this.actions.length]=['addJumper', kwds];
    },

    setBarHeight(_newHeight) {
      const newHeight = isNaN(_newHeight) ? parseFloat(_newHeight) : _newHeight;
      const prevHeight = this.heights.length ? this.heights[this.heights.length-1] : 0;
      if ((!this.inJumpOff)  && (prevHeight >= newHeight)) {
        throw new Error('The bar can only go up, except in a jump-off');
      }
      this.heights[this.heights.length] = newHeight;
      this.barHeight = newHeight;
      this.actions.push(['setBarHeight', newHeight]);
    },

    cleared(bib) {
      // Record a successful jump
      const jumper = this.jumpersByBib[bib];
      jumper.cleared(this.heights.length, this.barHeight);
      this._rank()
      this.actions.push(['cleared', bib]);
    },

    failed(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.jumpersByBib[bib];
      jumper.failed(this.heights.length, this.barHeight);
      this._rank()
      this.actions.push(['failed', bib]);
    },

    retired(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.jumpersByBib[bib];
      jumper.retired(this.heights.length, this.barHeight);
      this._rank()
      this.actions.push(['retired', bib]);
    },

    remaining() {
      // How many are left in the competition?
      let remaining = 0;
      for (let j; j<=this.jumpers.length; j++) if (!j.eliminated) remaining += 1;
      return remaining;
    },

    _compareKeys(a, b) {
      for (let i=0; i<a.length; i++) {
        if (a[i]===b[i]) continue;
        return a[i]<b[i] ? -1 : 1;
      }
      return 0;
    },

    _rank() {
      // Determine who is winning
      // sort them
      const sorter=[];
      const cmpKeys=this._compareKeys;
      this.rankedJumpers.map((j) => {sorter.push([j.rankingKey(), j])});
      sorter.sort((a, b) => cmpKeys(a[0], b[0]));

      let pk=null;
      let pj=null;
      for (let i=0; i<sorter.length; i++) {
        const k=sorter[i][0];
        const j=sorter[i][1];
        if (i===0) {
          j.place = 1
        } else {
          j.place = (cmpKeys(pk, k)===0? pj.place : i+1)
        }
        pk = k
        pj = j
        this.rankedJumpers[i] = j;
      }
    },

    displayBarHeight() {
      return parseFloat(Math.round(this.barHeight * 100) / 100).toFixed(2);
    },


    _looksLikeHeight(txt) {
      return !isNaN(parseFloat(txt));
    },


    _ensureObjsOrdered(objs) {
      // Ensure they each have an 'order' attribute in which they jump

      // If partially present, respect ordered ones first and place others after
      const unordered = [];
      let highest = 0;
      objs.map((o) => {
        if ('order' in o) {
          if (o.order>highest) highest = o.order;
        } else {
          unordered.push(o);
        }
      });
      for (let i=0; i<unordered.length; i++) {
        highest++;
        unordered[i].order = highest;
      }
    },
  }
  obj.__init__();
  return obj;
}

HighJumpCompetition.fromMatrix = function fromMatrix(matrix, toNthHeight) {
  // Convert from a pasteable tabular representation like this...

  // RIO_MENS_HJ = [  # pasted from Wikipedia
  //  ["place", "order", "bib", "first_name", "last_name", "team", "2.20", "2.25",
  //                    "2.29", "2.33", "2.36", "2.38", "2.40", "best", "note"],
  //  ["1", 7, 2197, "Derek", "Drouin", "Canada", "o", "o", "o", "o", "o", "o",
  //                     "x", 2.38, ""],
  //  ["2", 9, 2878, "Mutaz", "Essa Barshim", "Qatar", "o", "o", "o", "o", "o", "xxx",
  //                     "", 2.36, ""],
  // ]

  // Column headers looking like numbers will be taken as the heights.  They may repeat,
  // as for a jumpoff where the bar comes down again.
  // We pay attention only to order, bib, first_name, last_name, team, category and
  // the heights.
  // The place and best are calculated so discarded.  The personal details may be used to
  // create competitor records if corresponding ones are not found.

  // replays the bar heights up to the Nth bar if given.
  // pass None for an empty competition.
  const c = HighJumpCompetition();
  // heights are in the top row - change to h1, h2 etc
  const heights = [];
  const headers = matrix[0].slice(0);
  for (let colNo=0; colNo<headers.length; colNo++) {
    const txt = headers[colNo];
    if (c._looksLikeHeight(txt)) {
      heights.push(parseFloat(txt));
      headers[colNo] = `h${heights.length}`;
    }
  }
  const objs = [];
  for (let rowNo=1; rowNo<matrix.length; rowNo++) {
    const row = matrix[rowNo];
    const ob = {};
    for (let j=0; j<headers.length; j++) {
      const key = headers[j];
      let value = row[j];
      if (typeof value==='undefined') continue;
      if (key==='bib') value = `${value}`;
      ob[key] = value;
    }
    objs.push(ob);
  }

  c._ensureObjsOrdered(objs);

  objs.sort((a, b) => {
    const la=a.order;
    const lb=b.order;
    if (la===lb) return 0; return la<lb?-1:+1;
  });

  objs.map((o) => {c.addJumper(o)});

  const n = !toNthHeight ? heights.length : toNthHeight - 0;
  for (let i=0; i<n; i++) {
    const height = heights[i];
    const heightKey = `h${i + 1}`;
    c.setBarHeight(height);
    for (let a=0; a<3; a++) {
      for (let j=0; j<objs.length; j++) {
        const ob = objs[j];
        const bib = ob.bib;
        let name  = ob.last_name;
        if (!name) name='';
        let attempts = ob[heightKey];
        if (!attempts) attempts='';
        if (attempts.length > a) {
          const result = attempts[a];
          switch (result) {
            case 'o': 
              c.cleared(bib);
              break;
            case 'x':
              c.failed(bib);
              break;
            case 'r':
              c.retired(bib);
              break;
            case '-':
              // often, this is pasted to indicate an explicit 'pass'
              break;
            default:
              throw Error(`Unknown jump result code \'${result}\'`);
          }
        }
      }
    }
  }
  return c;
}
module.exports = { HighJumpCompetition }
