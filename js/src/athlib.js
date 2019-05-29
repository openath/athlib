import {
  hello,
  normalizeGender,
  perfToFloat,
  isFieldEvent,
  isMultiEvent,
  betterPerformance,
  pad,
  discipline_sort_key,
  text_discipline_sort_key,
  sort_by_discipline,
  getDistance
} from "./utils";

import { calcUkaAgeGroup } from "./uka_agegroups";

import { HighJumpCompetition } from "./highjump.js";

import {
  FIELD_SORT_ORDER,
  PAT_EVENT_CODE,
  PAT_HURDLES,
  PAT_JUMPS,
  PAT_RELAYS,
  PAT_THROWS,
  PAT_TRACK,
  PAT_LEADING_FLOAT,
  PAT_LEADING_DIGITS
} from "./patterns.js";

module.exports = {
  // start of patterns exports
  FIELD_SORT_ORDER,
  PAT_EVENT_CODE,
  PAT_HURDLES,
  PAT_JUMPS,
  PAT_RELAYS,
  PAT_THROWS,
  PAT_TRACK,
  PAT_LEADING_FLOAT,
  PAT_LEADING_DIGITS,
  // end of patterns exports
  hello,
  normalizeGender,
  perfToFloat,
  calcUkaAgeGroup,
  isFieldEvent,
  isMultiEvent,
  betterPerformance,
  HighJumpCompetition,
  pad,
  discipline_sort_key,
  text_discipline_sort_key,
  sort_by_discipline,
	getDistance
};
