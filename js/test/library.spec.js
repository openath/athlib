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

});