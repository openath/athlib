// direct copy of Andy's highjump.py

function Jumper(kwds) {
  const obj = {
    __init__(options) {
      // Allow option setup
      this.order = 1; // if we get only one, I guess they jump first
      this.place = 1; // if we only get one, I guess they are winning

      // list of strings containing '', 'o', 'xo', 'xxo', 'xxx', 'x', 'xx'
      this.attempts_by_height = [];
      this.highest_cleared = 0;
      this.failures_at_height = 0;
      this.consecutive_failures = 0;
      this.total_failures = 0;
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
        if (arg==='bib') value = ''+value;
        this[arg] = value;
      }
    },

    _set_jump_array (height_count) {
      var atts = this.attempts_by_height;
      // Ensure they have one string for each height in the competition
      // Jumpers can miss out heights.
      if (height_count<=0) throw 'Start at height number 1, not 0';
      // they may have skipped some, pas with empty strings
      while (atts.length < height_count) atts[atts.length] = '';
    },

    ranking_key () {
      // Return a sort key to determine who is winning"""
      return [-this.highest_cleared, this.failures_at_height, this.total_failures];
    },

    cleared (height_count, height) {
      // Add a clearance at the current bar position
      // First round is index zero
      if (this.eliminated) throw 'Cannot jump after being eliminated';
      this._set_jump_array(height_count);
      // Holds their pattern of 'o' and 'x'
      let cur = this.attempts_by_height[this.attempts_by_height.length-1];
      cur += 'o';
      this.attempts_by_height[this.attempts_by_height.length-1] = cur;
      if (cur.length > 3) throw 'Can attempt a maximum of '+cur.length+' times';
      this.highest_cleared = height;
      this.failures_at_height = 0;
      this.consecutive_failures = 0;
    },

    failed (height_count, height) {
      // Add a failure at the current bar position
      if (this.eliminated) throw 'Cannot jump after being eliminated';
      this._set_jump_array(height_count);

      // Holds their pattern of 'o' and 'x'
      let cur = this.attempts_by_height[this.attempts_by_height.length-1];
      cur += 'x';
      this.attempts_by_height[this.attempts_by_height.length-1] = cur;
      if (cur.length>3) throw 'More than 3 attempts at height';
      this.failures_at_height += 1;
      this.consecutive_failures += 1;
      if (this.consecutive_failures===3) this.eliminated=true;
    },

    retired (height_count, height) {
      // Competitor had enough, or pulls out injured
      if (this.eliminated) throw 'Cannot retire after being eliminated';
      this._set_jump_array(height_count);
      // Holds their pattern of 'o' and 'x'
      var atts = this.attempts_by_height;
      cur = atts[atts.length-1];
      cur += 'r';
      this.attempts_by_height[this.attempts_by_height.length-1] = cur;
      if (len(cur)>3) throw 'More than 3 attempts at height';
      this.eliminated = true;
      this.actions[this.actions.length] = ['retired', height_count, height];
    },
    display_height () {
      return parseFloat(Math.round(this.height * 100) / 100).toFixed(2);
    }
  }
  obj.__init__(kwds);
  return obj;
}

function HighJumpCompetition() {
  // Simulation of a HighJump competition in progress.
  // This is a small "state machine" which respons to things like
  // "raise the bar", "do a jump", and aims to tell you who is leading
  // at any point.
  var obj = {
    __init__ () {
      this.jumpers = [];
      this.jumpers_by_bib = {};
      this.ranked_jumpers = [];
      this.bar_height = 0;
      this.trials = [];
      this.heights = [];  // sequence of heights so far
      this.in_jump_off = false;
      this.actions = [];  // log for replay purposes.
    },

    add_jumper (kwds) {
      // Add one more person to the competition
      // Normally we add them first, but can arrive mid-competition.
      // If so, they are in last place until they clear a height.
      var j = Jumper(kwds);
      j.place = this.jumpers.length + 1;

      this.jumpers_by_bib[j.bib] = j;
      this.jumpers[this.jumpers.length]=j;
      this.ranked_jumpers[this.ranked_jumpers.length] = j;

      // record what happened
      this.actions[this.actions.length]=['add_jumper', kwds];
    },

    set_bar_height (new_height) {
      var prev_height = this.heights.length ? this.heights[this.heights.length-1] : 0;
      if ((!this.in_jump_off)  && (prev_height >= new_height)) throw 'The bar can only go up, except in a jump-off';
      this.heights[this.heights.length] = new_height;
      this.bar_height = new_height;
    },

    cleared (bib) {
      // Record a successful jump
      var jumper = this.jumpers_by_bib[bib];
      jumper.cleared(this.heights.length, this.bar_height);
      this.actions[this.actions.length] = ['cleared', bib];
    },

    failed (bib) {
      // Record a failed jump. Throws RuleViolation if out of order
      var jumper = this.jumpers_by_bib[bib];
      jumper.failed(this.heights.length, this.bar_height);
      this.actions[this.actions.length] = ['failed', bib];
    },

    retired (bib) {
      // Record a failed jump. Throws RuleViolation if out of order
      var jumper = this.jumpers_by_bib[bib];
      jumper.retired(this.heights.length, this.bar_height);
      this.actions[this.actions.length] = ['retired', bib];
    },

    remaining () {
      // How many are left in the competition?
      var remaining = 0;
      for (var j; j<=this.jumpers.length; j++) if (!j.eliminated) remaining += 1;
      return remaining;
    },

    _compare_sorter_keys(a, b) {
      // a & b are of the form [[x,y,z],jumper]
      // we only compare the [[x,y,z in order]
	  return this.compare_keys(a[0],b[0]);
		},
	_compare_keys(a,b){
      for (let i; i<a.length; i++) {
        if (a[i]===b[i]) continue;
        return (a[i]-0)<(b[i]-0) ? -1 : +1;
      }
      return 0;
    },

    _rank (quite) {
      // Determine who is winning
      // sort them
      let i, j, k, sorter=[]
	  const cmpkeys=this._compare_keys;
      for (i=0; i<this.ranked_jumpers.length; i++) {
        sorter[i] = [j.ranking_key(), j];
      }
      sorter.sort(this._compare_sorter_keys)

      var pk=null, pj=null;
      for (i=0; i<sorter.length; i++) {
        k=sorter[i][0];
        j=sorter[i][1];
        j.place = !i ? 1 : (cmpkeys(pk,k) ? pj.place : i+1);
        pk = k
        pj = j
        this.ranked_jumpers[i] = j;
      }
    },

    display_bar_height () {
      return parseFloat(Math.round(this.bar_height * 100) / 100).toFixed(2);
    }
  }
  obj.__init__();
  return obj;
}
module.exports = { HighJumpCompetition }
