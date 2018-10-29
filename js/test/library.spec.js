import Athlib from '../src/library.js';


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

});
