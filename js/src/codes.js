// 'Standard event codes, and things to parse and check them'
// patterns allow both for generic (JT = Javelin Throw) and specific (JT800) patterns.

const JUMPS = ['HJ', 'PV', 'LJ', 'TJ'];
const THROWS = ['SP', 'DT', 'JT', 'HT', 'WT'];
const MULTI_EVENTS = ['PEN', 'HEP', 'OCT', 'DEC', 'ICO', 'MUL'];
const FIELD_EVENTS = JUMPS.concat(THROWS);

module.exports = {
  JUMPS,
  THROWS,
  MULTI_EVENTS,
  FIELD_EVENTS
};
