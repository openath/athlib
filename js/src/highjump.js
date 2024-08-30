// direct copy of Andy's highjump.py
// The countback rule used to separate competitors with equal best heights in High Jump and Pole Vault
// is possibly the most misunderstood rule in the whole of the sport.s
// Here's how it operates:
// The athlete with the fewest attempts at the last height successfully cleared gets the verdict.
// This means that, no matter how poorly your earlier attempts have gone, there's still a way back into the competition.
// Then you count the athletes's number of failures, not including any attempts beyond the height actually cleared:
// the athlete with the fewest gets the verdict.
// So you cannot harm your cause by trying for a height which you think it unlikely that you will clear.
// But accurate jumping at the lower heights is vital!
// http://s250914043.websitehome.co.uk/offcourse/HighJumpRules.html

function Jumper(kwds) {
  const obj = {
    __init__(_options) {
      // Allow option setup
      this.order = 1; // if we get only one, I guess they jump first
      this._place = 1; // if we only get one, I guess they are winning

      // list of strings containing '', 'o', 'xo', 'xxo', 'xxx', 'x', 'xx'
      this.attemptsByHeight = [];
      this.highestCleared = 0;
      this.highestClearedIndex = -1;
      this.eliminated = false; // still in the competition?
      this.dismissed = false; // still in the round?
      this.roundLim = 3;
      this.consecutiveFailures = 0;
      const defaults = [
        'first_name',
        'unknown',
        'last_name',
        'athlete',
        'bib',
        '0',
        'team',
        'GUEST',
        'gender',
        'M', // sexist but valid
        'category',
        'OPEN',
        'order',
        1,
        'non_scorer',
        false
      ];

      const options = _options || {};

      for (let i = 0; i < defaults.length; i += 2) {
        const arg = defaults[i];
        let value = options[arg];

        if (typeof value === 'undefined') value = defaults[i + 1];
        if (arg === 'bib') value = `${value}`;
        this[arg] = value;
      }
    },

    get place() {
      if (this.order === 'DQ' || this.order === 'DNS') {
        return self.order;
      }
      if (this.highestClearedIndex < 0) {
        return '';
      }
      return this._place;
    },

    _setJumpArray(heightCount, label) {
      if (this.eliminated || this.dismissed) {
        const what = this.hasRetired ? 'retiring' : (this.eliminated ? 'being eliminated' : 'passing');

        throw new Error(`Cannot ${label ? label : 'jump'} after ${what}`);
      }
      // Ensure they have one string for each height in the competition
      // Jumpers can miss out heights.
      if (heightCount <= 0) throw new Error('Start at height number 1, not 0');
      // they may have skipped some, pas with empty strings
      const atts = this.attemptsByHeight;

      while (atts.length < heightCount) atts[atts.length] = '';
      if (
        this.attemptsByHeight[this.attemptsByHeight.length - 1].length >
        this.roundLim - 1
      ) {
        throw new Error(`Can attempt a maximum of ${this.roundLim} times`);
      }
    },

    get hasRetired() {
      return this.attemptsByHeight.length > 0 && this.attemptsByHeight[this.attemptsByHeight.length - 1].endsWith('r');
    },

    get rankingKey() {
      // Return a sort key to determine who is winning"""
      const x = this.highestClearedIndex;
      var failuresAtHeight;
      var failuresBeforeAndAtHeight;
      var i;

      if (x < 0) {
        failuresAtHeight = failuresBeforeAndAtHeight = 0;
      } else {
        failuresAtHeight = failuresBeforeAndAtHeight = this.attemptsByHeight[x].split('x').length - 1;
        for (i = 0; i < x; i++) failuresBeforeAndAtHeight += this.attemptsByHeight[i].split('x').length - 1;
      }
      if (this.highestCleared === 0 && this.attemptsByHeight.length === 0) {
        return [3, -0, 0, 0];
      }

      return [
        this.eliminated ? (x < 0 ? 3 : 2) : (x < 0 ? 1 : 0),
        -this.highestCleared,
        failuresAtHeight,
        failuresBeforeAndAtHeight
      ];
    },

    cleared(heightCount, height) {
      // Add a clearance at the current bar position
      // First round is index zero
      this._setJumpArray(heightCount);
      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length - 1;

      this.attemptsByHeight[n] += 'o';
      this.highestCleared = height;
      this.highestClearedIndex = n;
      this.consecutiveFailures = 0;
      this.dismissed = true;
    },

    // eslint-disable-next-line no-unused-vars
    failed(heightCount, height) {
      // Add a failure at the current bar position
      this._setJumpArray(heightCount);

      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length - 1;

      this.attemptsByHeight[n] += 'x';
      this.consecutiveFailures += 1;
      if (this.consecutiveFailures >= this.roundLim) {
        this.eliminated = this.dismissed = true;
      } else this.dismissed = false;
    },

    // eslint-disable-next-line no-unused-vars
    passed(heightCount, height) {
      // pass at the current height
      if (this.eliminated) {throw new Error('Cannot jump after being eliminated');}
      this._setJumpArray(heightCount, 'pass');

      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length - 1;

      this.attemptsByHeight[n] += '-';
      this.dismissed = true;
    },

    // eslint-disable-next-line no-unused-vars
    retired(heightCount, height) {
      // Competitor had enough, or pulls out injured
      this._setJumpArray(heightCount, 'retire');
      // Holds their pattern of 'o' and 'x'
      const n = this.attemptsByHeight.length - 1;

      this.attemptsByHeight[n] += 'r';
      this.eliminated = this.dismissed = true;
    }
  };

  obj.__init__(kwds);
  return obj;
}

