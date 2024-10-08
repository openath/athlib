import {
  FIELD_EVENTS,
  FIELD_SORT_ORDER,
  MULTI_EVENTS,
  PAT_HURDLES,
  PAT_JUMPS,
  PAT_RELAYS,
  PAT_THROWS,
  PAT_TRACK,
  PAT_LEADING_FLOAT,
  PAT_LEADING_DIGITS,
  PAT_EVENT_CODE,
  PAT_PERF,
  FIELD_EVENT_RECORDS_BY_GENDER,
  codesmap,
  PAT_RACES_FOR_DISTANCE
} from './patterns.js';

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

/** Takes common gender expressions and returns 'm' or 'f' */
function normalizeGender(gender) {
  if (typeof gender !== 'string') throw new Error(`cannot normalizeGender(${gender})`);

  const g = gender.trim().toUpperCase();

  if (g.length >= 1 && /[MF]/.test(g[0])) {
    return g[0];
  }
  throw new Error(`cannot normalize gender for "${gender}"`);
}

/** Trim and uppercase an event code */
function _normalizeEventCode(eventCode) {
  return eventCode.trim().toUpperCase();
}

/** convert a performance (time or distance) to seconds or metres */
function perfToFloat(perfText) {
  const parts = perfText.split(/:/).reverse();
  let mult = 1;
  let out = 0.0;
  let i = 1;
  const n = parts.length;

  for (i = 0;i < n;i++) {
    out += parseFloat(parts[i]) * mult;
    mult *= 60.0;
  }
  return out;
}

/** is this a field event code?  HJ, PV, TJ, LJ etc */
function isFieldEvent(eventCode) {
  const firstTwo = _normalizeEventCode(eventCode).slice(0, 2);

  return FIELD_EVENTS.indexOf(firstTwo) > -1;
}

