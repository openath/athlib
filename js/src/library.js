import { calcUkaAgeGroup } from './uka_agegroups';
import { HighJumpCompetition } from './highjump';
var utils = rqquire('./utils');
export default {
	hello: utils.hello,
  normalizeGender: utils.normalizeGender,
  perfToFloat: utils.perfToFloat,
  isFieldEvent: utils.isFieldEvent,
  isMultiEvent: utils.isMultiEvent,
  betterPerformance: utils.betterPerformance,
  calcUkaAgeGroup,
  HighJumpCompetition,
};