// function to compare list of lists/numbers
function cmpKeys(a, b) {
  let r;
  let ai;
  let bi;

  // console.log('a, b', a, b);
  for (let i = 0; i < a.length; i++) {
    ai = a[i];
    bi = b[i];
    if (typeof ai === 'object') {
      r = cmpKeys(ai, bi);
      if (r) return r;
      continue;
    } else if (ai === bi) continue;
    return ai < bi ? -1 : 1;
  }
  return 0;
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
      this.heights = []; // sequence of heights so far
      this.inJumpOff = false;
      this.actions = []; // log for replay purposes.
      this.state = 'scheduled';
    },

    addJumper(kwds) {
      // Add one more person to the competition
      // Normally we add them first, but can arrive mid-competition.
      // If so, they are in last place until they clear a height.
      if (this.state !== 'scheduled') {
        throw new Error(
          `Cannot add jumpers in competition state ${this.state}`
        );
      }
      const j = Jumper(kwds);

      if (typeof this.jumpersByBib[j.bib] !== 'undefined') {
        throw new Error(
          `Cannot have two jumpers with the same bib (${this.bib})!`
        );
      }

      // j._place = this.jumpers.length + 1;

      this.jumpersByBib[j.bib] = j;
      this.jumpers[this.jumpers.length] = j;
      this.rankedJumpers[this.rankedJumpers.length] = j;

      // record what happened
      this.actions[this.actions.length] = ['addJumper', kwds];
    },

    setBarHeight(_newHeight) {
      if (this.state === 'scheduled') this.state = 'started';
      else if (
        this.state !== 'started' &&
        this.state !== 'jumpoff' &&
        this.state !== 'won' &&
        this.state !== 'drawn'
      ) {
        throw new Error(
          `Bar height cannot be set in a ${this.state} competition!`
        );
      }

      const newHeight = isNaN(_newHeight) ? parseFloat(_newHeight) : _newHeight;
      const prevHeight = this.heights.length ?
        this.heights[this.heights.length - 1] :
        0;
      let bib = 0;

      if (this.state !== 'jumpoff' && prevHeight >= newHeight) {
        throw new Error('The bar can only go up, except in a jump-off');
      }
      for (bib in this.jumpersByBib) {
        if (!this.jumpersByBib[bib].eliminated) {this.jumpersByBib[bib].dismissed = false;}
      }
      this.heights[this.heights.length] = newHeight;
      this.barHeight = newHeight;
      this.actions.push(['setBarHeight', newHeight]);
    },

    checkStarted(bib, _label) {
      const jumper = this.jumpersByBib[bib];
      const state = this.state;
      const label = _label ? _label : 'jumping';

      if (state !== 'started' && state !== 'jumpoff') {
        if (state === 'won') {
          if (jumper._place !== 1) {
            throw new Error(
              `The competition has been won; ${label} is not allowed!`
            );
          }
        } else if (state === 'finished') {
          throw new Error(
            `The competition has finished and ${label} is not allowed!`
          );
        } else throw new Error('The competition has not been started yet!');
      } else if (jumper.order === 'DQ' || jumper.order === 'DNS') {
        throw new Error(
          `Jumper bib=${bib} has order ${
            jumper.order
          }; ${label} is not allowed!`
        );
      }
      return jumper;
    },

    cleared(bib) {
      // Record a successful jump
      const jumper = this.checkStarted(bib);

      jumper.cleared(this.heights.length, this.barHeight);
      this.actions.push(['cleared', bib]);
      this._rank();
    },

    failed(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib);

      jumper.failed(this.heights.length, this.barHeight);
      this.actions.push(['failed', bib]);
      this._rank();
    },

    passed(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib);

      jumper.passed(this.heights.length, this.barHeight);
      this.actions.push(['passed', bib]);
      this._rank();
    },

    retired(bib) {
      // Record a failed jump. Throws Error if out of order
      const jumper = this.checkStarted(bib, 'retiring');

      jumper.retired(this.heights.length, this.barHeight);
      this.actions.push(['retired', bib]);
      this._rank();
    },

    get remaining() {
      const r = [];

      this.jumpers.forEach(j => {
        if (!j.eliminated) r.push(j);
      });
      return r;
    },

    get eliminated() {
      const r = [];

      this.jumpers.forEach(j => {
        if (j.eliminated) r.push(j);
      });
      return r;
    },

    _compareKeys(a, b) {
      return cmpKeys(a, b);
    },

    _rankj() {
      // sort them
      const rankj = this.rankedJumpers;
      const rankjlen = rankj.length;
      const state = this.state;
      let i;

      // console.log('rankj before', rankj);

      for (i = 0; i < rankjlen; i++) rankj[i]._oldPos = i;
      rankj.sort(function (a, b) {
        var r;
        var aRankingKey = a.rankingKey;
        var bRankingKey = b.rankingKey;

        if (state === 'started') {
          aRankingKey.shift();
          bRankingKey.shift();
        }

        // console.log(a.first_name, b.first_name);
        // console.log(aRankingKey, bRankingKey);
        r = cmpKeys([aRankingKey, a._oldPos], [bRankingKey, b._oldPos]);
        // console.log('result', r);
        return r;
      });

      let pk = null;
      let pj = null;

      let p = 0;

      for (i = 0; i < rankjlen; i++) {
        const j = rankj[i];
        const k = j.rankingKey;

        // console.log(j);

        delete j._oldPos;
        if (p === 0) {
          j._place = 1;
        } else {
          if (cmpKeys(pk, k) === 0) {
            j._place = pj._place;
          } else if (pj.non_scorer) {
            j._place = pj._place;
            p--;
          } else {
            j._place = p + 1;
          }
        }
        pk = k;
        pj = j;
        p++;
      }
      // console.log('rankj after', rankj);
      return rankj;
    },

    _rank() {
      var nc;

      // Determine who is winning
      const rankj = this._rankj();

      if (rankj.length === 0) return;

      const remj = this.remaining;

      if (remj.length === 0) {
        // they all failed or retired
        if (rankj.length > 1 && rankj[1]._place === 1) {
          nc = 0;
          rankj.forEach(j => {
            if (j._place === 1 && !j.hasRetired) {
              j.roundLim = 1;
              j.eliminated = false;
              j.consecutiveFailures = 0;
              nc += 1;
            }
          });
          this.state = nc > 0 ? 'jumpoff' : 'drawn';
        } else if (this.state === 'jumpoff' && !rankj[0].hasRetired) {
          const j = rankj[0];

          j.roundLim = 1;
          j.eliminated = false;
          j.consecutiveFailures = 0;
        } else {
          this.state = 'finished';
        }
      } else if (
        remj.length === 1 &&
        1 + this.eliminated.length === this.jumpers.length
      ) {
        const a = remj[0].attemptsByHeight;

        if (
          a.length === this.heights.length &&
          a[a.length - 1].split('o').length >= 2
        ) {
          this.state =
            this.state === 'started' || this.state === 'won' ?
              'won' :
              'finished';
        }
      } else {
        // Check for any athletes without jumps (should be eliminated)
        rankj.forEach(j => {
          // console.log(j.first_name + j.last_name, j.highestCleared === 0, j.attemptsByHeight.length === 0);
          if (this.state === 'finished' && j.highestCleared === 0 && j.attemptsByHeight.length === 0) {
            j.eliminated = true;
          }
        });
      }
      // console.log('this.rankedJumpers', this.rankedJumpers);
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

      objs.forEach(o => {
        if ('order' in o) {
          if (o.order > highest) highest = o.order;
        } else {
          unordered.push(o);
        }
      });
      for (let i = 0; i < unordered.length; i++) {
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
          throw Error(`Unknown jump trial code '${trial}'`);
      }
    },
    actionLetter: {
      cleared: 'o',
      failed: 'x',
      passed: '-',
      retired: 'r'
    },
    get trials() {
      const self = this;
      var T = [];
      const al = self.actionLetter;
      var bh;

      function processAction(v) {
        var a = v[0];

        if (a === 'setBarHeight') {
          bh = v[1];
        } else {
          a = al[a];
          if (typeof a === 'string') {
            T.push([v[1], bh, a]);
          }
        }
      }
      self.actions.forEach(processAction);
      return T;
    },
    get trialObjs() {
      return this.trials.map(function (t) {
        return {bib: t[0], height: t[1].toFixed(2), result: t[2]};
      });
    },
    fromActions(actions) {
      if (typeof actions === 'undefined') actions = this.actions.slice();
      const hj = HighJumpCompetition();

      actions.forEach(function (action) {
        hj[action[0]](action[1]);
      });
      return hj;
    },
    toMatrix(keys) {
      var i, j, R, J;

      if (typeof keys === 'undefined') keys = ['bib'];
      else if (keys.filter(function (k) {k === 'bib';}).length === 0) {
        keys.unshift('bib');
      }

      R = [keys.concat(this.heights.map(function (h) {return h.toFixed(2);}))];
      J = this.jumpers.map(function (j) {
        return [keys.map(function (k) {
          const jk = j[k];

          return typeof jk !== 'undefined' ? jk : '';
        }), j];
      });
      J = J.sort(cmpKeys);
      for (i = 0; i < J.length; i++) {
        j = J[i];
        R.push(j[0].concat(j[1].attemptsByHeight));
      }
      return R;
    },
    get isFinished() {
      return ['finished', 'won', 'drawn'].indexOf(this.state) >= 0;
    },
    get isRunning() {
      return this.state === 'started' || this.state === 'jumpoff';
    }
  };

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

  for (let colNo = 0; colNo < headers.length; colNo++) {
    const txt = headers[colNo];

    if (c._looksLikeHeight(txt)) {
      heights.push(parseFloat(txt));
      headers[colNo] = `h${heights.length}`;
    }
  }
  const objs = [];

  for (let rowNo = 1; rowNo < matrix.length; rowNo++) {
    const row = matrix[rowNo];
    const ob = {};

    for (let j = 0; j < headers.length; j++) {
      const key = headers[j];
      let value = row[j];

      if (typeof value === 'undefined') continue;
      if (key === 'bib') value = `${value}`;
      ob[key] = value;
    }
    objs.push(ob);
  }

  c._ensureObjsOrdered(objs);

  objs.sort((a, b) => {
    const la = a.order;
    const lb = b.order;

    if (la === lb) return 0;
    return la < lb ? -1 : +1;
  });

  objs.forEach(o => {
    c.addJumper(o);
  });

  const n = !toNthHeight ? heights.length : toNthHeight - 0;

  for (let i = 0; i < n; i++) {
    const height = heights[i];
    const heightKey = `h${i + 1}`;

    c.setBarHeight(height);
    for (let a = 0; a < 3; a++) {
      for (let j = 0; j < objs.length; j++) {
        const ob = objs[j];
        const bib = ob.bib;

        if (ob.order === 'DNS' || ob.order === 'DQ') continue;
        let name = ob.last_name;

        if (!name) name = '';
        let attempts = ob[heightKey];

        if (!attempts) attempts = '';
        if (attempts.length > a) {
          c.bibTrial(bib, attempts[a]);
        }
      }
    }
  }
  return c;
};
module.exports = { HighJumpCompetition };