/** is this a multi-event code?  DEC, PEN, HEP etc */
function isMultiEvent(eventCode) {
  const firstThree = _normalizeEventCode(eventCode).slice(0, 3);

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
  var m;

  // Return a tuple which will sort into programme order
  // Track should be ordered by distance.
  if (!discipline) {
    // Goes at the end
    return [6, 0, '?'];
  }

  discipline = discipline.trim();

  m = discipline.match(PAT_THROWS);
  if (m) {
    m = FIELD_SORT_ORDER.indexOf(discipline.slice(0, 3).toUpperCase());
    if (m < 0) m = FIELD_SORT_ORDER.indexOf(discipline.slice(0, 2).toUpperCase());
    return [ 4, m, discipline ];
  }

  m = discipline.match(PAT_HURDLES);
  if (m) {
    return [2, m[1] - 0, discipline];
  }

  m = discipline.match(PAT_JUMPS);
  if (m) {
    m = FIELD_SORT_ORDER.indexOf(discipline.slice(0, 3).toUpperCase());
    if (m < 0) m = FIELD_SORT_ORDER.indexOf(discipline.slice(0, 2).toUpperCase());
    return [ 3, m, discipline ];
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
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function text_discipline_sort_key(discipline) {
  // Return a text version of the event_sort_key
  const k = discipline_sort_key(discipline);

  return k[0] + '_' + pad(k[1], 5) + '_' + k[2];
}

function sort_by_discipline(stuff, attr) {
  var sorter;

  // Sort dicts or objects into the normal athletics order
  attr = attr || 'discipline';
  sorter = stuff.map((e) => [text_discipline_sort_key(e[attr]), e]);

  sorter.sort();
  return sorter.map((e) => e[1]);
}

function getDistance(discipline) {
  var m;
  var g2;
  var qtyText;
  var remains;
  var qty;

  // Return approx distance in metres, for sanity checking
  // :param discipline:

  // Ignore final words like ' road'
  discipline = discipline.split(' ')[0];
  if (discipline === 'XC') {
    return null;
  } else if (discipline === 'MAR') {
    return 42195;
  } else if (discipline === 'HM') {
    return 21098;
  } else if (discipline === 'MILE' || discipline === 'CHUNDER-MILE') {
    return 1609;
  }

  m = discipline.match(PAT_RELAYS);

  if (m) {
    g2 = m[2].toUpperCase();

    if (g2 === 'RELAY' || g2 === 'DMR' || g2 === 'SMR') {
      return null; // cowardly refusing to guess
    }
    return parseInt(m[1], 10) * parseInt(g2, 10); // will be NaN if bad stuff
  }

  m = discipline.match(PAT_LEADING_FLOAT);
  if (!m) {
    m = discipline.match(PAT_LEADING_DIGITS);
  }
  if (!m) {
    return null;
  }

  qtyText = m[0];
  remains = discipline.slice(qtyText.length);
  qty = parseFloat(qtyText);

  if (!remains) {
    return parseInt(qty, 10);
  } else if (remains.toLowerCase().match(/^(?:sc|h|w)$/) || remains.match(/^(?:m|mH)$/)) {
    return parseInt(qty, 10);
  } else if (remains.match(/^(?:k|K|km)$/)) {
    return parseInt(1000 * qty, 10);
  } else if (remains.toLowerCase().match(/^(?:kw|kmw)$/)) {
    return parseInt(1000 * qty, 10);
  } else if (remains.match(/^(?:M|Mi|MI)$/)) {
    return parseInt(1609 * qty, 10);
  } else if (remains.match(/^(?:Y|y|YD|yd)$/)) {
    return parseInt(0.9144 * qty, 10);
  }
  return null;
}

function getDurationEventTime(dev) {
  var m, t;

  dev = dev.replace(/\s/g, '');
  m = dev.match(PAT_RACES_FOR_DISTANCE);
  if (!m) return null;
  t = codesmap(PAT_RACES_FOR_DISTANCE, 'dhours', m);
  if (t) return (t - 0) * 3600;
  return (codesmap(PAT_RACES_FOR_DISTANCE, 'dmins', m) - 0) * 60;
}

function roundUpStrNum(s, prec, maxDP) {
  // s is a valid non-negative float number string containing possible .xyz
  // returns string number rounded up to prec places

  // anything after the maxDP'th place is considered to be noise and is not considered
  var i, f, t, n;

  if (typeof prec === 'undefined') prec = 2;
  if (typeof maxDP === 'undefined') maxDP = 5;

  if (s.indexOf('.') < 0) {
    i = s;
    f = pad('', prec);
  } else {
    f = s.split('.', 2);
    i = f[0];
    f = f[1].slice(0, maxDP);
  }
  n = f.length;
  if (n > prec) {
    t = f.slice(prec);
    f = f.slice(0, prec);
    while (t.length && t.startsWith('0')) t = t.slice(1); // t.lstrip('0')
    if (t.length) {
      i += f;
      i = i ? '' + ((i - 0) + 1) : '1';
      n = i.length - prec;
      if (n < 1) {
        i = pad('', (1 - n)) + i;
        n = 1;
      }
      f = i.slice(-prec);
      i = i.slice(0, n);
    }
  } else {
    if (n < prec) f += pad('', prec - n);
    if (!i) i = '0';
  }
  return prec ? [i, f].join('.') : i;
}

function formatSecondsAsTime(seconds, prec) {
  var t;
  var secs;
  var frac;
  var mins;
  var hours;

  // convert non-negative seconds to a string formatted as hours:min:secs
  // fractional seconds are rounded up to prec digits eg
  // format_seconds_as_time(3599.1, prec=0) == 1:00:00
  //
  // :param seconds: non-negative floating point seconds
  // :param prec=0: precision for seconds
  // :returns formatted string:
  if (prec === undefined) prec = 0;

  if (prec === 0 || prec === 1 || prec === 2 || prec === 3) {
    secs = parseInt(seconds, 10);
    frac = Math.max(seconds - secs, 0);
    mins = parseInt(secs / 60, 10);
    secs -= 60 * mins;
    hours = parseInt(mins / 60, 10);
    mins -= 60 * hours;
    frac = roundUpStrNum('' + frac, prec);
    t = frac.substr(0, 1);
    frac = frac.slice(1);
    if (t !== '0') {
      secs += 1;
      if (secs === 60) {
        secs = 0;
        mins += 1;
        if (mins === 60) {
          mins = 0;
          hours += 1;
        }
      }
    }
  } else {
    throw new Error("prec parameter should be 0, 1, 2 or 3 not '" + prec + "'");
  }

  if (hours) t = [hours + '', pad(mins, 2), pad(secs, 2)];
  else if (mins) t = [mins + '', pad(secs, 2)];
  else t = [secs + ''];
  return t.join(':') + frac;
}

function str2num(s) {
  // convert string to int if possible else float
  const f = Number(s);

  if (isNaN(f)) throw Error(`Invalid input ${s} to str2num`);
  return s.indexOf('.') >= 0 ? parseFloat(s) : parseInt(s, 10);
}

function parseHms(t) {
  var sep;
  var sec;
  var s;
  var i;

  // Parse a time duration with 0, 1 or 2 colons and return seconds.
  if (typeof t === 'number') return t;

  // Try : and ; separators
  for (sep in { ':': null, ';': null }) {
    if (t.indexOf(sep) === -1) continue;
    const S = t.split(sep);

    for (i = sec = 0; i < S.length; i++) {
      s = S[i];
      sec *= 60;

      try {
        sec += str2num(s);
      } catch (e) {
        throw Error('cannot parse component ' + s + ' from ' + t);
      }
    }
    return sec;
  }
  try {
    return str2num(t);
  } catch (e) {
    throw Error('cannot parse seconds from ' + t);
  }
}

function checkEventCode(c) {
  return c.match(PAT_EVENT_CODE);
}

function invertKeyValues(obj, options) {
  // invert { key0: val0, key1: val1,....}
  // default assumes unique mapping
  const fn = (options || {}).fn;
  const uniq = (options || {}).uniq || true;
  var val;

  return Object.keys(obj).reduce(function (acc, key) {
    val = obj[key];
    if (fn) val = fn(val);
    if (uniq) {
      acc[val] = key;
    } else {
      acc[val] = acc[val] || [];
      acc[val].push(key);
    }
    return acc;
  }, {});
}

// returns an array containing non-trivial captures
function regexCaptures(pat, s) {
  const A = pat.exec(s);
  var R, n, ss, sst, i;

  if (A !== null) {
    R = [];
    n = (Object.keys(A).length - 3);

    for (i = 1; i < n; i++) { // avoid full result
      ss = A[i];

      if (ss != null) {
        sst = ss.trim();

        if (sst !== '') {
          const start = s.indexOf(ss);
          const end = start + ss.length;

          R[i] = [start, end, sst];
        }
      }
    }
  }
  return R;
}

function _normTZeroes(s) {
  s = s.trim();
  if (s.indexOf('.') >= 0) {
    while (s.length && s.slice(-1).match(/[' .0']/)) s = s.slice(0, -1);
  }
  return s;
}

function _normCM(s) {
  return _normTZeroes(s.slice(0, -2)) + 'cm';
}

function _normm(s) {
  while (s.slice(-1).match(/[ m]/)) s = s.slice(0, -1);
  return _normTZeroes(s) + 'm';
}

function _normgKg(s) {
  while (s.slice(-1).match(/[ g]/)) s = s.slice(0, -1);
  while (s.slice(-1).match(/[ kK]/)) s = s.slice(0, -1);
  return _normTZeroes(s) + 'K';
}

function _normg(s) {
  while (s.slice(-1).match(/[ g]/)) s = s.slice(0, -1);
  return _normTZeroes(s);
}

var _gnorms = { // eslint-disable-line vars-on-top
  jtnum: _normg, hhh: _normCM, hsd: _normm, hid: _normm, dtnum: _normgKg,
  htnum: _normgKg, spnum: _normgKg, swtnum: _normgKg,
  btnum: _normgKg, stnum: _normgKg, gdtnum: _normgKg, otnum: _normg
};

function normalizeEventCode(c) {
  var m, n, ign, k, i, v, start, end, gnr;

  c = c.trim();
  m = regexCaptures(PAT_EVENT_CODE, c);

  if (!m) {
    throw new Error(`cannot normalize event code ${c}`);
  } else {
    n = c.match(PAT_RELAYS);
    if (n) {
      c = n[1] + 'x' + n[2].toUpperCase();
    } else {
      n = m.length;
      ign = invertKeyValues(codesmap(PAT_EVENT_CODE));

      c = c.toUpperCase();

      for (i = n - 1; i > 0; i--) { // move backwards through the captures
        k = ign[i];

        if (k != null && (gnr = _gnorms[k]) != null) {
          v = m[i];
          if (v == null) continue;

          start = v[0];
          end = v[1];

          v = v[2];
          c = c.slice(0, start) + gnr(v) + c.slice(end);
        }
      }
    }
    return c.replace(/\s/g, '');
  }
}

function fieldEventRecord(evc, gender) {
  var R;

  if (!gender) R = FIELD_EVENT_RECORDS_BY_GENDER.all;
  else {
    R = FIELD_EVENT_RECORDS_BY_GENDER[gender.toLowerCase()];
    if (R === undefined) R = FIELD_EVENT_RECORDS_BY_GENDER.all;
  }
  const r = R[evc.toUpperCase()];

  return (r === undefined) ? null : r;
}

function checkPerformanceForDiscipline(discipline, textvalue, gender, ulpc, errorKlass, prec) {
  var distance;
  var record;
  var points;
  var chunks;
  var hours;
  var minutes;
  var seconds;
  var t;
  var duration;
  var velocity;

  if (gender === undefined) gender = 'all';
  if (ulpc === undefined) ulpc = 1.2;
  if (errorKlass === undefined) errorKlass = Error;
  if (prec === undefined) prec = null;
  // Fix up and return what they typed in,    or raise errorKlass(default ValueError)
  textvalue = textvalue.trim();

  if (discipline.toLowerCase() === 'xc' && textvalue === '') return textvalue;

  //  fix up "," for the Frenchies
  if (textvalue.indexOf(',') >= 0 && textvalue.indexOf('.') === -1) textvalue = textvalue.replace(',', '.');
  if (textvalue. indexOf(';') >= 0) textvalue = textvalue.replace(';', ':');
  if (!textvalue.match(PAT_PERF)) throw errorKlass("Illegal numeric pattern.  Use digits, ':' and '.' only");

  if (isFieldEvent(discipline)) {
    distance = Number(textvalue);
    if (isNaN(distance)) {
      throw errorKlass(`${textvalue} is not valid for length/height. Use metres/centimetres e.g. '2.34'`);
    } else {
      record = fieldEventRecord(discipline, gender);
      if (record && distance > record * ulpc) {
        throw errorKlass(`${discipline}(${gender}) performance ${textvalue} seems too large as record is ${record}`);
      }
      return distance.toFixed(2);
    }
  } else if (MULTI_EVENTS.indexOf(discipline.toUpperCase()) >= 0) {
    points = Number(textvalue);

    if (isNaN(points)) throw errorKlass(`${textvalue} is not a valid points value for multi-events`);
    if (points > 9999) throw errorKlass(`Multi-events scores should be below 10000 not ${textvalue}`);
    return points + '';
  } else {
    //    It's a running distance.  format check.  Try to extract metres
    distance = getDistance(discipline);

    if (textvalue.startsWith('0:')) textvalue = textvalue.slice(2);
    if (textvalue.startsWith('00:')) textvalue = textvalue.slice(3);
    if (distance && (distance <= 200) && textvalue.indexOf(':') >= 0 &&
      textvalue.indexOf('.') < 0) textvalue = textvalue.replace(':', '.');
    if (distance && (distance >= 800) && textvalue.indexOf('.') >= 0 &&
      textvalue.indexOf(':') < 0) textvalue = textvalue.replace('.', ':');

    if (['800', '1500', '3000'].indexOf(discipline) >= 0) {
      if (textvalue.indexOf('.') < 0) {
        chunks = textvalue.split(':');
        if (chunks.length === 3) {textvalue = chunks[0] + ':' + chunks[1] + '.' + chunks[2];}
        // we got hours/mins/secs, should have been min/sec+fraction
      }
    }

    chunks = textvalue.split(':');

    //    The regex ensures we have 1, 2 or 3 chunks
    if (chunks.length === 1) {
      hours = 0;
      minutes = 0;
      seconds = parseFloat(chunks[0], 10);
    } else if (chunks.length === 2) {
      hours = 0;
      minutes = parseInt(chunks[0], 10);
      seconds = parseFloat(chunks[1], 10);
    } else if (chunks.length === 3) {
      hours = parseInt(chunks[0], 10);
      minutes = parseInt(chunks[1], 10);
      seconds = parseFloat(chunks[2], 10);
    }

    if (minutes === 0 && seconds >= 100) {
      throw errorKlass(`Please use mm:ss or h:mm:ss for times above 99 seconds not ${textvalue}`);
    }

    if (distance === 400 && minutes > 45) {
      // 63:40 instead of 63.40
      seconds = minutes + 0.01 * seconds;
      hours = 0;
      minutes = 0;
    }

    duration = 3600 * hours + 60 * minutes + seconds;
    //    print("duration: %0.2f seconds" % duration)

    //    do sanity checks.  Over 11 metres per second is pretty fishy for a
    //    sprint
    if (distance > 0 && duration > 0) {
      velocity = distance * 1.0 / duration;

      if (distance <= 400) {
        if (velocity > 11.0) throw errorKlass(`${textvalue} too fast for ${discipline}, check the format`);
      } else if (distance > 400) {
        if (velocity > 10.0) throw errorKlass(`${textvalue} too fast for ${discipline}, check the format`);
      }
      if (velocity < 0.5) throw errorKlass(`${textvalue} too slow for ${discipline}, check the format`);
    } else {
      if (discipline.toUpperCase() === 'XC' && minutes === 0) {
        throw errorKlass(`Please use mm:ss for minutes and seconds, not mm.ss (entered ${textvalue})`);
      }
    }

    if (prec === null) {
      // use Andy's method
      // Format consistently for output
      if (hours > 0) {
        t = parseInt(seconds, 10);
        t = [hours + '', pad(minutes, 2), pad(t, 2) + (seconds - t).toFixed(2).slice(1)].join(':');
      } else if (minutes > 0) {
        t = parseInt(seconds, 10);
        t = [minutes + '', pad(t, 2) + (seconds - t).toFixed(2).slice(1)].join(':');
      } else {
        t = seconds.toFixed(2);
      }

      //  Strip trailing zeroes except for short ones
      if (t.length > 5) {
        while (t.endsWith('0') && t.length > 4) t = t.slice(0, -1);
        if (t.endsWith('.')) t = t.slice(0, -1);
      }
      return t;
    }
    return formatSecondsAsTime(duration, prec);
  }
}

// direct copy of utils.py
function isHandTiming(perf) {
  var dp;

  if (typeof perf === 'number') return false;

  dp = perf.lastIndexOf('.');
  return dp < 0 || (perf.length - dp) < 3;
}

function zip(arrays) {
  return arrays[0].map(function (_, i) {
    return arrays.map(function (array) {return array[i];});
  });
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
  roundUpStrNum,
  formatSecondsAsTime,
  parseHms,
  str2num,
  checkEventCode,
  invertKeyValues,
  regexCaptures,
  normalizeEventCode,
  fieldEventRecord,
  checkPerformanceForDiscipline,
  isHandTiming,
  getDurationEventTime,
  zip
};
