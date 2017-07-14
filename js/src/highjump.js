// direct copy of Andy's highjump.py

function Jumper(kwds) {
  const obj = {
    __init__(options) {
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
      if (cur.length > 3) throw new Error(`Can attempt a maximum of $(cur.length) times`);
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
      this.actions[this.actions.length] = ['retired', heightCount, height];
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

    setBarHeight(newHeight) {
      const prevHeight = this.heights.length ? this.heights[this.heights.length-1] : 0;
      if ((!this.inJumpOff)  && (prevHeight >= newHeight)) {
        throw new Error('The bar can only go up, except in a jump-off');
      }
      this.heights[this.heights.length] = newHeight;
      this.barHeight = newHeight;
    },

    cleared(bib) {
      // Record a successful jump
      const jumper = this.jumpersByBib[bib];
      jumper.cleared(this.heights.length, this.barHeight);
      this.actions[this.actions.length] = ['cleared', bib];
    },

    failed(bib) {
      // Record a failed jump. Throws RuleViolation if out of order
      const jumper = this.jumpersByBib[bib];
      jumper.failed(this.heights.length, this.barHeight);
      this.actions[this.actions.length] = ['failed', bib];
    },

    retired(bib) {
      // Record a failed jump. Throws RuleViolation if out of order
      const jumper = this.jumpersByBib[bib];
      jumper.retired(this.heights.length, this.barHeight);
      this.actions[this.actions.length] = ['retired', bib];
    },

    remaining() {
      // How many are left in the competition?
      let remaining = 0;
      for (let j; j<=this.jumpers.length; j++) if (!j.eliminated) remaining += 1;
      return remaining;
    },

    _compareSorterKeys(a, b) {
      // a & b are of the form [[x,y,z],jumper]
      // we only compare the [[x,y,z in order]
      return this.compare_keys(a[0], b[0]);
    },
    _compareKeys(a, b) {
      for (let i; i<a.length; i++) {
        if (a[i]===b[i]) continue;
        return (a[i]-0)<(b[i]-0) ? -1 : +1;
      }
      return 0;
    },

    _rank(quite) {
      // Determine who is winning
      // sort them
      let i;
      let j;
      let k;
      const sorter=[];
      const cmpkeys=this._compareKeys;
      for (i=0; i<this.rankedJumpers.length; i++) {
        sorter[i] = [j.ranking_key(), j];
      }
      sorter.sort(this._compareSorterKeys)

      let pk=null;
      let pj=null;
      for (i=0; i<sorter.length; i++) {
        k=sorter[i][0];
        j=sorter[i][1];
        if (i===0) {
          j.place = 1
        } else {
          j.place = (cmpkeys(pk, k) ? pj.place : i+1)
        }
        pk = k
        pj = j
        this.rankedJumpers[i] = j;
      }
    },

    displayBarHeight() {
      return parseFloat(Math.round(this.barHeight * 100) / 100).toFixed(2);
    },
  }
  obj.__init__();
  return obj;
}
module.exports = { HighJumpCompetition }
