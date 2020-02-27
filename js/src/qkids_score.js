// direct copy of qkids_score.py
import {
  normalizeEventCode,
  parseHms
} from './utils.js';
import {
  PAT_RUN
} from './patterns.js';

// start qkids tables created by qkids-process.py Thu Feb 27 16:47:32 2020
/* eslint-disable */
var _qkidsTables = {
  'QKWL': {
    '75': [0.1, 16.0, 7.0],
    '600': [1, 180, 90],
    'LJ': [0.03, 2.2, 4.9],
    'OT': [0.5, 5.0, 50.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKWLU13': {
    '70H': [0.1, 20.0, 11.0],
    '800': [1, 230, 140],
    'LJ': [0.04, 2.0, 5.6],
    'SP': [0.1, 2.0, 11.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKSEC': {
    '100': [0.1, 19.5, 10.5],
    '800': [1, 230, 140],
    'LJ': [0.05, 2.0, 6.5],
    'OT': [0.6, 6.0, 60.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKPRI': {
    '75': [0.1, 16.0, 7.0],
    '600': [1, 180, 90],
    'SLJ': [0.02, 1.02, 2.82],
    'OT': [0.5, 5.0, 50.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKSTA': {
    '50': [0.1, 12.0, 3.0],
    '400': [1, 125, 35],
    'SLJ': [0.03, 0.75, 3.0],
    'OT': [0.5, 2.5, 47.5],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKCLUB': {
    '75': [0.1, 16.0, 7.0],
    '600': [1, 180, 90],
    'LJ': [0.03, 2.2, 4.9],
    'OT': [0.5, 5.0, 50.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKCLU13': {
    '100': [0.1, 19.5, 10.5],
    '800': [1, 230, 140],
    'LJ': [0.05, 2.0, 6.5],
    'OT': [0.6, 6.0, 60.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKCLU9': {
    '50': [0.1, 12.0, 3.0],
    '400': [1, 130, 40],
    'SLJ': [0.02, 0.9, 2.7],
    'OT': [0.5, 0.0, 45.0],
    '4x100': [0.5, 94.0, 49.0]
    },
  'QKPRE': {
    '50': [0.1, 13.0, 4.0],
    '300': [1, 135, 45],
    'SLJ': [0.03, 0.5, 3.2],
    'OT': [0.5, 0.0, 45.0],
    '4x100': [0.5, 99.0, 54.0]
    }
  };
 _qkidsTables['QKWLU13']['75H'] = _qkidsTables['QKWLU13']['70H'];
var _compTypeMap = {'WESSEXLEAGUE': 'QKWL', 'WESSEXLEAGUE(U13)': 'QKWLU13',
  'QUADKIDSSECONDARY': 'QKSEC', 'QUADKIDSPRIMARY': 'QKPRI',
  'QUADKIDSSTART': 'QKSTA', 'QUADKIDSCLUB': 'QKCLUB',
  'QUADKIDSCLUBU13': 'QKCLU13', 'QUADKIDSCLUBU9': 'QKCLU9',
  'QUADKIDSPRE-START': 'QKPRE'};
/* eslint-enable */
// end qkids tables

function qkidsScore(competitionType, event, perf) {
  var table, v, row, delta;

  competitionType = competitionType.replace(/\s/g, '').toUpperCase();
  if (_compTypeMap.hasOwnProperty(competitionType)) {
    competitionType = _compTypeMap[competitionType];
  }
  table = _qkidsTables[competitionType];
  if (!table) {
    throw new Error(`cannot find QuadKids Table for competition type ${competitionType}`);
  }
  event = normalizeEventCode(event);
  row = table[event];
  if (!row) {
    throw new Error(`cannot find find data for QuadKids Table[${competitionType}][${event}]`);
  }
  v = event.match(PAT_RUN);
  delta = v ? (row[1] - parseHms(perf)) : ((perf - 0) - row[1]);
  v = parseInt(1e-6 + delta / row[0] + 10, 10);
  return Math.max(10, Math.min(v, 100));
}

module.exports = { qkidsScore };
