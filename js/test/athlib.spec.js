var Athlib = process.env.TESTSRC;
Athlib = Athlib==='src' ? '../src/athlib.js' : (Athlib==='dist' ? '../dist/athlib.web.js' : '../lib/athlib.js');
if(process.env.DEBUG=='1') console.log('!!!!! athlib.spec.js require("'+Athlib+'")');
Athlib = require(Athlib);

describe('Given an instance of Athlib', () => {
  describe('testing the hello function', () => {
    test('hello("world") should return "Hello, world!"', () => {
      expect(Athlib.hello('world')).toEqual('Hello, world!');
    });
  });
  describe('testing normalizeGender', () => {
    test('Male should return M', () => {
      expect(Athlib.normalizeGender('Male')).toEqual('m');
      expect(Athlib.normalizeGender('FeMale')).toEqual('f');
    });
  });
  describe('testing UKA age groups', () => {
    test('should return SEN for TF', () => {
      expect(Athlib.calcUkaAgeGroup(
        new Date('1989-01-26'),
        new Date('2017-01-01'),
        'TF',
        false,
        false)).toEqual('SEN');
    });
    test('should return SEN for XC', () => {
      expect(Athlib.calcUkaAgeGroup(
        new Date('1989-01-26'),
        new Date('2017-01-01'),
        'XC',
        false,
        false)).toEqual('SEN');
    });
  });

  describe('perfToFloat', () => {
    test('should parse performances', () => {
      expect(Athlib.perfToFloat('1:57.2')).toEqual(117.2);
      expect(Athlib.perfToFloat('9.58')).toEqual(9.58);
      expect(Athlib.perfToFloat('63.2')).toEqual(63.2);
      expect(Athlib.perfToFloat('1:03.2')).toEqual(63.2);
      expect(Athlib.perfToFloat('2:03:59.1')).toEqual(7439.10);
    });
  });

  describe('isFieldEvent', () => {
    test('should detect field events', () => {
      expect(Athlib.isFieldEvent('JT')).toEqual(true);
      expect(Athlib.isFieldEvent('JT700')).toEqual(true);
      expect(Athlib.isFieldEvent('800')).toEqual(false);
      expect(Athlib.isMultiEvent('PEN')).toEqual(true);
      expect(Athlib.isMultiEvent(' heptathalon ')).toEqual(true);
      expect(Athlib.isMultiEvent('Decy')).toEqual(true);
      expect(Athlib.isMultiEvent('Octa')).toEqual(true);
    });
  });

  describe('betterPerformance', () => {
    test('should detect better performances', () => {
      expect(Athlib.betterPerformance('83.25', '17.3', 'JT')).toEqual('83.25');
      expect(Athlib.betterPerformance('10.5', '10.6', '100')).toEqual('10.5');
      expect(Athlib.betterPerformance('3456', '4567', 'DEC')).toEqual('4567');
      expect(Athlib.betterPerformance('3456', '4567', 'MUL')).toEqual('4567');
    });
  });

  describe('checkPatternsDefined', () => {
    test('should see if patterns are defined', () => {
      expect(Athlib.FIELD_SORT_ORDER).toBeDefined();
      expect(Athlib.PAT_HURDLES).toBeDefined();
      expect(Athlib.PAT_RELAYS).toBeDefined();
      expect(Athlib.PAT_JUMPS).toBeDefined();
      expect(Athlib.PAT_THROWS).toBeDefined();
      expect(Athlib.PAT_TRACK).toBeDefined();
      expect(Athlib.PAT_EVENT_CODE).toBeDefined();
    });
  });

  describe('discipline_sort_key', () => {
    test('should see if event ordering will work', () => {
      expect(Athlib.discipline_sort_key('')).toEqual([6, 0, "?"]);
      expect(Athlib.discipline_sort_key('HJ')).toEqual([3, 0, "HJ"]);
      expect(Athlib.discipline_sort_key('LJ')).toEqual([3, 2, "LJ"]);
      expect(Athlib.discipline_sort_key('PV')).toEqual([3, 1, "PV"]);
      expect(Athlib.discipline_sort_key('100')).toEqual([1, 100, "100"]);
      expect(Athlib.discipline_sort_key('4x400')).toEqual([5, 400, "4x400"]);
      expect(Athlib.discipline_sort_key('JT')).toEqual([4, 7, "JT"]);
      expect(Athlib.discipline_sort_key('200H')).toEqual([2, 200, "200H"]);
    });
  });

  describe('text_discipline_sort_key', () => {
    test('should see if event ordering will work', () => {
      expect(Athlib.text_discipline_sort_key('')).toEqual("6_00000_?");
      expect(Athlib.text_discipline_sort_key('HJ')).toEqual("3_00000_HJ");
      expect(Athlib.text_discipline_sort_key('LJ')).toEqual("3_00002_LJ");
      expect(Athlib.text_discipline_sort_key('PV')).toEqual("3_00001_PV");
      expect(Athlib.text_discipline_sort_key('100')).toEqual("1_00100_100");
      expect(Athlib.text_discipline_sort_key('4x400')).toEqual("5_00400_4x400");
      expect(Athlib.text_discipline_sort_key('JT')).toEqual("4_00007_JT");
      expect(Athlib.text_discipline_sort_key('200H')).toEqual("2_00200_200H");
    });
  });
  describe('sort_by_discipline', () => {
    test('sort a list of pseudo-events', () => {
      const events = [
        {e:'',a:60},
        {e:'HJ',a:30},
        {e:'LJ',a:32},
        {e:'PV',a:31},
        {e:'100',a:1100},
        {e:'800',a:1800},
        {e:'4x400',a:5400},
        {e:'JT',a:47},
        {e:'200H',a:2200},
      ];
      const sorted = Athlib.sort_by_discipline(events,'e').map(x => x.a);
      expect(sorted).toEqual([1100,1800,2200,30,31,32,47,5400,60]);
    });
  });

});
