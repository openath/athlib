// private function returns the number of years between two dates
function _calculateAge(birthDate, matchDate) {
  try {
    const ageDifMs = matchDate - birthDate.getTime();
    const ageDate = new Date(ageDifMs); // miliseconds from epoch

    return ageDate.getUTCFullYear() - 1970;
  } catch (error) {
    // throw the error again
    throw error;
  }
}

// rule107 Track and Field
function rule107tf(birthDate, matchDate, vets, underAge) {
  if (!(birthDate instanceof Date && matchDate instanceof Date)) {
    throw new TypeError('birthDate and matchDate must be DATE');
  }
  const augustCutOff = new Date(matchDate.getFullYear(), 7, 11);
  const decemberCutOff = new Date(matchDate.getFullYear(), 11, 31);
  const ageOn31Aug = _calculateAge(birthDate, augustCutOff);
  const ageOn31Dec = _calculateAge(birthDate, decemberCutOff);
  const ageOnMatchDate = _calculateAge(birthDate, matchDate);

  if (underAge && ageOn31Aug < 9) {
    return 'U9';
  }
  switch (true) {
    case ageOn31Aug < 11:
      return 'U11';
    case ageOn31Aug === 11 || ageOn31Aug === 12:
      return 'U13';
    case ageOn31Aug === 13 || ageOn31Aug === 14:
      return 'U15';
    case ageOn31Aug === 15 || ageOn31Aug === 16:
      return 'U17';
    case ageOn31Dec < 20:
      return 'U20';
    case ageOnMatchDate > 35 && vets:
      return 'V${(ageOn31MatchDay/5)*5}';
    default:
      return 'SEN';
  }
}

// rule507 Cross Country
function rule507xc(birthDate, matchDate, vets, underAge) {
  let birthDate2;
  let augCO = new Date();

  try {
    augCO = new Date(matchDate);
    if (typeof birthDate !== Date) {
      birthDate2 = new Date(birthDate);
    } else {
      birthDate2 = birthDate;
    }
  } catch (error) {
    // just throw it
    throw error;
  }
  const ageOn31Aug = _calculateAge(birthDate2, augCO);
  const ageOnMatchDate = _calculateAge(birthDate2, matchDate);

  if (underAge && ageOn31Aug < 9) {
    return 'U9';
  }
  switch (true) {
    case ageOnMatchDate < 11:
      return 'U11';
    case ageOn31Aug === 11 || ageOn31Aug === 12:
      return 'U13';
    case ageOn31Aug === 13 || ageOn31Aug === 14:
      return 'U15';
    case ageOn31Aug === 15 || ageOn31Aug === 16:
      return 'U17';
    case ageOn31Aug < 20:
      return 'U20';
    case ageOnMatchDate > 35 && vets:
      return 'V${(ageOn31MatchDay/5)*5}';
    default:
      return 'SEN';
  }
}

// function priorDate(matchDate, cutoffDate) {
//   try {
//     const md = new Date(matchDate);
//     const cd = new Date(cutoffDate);
//     const x = new Date(md.getFullYear(), cd.getMonth(), cd.getDay());
//     if (x > md) {
//       return new Date(md.getFullYear() - 1, cd.getMonth(), cd.getDay())
//     }
//   } catch (error) {
//     // just throw it again
//     throw error;
//   }
// }

/** Return the UK Athletics age group code for the athlete on match day */
function calcUkaAgeGroup(birthDate, matchDate, category, vets, underAge) {
  if (!(birthDate instanceof Date || matchDate instanceof Date)) {
    throw new Error('you must pass a valid date');
  }
  switch (category) {
    case 'TF':
      return rule107tf(birthDate, matchDate, vets || true, underAge || false);
    case 'ROAD': // same categories as cross country
    case 'XC':
      return rule507xc(birthDate, matchDate, vets || true, underAge || false);
    case 'ESAA':
      throw new Error('this has not been implemented');
    default:
      throw new Error('incorrect category');
  }
}

module.exports = { calcUkaAgeGroup };
