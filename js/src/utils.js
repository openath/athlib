import {
  JUMPS,
  THROWS,
  MULTI_EVENTS,
  FIELD_EVENTS,
} from './codes.js'

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
  return `Hello, ${arg}!`
}

/** Takes common gender expressions and returns `m` or `f` */
function normalizeGender(gender) {
  const g = gender.toLowerCase();
  if (g.len === 0) {
    throw new Error('this is an error that I am throwing');
  }
  if (/[mf]/.test(g[0])) {
    return g[0];
  }
  throw new Error('this is another error');
}

/** Trim and uppercase an event code */
function normalizeEventCode(eventCode) {
  return eventCode.trim().toUpperCase()
}

/** convert a performance (time or distance) to seconds or metres */
function perfToFloat(perfText) {
  const parts = perfText.split(/:/).reverse()
  let mult = 1
  let out = 0.0
  for (const part of parts) {
    out += (parseFloat(part) * mult)
    mult = mult * 60.0
  }
  return out
}

/** is this a field event code?  HJ, PV, TJ, LJ etc */
function isFieldEvent(eventCode) {
  const firstTwo = normalizeEventCode(eventCode).slice(0, 2)
  return (FIELD_EVENTS.indexOf(firstTwo) > -1)
}

/** is this a multi-event code?  DEC, PEN, HEP etc */
function isMultiEvent(eventCode) {
  const firstThree = normalizeEventCode(eventCode).slice(0, 3)
  return (MULTI_EVENTS.indexOf(firstThree) > -1)
}


/** return the better of two performance strings. 
 * For running events, lower times are better
 * For field events, greater numbers are better
 */
function betterPerformance(perfA, perfB, eventCode) {
  const fA = perfToFloat(perfA)
  const fB = perfToFloat(perfB)
  let better
  if (isFieldEvent(eventCode) || isMultiEvent(eventCode)) {
    better = (fA > fB) ? perfA : perfB // further is better
  } else {
    better = (fA < fB) ? perfA : perfB // faster is better
  }
  return better
}

export default { hello, normalizeGender, perfToFloat, isFieldEvent, isMultiEvent, betterPerformance }
