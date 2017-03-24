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

function isFieldEvent(eventCode) {
  const FIELD_PREFIXES = ['HJ', 'PV', 'LJ', 'TJ', 'SP', 'DT', 'JT', 'HT', 'WT']
  const firstTwo = eventCode.slice(0, 2)
  return (FIELD_PREFIXES.indexOf(firstTwo) > -1)
}

/** return the better of two performance strings */
function betterPerformance(perfA, perfB, eventCode) {
  const fA = perfToFloat(perfA)
  const fB = perfToFloat(perfB)
  let better
  if (isFieldEvent(eventCode)) {
    better = (fA > fB) ? perfA : perfB  // further is better
  } else {
    better = (fA < fB) ? perfA : perfB  // faster is better
  }
  return better
}
module.exports = { 
  hello, 
  normalizeGender, 
  perfToFloat, 
  isFieldEvent,
  betterPerformance,
}