import { expect } from 'chai';
import Athlib from '../index.js';

describe('Given an instance of Athlib', function() {
    describe('testing the hello function', function() {
        it('hello("world") should return "Hello, world!"', () => {
            expect(Athlib.hello('world')).to.be.equal('Hello, world!');
        });
    });
    describe('testing normalizeGender', function() {
        it('Male should return M', () => {
            expect(Athlib.normalizeGender('Male')).to.be.equal('m');
            expect(Athlib.normalizeGender('FeMale')).to.be.equal('f');
        });
    });
    describe('testing UKA age groups', function() {
        it('should return SEN for TF', function() {
            expect(Athlib.calcUkaAgeGroup(
                new Date('1989-01-26'),
                new Date('2017-01-01'),
                'TF',
                false,
                false)).to.equal('SEN');
        });
        it('should return SEN for XC', function() {
            expect(Athlib.calcUkaAgeGroup(
                new Date('1989-01-26'),
                new Date('2017-01-01'),
                'XC',
                false,
                false)).to.equal('SEN');
        });
    });

    describe('perfToFloat', function() {
        it('should parse performances', function() {
            expect(Athlib.perfToFloat('1:57.2')).to.equal(117.2);
            expect(Athlib.perfToFloat('9.58')).to.equal(9.58);
            expect(Athlib.perfToFloat('63.2')).to.equal(63.2);
            expect(Athlib.perfToFloat('1:03.2')).to.equal(63.2);
            expect(Athlib.perfToFloat('2:03:59.1')).to.equal(7439.10);
        });
    });

    describe('isFieldEvent', function() {
        it('should detect field events', function() {
            expect(Athlib.isFieldEvent('JT')).to.equal(true);
            expect(Athlib.isFieldEvent('JT700')).to.equal(true);
            expect(Athlib.isFieldEvent('800')).to.equal(false);
        });
    });
    describe('betterPerformance', function() {
        it('should detect better performances', function() {
            expect(Athlib.betterPerformance('83.25', '17.3', 'JT')).to.equal('83.25');
            expect(Athlib.betterPerformance('10.5', '10.6', '100')).to.equal('10.5');
        });
    });

});
