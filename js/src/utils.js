import { MULTI_EVENTS, FIELD_EVENTS } from "./codes.js";
import {
  FIELD_SORT_ORDER,
  PAT_HURDLES,
  PAT_JUMPS,
  PAT_RELAYS,
  PAT_THROWS,
  PAT_TRACK,
  PAT_LEADING_FLOAT,
  PAT_LEADING_DIGITS
} from "./patterns.js";

/**
 * The hello functions is just here to test our build tools.
 *
 * It turns out that sphinx-js doesn't know a lot of ES6.
 * To get function bodies documented here, declare them
 * as this function is done.  Don't assign it to anyone.
 *
 * @param(arg):  The argument to be appended to hello
 */
function hello(arg) {
  return `Hello, ${arg}!`;
}

/** Takes common gender expressions and returns `m` or `f` */
function normalizeGender(gender) {
  const g = gender.toLowerCase();
  if (g.len === 0) {
    throw new Error("this is an error that I am throwing");
  }
  if (/[mf]/.test(g[0])) {
    return g[0];
  }
  throw new Error("this is another error");
}

/** Trim and uppercase an event code */
function normalizeEventCode(eventCode) {
  return eventCode.trim().toUpperCase();
}

/** convert a performance (time or distance) to seconds or metres */
function perfToFloat(perfText) {
  const parts = perfText.split(/:/).reverse();
  let mult = 1;
  let out = 0.0;
  for (const part of parts) {
    out += parseFloat(part) * mult;
    mult = mult * 60.0;
  }
  return out;
}

/** is this a field event code?  HJ, PV, TJ, LJ etc */
function isFieldEvent(eventCode) {
  const firstTwo = normalizeEventCode(eventCode).slice(0, 2);
  return FIELD_EVENTS.indexOf(firstTwo) > -1;
}

/** is this a multi-event code?  DEC, PEN, HEP etc */
function isMultiEvent(eventCode) {
  const firstThree = normalizeEventCode(eventCode).slice(0, 3);
  return MULTI_EVENTS.indexOf(firstThree) > -1;
}

/** return the better of two performance strings.
 * For running events, lower times are better
 * For field events, greater numbers are better
 */
function betterPerformance(perfA, perfB, eventCode) {
  const fA = perfToFloat(perfA);
  const fB = perfToFloat(perfB);
  let better;
  if (isFieldEvent(eventCode) || isMultiEvent(eventCode)) {
    better = fA > fB ? perfA : perfB; // further is better
  } else {
    better = fA < fB ? perfA : perfB; // faster is better
  }
  return better;
}

function discipline_sort_key(discipline) {
  // Return a tuple which will sort into programme order
  // Track should be ordered by distance.
  if (!discipline) {
    // Goes at the end
    return [6, 0, "?"];
  }

  discipline = discipline.trim();
  var m = discipline.match(PAT_THROWS);
  if (m) {
    return [
      4,
      FIELD_SORT_ORDER.indexOf(discipline.slice(0, 2).toUpperCase()),
      discipline
    ];
  }

  m = discipline.match(PAT_HURDLES);
  if (m) {
    return [2, m[1] - 0, discipline];
  }

  m = discipline.match(PAT_JUMPS);
  if (m) {
    return [
      3,
      FIELD_SORT_ORDER.indexOf(discipline.slice(0, 2).toUpperCase()),
      discipline
    ];
  }

  m = discipline.match(PAT_RELAYS);
  if (m) {
    return [5, m[2] - 0, discipline];
  }

  // track last, so '100' doesn't match before '100H'
  m = discipline.match(PAT_TRACK);
  if (m) {
    return [1, m[1] - 0, discipline];
  }

  // anything else sorts to end
  return [6, 0, discipline];
}

function pad(n, width, z) {
  z = z || "0";
  n = n + "";
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function text_discipline_sort_key(discipline) {
  // Return a text version of the event_sort_key
  const k = discipline_sort_key(discipline);
  return k[0] + "_" + pad(k[1], 5) + "_" + k[2];
}

function sort_by_discipline(stuff, attr) {
  // Sort dicts or objects into the normal athletics order
  attr = attr || "discipline";
  var sorter = stuff.map(e => [text_discipline_sort_key(e[attr]), e]);
  sorter.sort();
  return sorter.map(e => e[1]);
}

function getDistance(discipline) {
  // Return approx distance in metres, for sanity checking
  // :param discipline:

  // Ignore final words like ' road'
  discipline = discipline.split(' ')[0];
  if (discipline === "XC") {
    return null;
  } else if (discipline === 'MAR') {
    return 42195;
  } else if (discipline === "HM") {
    return 21098;
  } else if (discipline === "MILE" || discipline === "CHUNDER-MILE") {
    return 1609;
  }

  var m = discipline.match(PAT_RELAYS);
  if (m) {
    var g2 = m[2].toUpperCase();
    if (g2 === 'RELAY') {
      return null; // cowardly refusing to guess
    }
    return parseInt(m[1], 10)*parseInt(g2, 10); // will be NaN if bad stuff
  }

  m = discipline.match(PAT_LEADING_FLOAT);
  if (!m) {
    m = discipline.match(PAT_LEADING_DIGITS);
  }
  if (!m) {
    return null;
  }

  var qty_text = m[0];
  var remains = discipline.slice(qty_text.length);
  var qty = parseFloat(qty_text);
  if (qty_text.match(/\./)) {
    return remains.match(/^(?:M|Mi|MI)$/) ? parseInt(1609 * qty, 10) : null;
  } else if (! remains) {
    return parseInt(qty, 10);
  } else if (remains.toLowerCase().match(/^(?:sc|h|w)$/) || remains.match(/^(?:m|mH)$/)) {
    return parseInt(qty, 10);
  } else if (remains.match(/^(?:k|K|km)$/)) {
    return parseInt(1000*qty, 10);
  } else if (remains.toLowerCase().match(/^(?:kw|kmw)$/)) {
    return parseInt(1000*qty, 10);
  } else if (remains.match(/^(?:M|Mi|MI)$/)) {
    return parseInt(1609*qty, 10);
  } else if (remains.match(/^(?:Y|y|YD|yd)$/)) {
    return parseInt(0.9144*qty, 10);
  }
}

function formatSecondsAsTime(seconds, prec) {
  // convert seconds to a string formatted as hours:min:secs
  // :param seconds: floating point seconds
  // :param prec=0: precision for seconds
  // :returns formatted string:
  if (prec === undefined) prec = 0;
  var secs = parseInt(seconds, 10);
  var frac = seconds - secs;
  var mins = parseInt(secs/60, 10);
  secs = secs - 60*mins;
  const hours = parseInt(mins/60, 10);
  mins = mins - 60*hours;


  if (prec === 0) frac = '';
  else if (prec === 1 || prec === 2 || prec === 3) frac = frac.toFixed(prec).slice(1);
  else {
    throw new Error("prec parameter should be 0, 1, 2 or 3 not '"+prec+"'");
  }
  var t;
  if (hours) t = [hours+'', pad(mins, 2), pad(secs, 2)];
  else if (mins) t = [mins+'', pad(secs, 2)];
  else t = [secs + ''];
  return t.join(':') + frac
}

module.exports = {
  hello,
  normalizeGender,
  perfToFloat,
  isFieldEvent,
  isMultiEvent,
  betterPerformance,
  discipline_sort_key,
  pad,
  text_discipline_sort_key,
  sort_by_discipline,
  getDistance,
  formatSecondsAsTime
};
