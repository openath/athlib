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
			expect(Athlib.isMultiEvent('PEN')).to.equal(true);
			expect(Athlib.isMultiEvent(' heptathalon ')).to.equal(true);
			expect(Athlib.isMultiEvent('Decy')).to.equal(true);
			expect(Athlib.isMultiEvent('Octa')).to.equal(true);
		});
	});
	describe('betterPerformance', function() {
		it('should detect better performances', function() {
			expect(Athlib.betterPerformance('83.25', '17.3', 'JT')).to.equal('83.25');
			expect(Athlib.betterPerformance('10.5', '10.6', '100')).to.equal('10.5');
			expect(Athlib.betterPerformance('3456', '4567', 'DEC')).to.equal('4567');
			expect(Athlib.betterPerformance('3456', '4567', 'MUL')).to.equal('4567');
		});
	});
	describe('getDistance', function() {
		it('checks itself', function() {
		  expect(Athlib.getDistance("100")).to.equal(100);
		  expect(Athlib.getDistance("110mH")).to.equal(110);
		  expect(Athlib.getDistance("5K")).to.equal(5000);
		  expect(Athlib.getDistance("MILE")).to.equal(1609);
		  expect(Athlib.getDistance("CHUNDER-MILE")).to.equal(1609);
		  expect(Athlib.getDistance("5M")).to.equal(8045);
		  expect(Athlib.getDistance("HM")).to.equal(21098);
		  expect(Athlib.getDistance("MAR")).to.equal(42195);
		  expect(Athlib.getDistance("XC")).to.equal(null);
		  expect(Athlib.getDistance("HJ")).to.equal(null);
		  expect(Athlib.getDistance("4xrelay")).to.equal(null);
		  expect(Athlib.getDistance("4x100")).to.equal(400);
		  expect(Athlib.getDistance("4x100H")).to.equal(400);
		  expect(Athlib.getDistance("3x100h")).to.equal(300);
		  expect(Athlib.getDistance("4x400")).to.equal(1600);
		  expect(Athlib.getDistance("7.5M")).to.equal(12067);
		  expect(Athlib.getDistance("7.5SC")).to.equal(null);
		  expect(Athlib.getDistance("440Y")).to.equal(402);
		  expect(Athlib.getDistance("3000W")).to.equal(3000);
		  expect(Athlib.getDistance("3KW")).to.equal(3000);
		  expect(Athlib.getDistance("3kmW")).to.equal(3000);
		});
	});
});
