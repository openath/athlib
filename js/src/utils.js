import { MULTI_EVENTS, FIELD_EVENTS } from "./codes.js";
import {
  FIELD_SORT_ORDER,
  PAT_HURDLES,
  PAT_JUMPS,
  PAT_RELAYS,
  PAT_THROWS,
  PAT_TRACK
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
  attr = attr || "disicpline";
  var sorter = stuff.map(e => [text_discipline_sort_key(e[attr]), e]);
  sorter.sort();
  return sorter.map(e => e[1]);
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
  sort_by_discipline
};
