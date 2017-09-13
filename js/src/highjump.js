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
      this.highestClearedIndex = -1
      this.totalFailures = 0;
      this.eliminated = false;  // still in the competition?
      this.dismissed = false;  // still in the round?
      this.roundLim = 3;
      this.consecutiveFailures = 0;
      const defaults = [
        'first_name', 'unknown',
        'last_name', 'athlete',
        'bib', '0',
        'team', 'GUEST',
        'gender', 'M',  // sexist but valid
        'category', 'OPEN',
        'order', 1,
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

    _setJumpArray(heightCount, label) {
      if (this.eliminated || this.dismissed) {
        const what = this.eliminated ? 'being eliminated' : 'passing';
        throw new Error(`Cannot ${label ? label : 'jump'} after ${what}`);
      }
      // Ensure they have one string for each height in the competition
      // Jumpers can miss out heights.
      if (heightCount<=0) throw new Error('Start at height number 1, not 0');
      // they may have skipped some, pas with empty strings
      const atts = this.attemptsByHeight;
      while (atts.length < heightCount) atts[atts.length] = '';
      if (this.attemptsByHeight[this.attemptsByHeight.length-1].length > this.roundLim-1) {
        throw new Error(`Can attempt a maximum of ${this.roundLim} times`)
      }
    },

    get rankingKey() {
      // Return a sort key to determine who is winning"""
      const x = this.highestClearedIndex;
      const failuresAtHeight = x<0 ? this.roundLim : (this.attemptsByHeight[x].split('x').length-1);
      return [-this.highestCleared, failuresAtHeight, this.totalFailures];
    },

    cleared(heightCount, height) {
      // Add a clearance at the current bar position
      // First round is index zero
      this._setJumpArray(heightCount);
      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length-1;
      this.attemptsByHeight[n] += 'o';
      this.highestCleared = height;
      this.highestClearedIndex = n;
      this.consecutiveFailures = 0;
      this.dismissed = true;
    },

    failed(heightCount, height) {
      // Add a failure at the current bar position
      this._setJumpArray(heightCount);

      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length-1;
      this.attemptsByHeight[n] += 'x';
      this.totalFailures += 1;
      this.consecutiveFailures += 1;
      if (this.consecutiveFailures>=this.roundLim) this.eliminated = this.dismissed = true;
      else this.dismissed = false;
    },

    passed(heightCount, height) {
      // pass at the current height
      if (this.eliminated) throw new Error('Cannot jump after being eliminated');
      this._setJumpArray(heightCount, 'pass');

      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length-1;
      this.attemptsByHeight[n] += '-';
      this.dismissed = true;
    },

    retired(heightCount, height) {
      // Competitor had enough, or pulls out injured
      this._setJumpArray(heightCount, 'retire');
      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length-1;
      this.attemptsByHeight[n] += 'r';
      this.eliminated = this.dismissed = true;
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
      this.state = 'scheduled';
    },

    addJumper(kwds) {
      // Add one more person to the competition
      // Normally we add them first, but can arrive mid-competition.
      // If so, they are in last place until they clear a height.
      if (this.state!=='scheduled') {
        throw new Error(`Cannot add jumpers in competition state ${this.state}`)
      }
      const j = Jumper(kwds);
      j.place = this.jumpers.length + 1;

      this.jumpersByBib[j.bib] = j;
      this.jumpers[this.jumpers.length]=j;
      this.rankedJumpers[this.rankedJumpers.length] = j;

      // record what happened
      this.actions[this.actions.length]=['addJumper', kwds];
    },

    setBarHeight(_newHeight) {
      if (this.state==='scheduled') this.state = 'started';
      else if (this.state!=='started' && this.state!=='jumpoff' && this.state!=='won') {
        throw new Error(`Bar height cannot be set in a ${this.state} competition!`);
      }

      const newHeight = isNaN(_newHeight) ? parseFloat(_newHeight) : _newHeight;
      const prevHeight = this.heights.length ? this.heights[this.heights.length-1] : 0;
      let bib = 0;
      if ((this.state!=='jumpoff')  && (prevHeight >= newHeight)) {
        throw new Error('The bar can only go up, except in a jump-off');
      }
      for (bib in this.jumpersByBib) {
        if (!this.jumpersByBib[bib].eliminated) this.jumpersByBib[bib].dismissed = false;
      }
      this.heights[this.heights.length] = newHeight;
      this.barHeight = newHeight;
      this.actions.push(['setBarHeight', newHeight]);
    },

    checkStarted(bib, _label) {
      const jumper = this.jumpersByBib[bib];
      const state = this.state;
      if (state!=='started' && state!=='jumpoff') {
        const label = _label ? _label : 'jumping';
        if (state==='won') {
          if (jumper.place!==1) {
            throw new Error(`The competition has been won and ${label} is not allowed!`);
          }
        } else if (state==='finished') {
          throw new Error(`The competition has finished and ${label} is not allowed!`);
        } else throw new Error('The competition has not been started yet!')
      }
      return jumper;
    },

    cleared(bib) {
      // Record a successful jump
      const jumper = this.checkStarted(bib);
      jumper.cleared(this.heights.length, this.barHeight);
      this.actions.push(['cleared', bib]);
      this._rank()
    },

    failed(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib);
      jumper.failed(this.heights.length, this.barHeight);
      this.actions.push(['failed', bib]);
      this._rank()
    },

    passed(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib);
      jumper.passed(this.heights.length, this.barHeight);
      this.actions.push(['passed', bib]);
      this._rank()
    },

    retired(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib, 'retiring');
      jumper.retired(this.heights.length, this.barHeight);
      this.actions.push(['retired', bib]);
      this._rank()
    },

    get remaining() {
      const r = [];
      this.jumpers.forEach((j) => {if (!j.eliminated) r.push(j)});
      return r;
    },

    get eliminated() {
      const r = [];
      this.jumpers.forEach((j) => {if (j.eliminated) r.push(j)});
      return r;
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
      this.rankedJumpers.forEach((j) => {sorter.push([j.rankingKey, j])});
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
      const remj = this.remaining;
      if (remj.length===0) {
        const rankj = this.rankedJumpers;
        if (rankj.length>1 && rankj[1].place===1) {
          this.state = 'jumpoff';
          rankj.forEach((_j) => {
            const j=_j
            if (j.place===1) {
              j.roundLim=1
              j.eliminated=false
              j.consecutiveFailures=0;
            }});
        } else this.state = 'finished';
      } else if (remj.length===1 && (1+this.eliminated.length)===this.jumpers.length) {
        const a = remj[0].attemptsByHeight;
        if (a.length===this.heights.length && a[a.length-1].split('o').length>=2) {
          this.state = (this.state==='started'||this.state==='won') ? 'won' : 'finished';
        }
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
      objs.forEach((o) => {
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

    bibTrial(bib, trial) {
      switch (trial) {
        case 'o': 
          this.cleared(bib);
          break;
        case 'x':
          this.failed(bib);
          break;
        case 'r':
          this.retired(bib);
          break;
        case '-':
          // often, this is pasted to indicate an explicit 'pass'
          break;
        default:
          throw Error(`Unknown jump trial code \'${trial}\'`);
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

  objs.forEach((o) => {c.addJumper(o)});

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
          c.bibTrial(bib, attempts[a]);
        }
      }
    }
  }
  return c;
}
module.exports = { HighJumpCompetition }
