import { expect } from 'chai';
import Athlib from '../index.js';
const pkg = require('../package.json');

describe('Given an instance of Athlib', function() {
	describe('testing version', function() {
		it('Athlib.version should match package,json version '+pkg.version, () => {
			expect(Athlib.version).to.be.equal(pkg.version);
		});
	});
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
	describe('sort_by_discipline', function() {
		it('verify it sorts into standard order', function() {
			const stuff = [
				{ e: "100", name: "Jordan"},
				{ e: "PV", name: "Bilen"},
				{ e: "4x100", name: "Assorted"},
				{ e: "400", name: "Adam"},
				{ e: "400H", name: "Richard"},
				{ e: "1500", name: "Neil"},
				{ e: "3000SC", name: "Andy"},
				{ e: "HT", name: "Chris"},
				{ e: "TJ", name: "Humphrey"},
				{ e: "", name: "Nobody"},
				{ e: "CHUNDER-MILE", name: "BinMan"}
			]
			const ordered = Athlib.sort_by_discipline(stuff, "e");
			const ordered_events = ordered.map(x => x["e"]);
		  expect(ordered_events).to.eql( [
				'100', '400', '1500', '400H', '3000SC', 'PV',
				'TJ', 'HT', '4x100', "", "CHUNDER-MILE"]);
		});
		it('text_discipline_sort_key', function() {
			expect(Athlib.text_discipline_sort_key("100H")).to.be.equal( "2_00100_100H");
		});
		it('object sorting', function() {
			var obj1 = new Object();
			obj1.discipline = "HJ"

			var obj2 = new Object();
			obj2.discipline = "200"

			var obj3 = new Object();
			obj3.discipline = "4x200"

			const stuff = [obj1, obj2, obj3];
			const ordered = Athlib.sort_by_discipline(stuff);
			expect(ordered[0].discipline).to.be.equal("200");
			expect(ordered[1].discipline).to.be.equal("HJ");
		});
	});
	describe('formatSecondsAsTime', function() {
		it('verify it works correctly in good cases', function() {
      expect(Athlib.formatSecondsAsTime(27.0)).to.be.equal( "27")
      expect(Athlib.formatSecondsAsTime(27.3)).to.be.equal( "28")
      expect(Athlib.formatSecondsAsTime(27.3, 1)).to.be.equal( "27.3")
      expect(Athlib.formatSecondsAsTime(27.3, 2)).to.be.equal( "27.30")
      expect(Athlib.formatSecondsAsTime(27.3, 3)).to.be.equal( "27.300")
      expect(Athlib.formatSecondsAsTime(63)).to.be.equal( "1:03")
      expect(Athlib.formatSecondsAsTime(7380)).to.be.equal( "2:03:00")
      expect(Athlib.formatSecondsAsTime(3599.1)).to.be.equal( "1:00:00")
      expect(Athlib.formatSecondsAsTime(3599.91,1)).to.be.equal( "1:00:00.0")
		});
		it('verify it detects bad precisions', function() {
      //precision must be 0 to 3
      expect(()=>{Athlib.formatSecondsAsTime(27.3, 4)}).to.throw(Error);
      expect(()=>{Athlib.formatSecondsAsTime(27.3, null)}).to.throw(Error);
      expect(()=>{Athlib.formatSecondsAsTime(27.3, "hi")}).to.throw(Error);
		});
	});
	describe('str2num', function() {
		it('str2num("27")===27', ()=>{expect(Athlib.str2num("27")).to.be.equal(27)});
		it('str2num("27.3")===27.3', ()=>{expect(Athlib.str2num("27.3")).to.be.equal(27.3)});
		it('str2num("slow") throws error',()=>{expect(()=>{Athlib.str2num("slow")}).to.throw(Error)});
		it('str2num("3:0") throws error',()=>{expect(()=>{Athlib.str2num("3:0")}).to.throw(Error)});
	});
	describe('parseHms', function() {
		it('verify it works correctly in good cases', function() {
		  expect(Athlib.parseHms("10")).to.be.equal(10);
		  expect(Athlib.parseHms("1:10")).to.be.equal(70);
		  expect(Athlib.parseHms("1:1:10")).to.be.equal(3670);
		  expect(Athlib.parseHms("1:01:10")).to.be.equal(3670);
		  expect(Athlib.parseHms("1:01:10.1")).to.be.equal(3670.1);

		  //  floats and ints come through as is
		  expect(Athlib.parseHms(10)).to.be.equal(10);
		  expect(Athlib.parseHms(10.1)).to.be.equal(10.1);
		});
		it('verify it detects bad input', function() {
      expect(()=>{Athlib.parseInput('slow')}).to.throw(Error);
      expect(()=>{Athlib.parseInput('3:32.x')}).to.throw(Error);
		});
	});
	describe('checkPerformanceForDiscipline', function() {
		it('checkperf("XC","")===""',() =>{expect(Athlib.checkPerformanceForDiscipline("XC","")).to.be.equal("")}                                                     );
		it('checkperf("xc","")===""',() =>{expect(Athlib.checkPerformanceForDiscipline("xc","")).to.be.equal("")});
		it('checkperf("HJ","2.34")==="2.34"',() =>{expect(Athlib.checkPerformanceForDiscipline("HJ","2.34")).to.be.equal("2.34")});
		it('checkperf("HJ","  2.34  ")==="2.34"',() =>{expect(Athlib.checkPerformanceForDiscipline("HJ","  2.34  ")).to.be.equal("2.34")});
		it('checkperf("60m","7.62")==="7.62"',() =>{expect(Athlib.checkPerformanceForDiscipline("60m","7.62")).to.be.equal("7.62")});
		it('checkperf("100m","9.73456")==="9.73"',() =>{expect(Athlib.checkPerformanceForDiscipline("100m","9.73456")).to.be.equal("9.73")});
		it('checkperf("100m","12")==="12.00"',() =>{expect(Athlib.checkPerformanceForDiscipline("100m","12")).to.be.equal("12.00")});
		it('checkperf("400m","63.1")==="63.10"',() =>{expect(Athlib.checkPerformanceForDiscipline("400m","63.1")).to.be.equal("63.10")});
		it('checkperf("400m","1:03.1")==="1:03.1"',() =>{expect(Athlib.checkPerformanceForDiscipline("400m","1:03.1")).to.be.equal("1:03.1")});
		it('checkperf("800m","2:33")==="2:33"',() =>{expect(Athlib.checkPerformanceForDiscipline("800m","2:33")).to.be.equal("2:33")});
		it('checkperf("200","27,33")==="27.33"',() =>{expect(Athlib.checkPerformanceForDiscipline("200","27,33")).to.be.equal("27.33")});	// Correct French commas to decimals
		it('checkperf("800m","2;33")==="2:33"',() =>{expect(Athlib.checkPerformanceForDiscipline("800m","2;33")).to.be.equal("2:33")});	// Correct semicolons - fail to hit the shift key
		it('checkperf("800","2.33")==="2:33"',() =>{expect(Athlib.checkPerformanceForDiscipline("800","2.33")).to.be.equal("2:33")});		// Correct dots for some events
		it('checkperf("Mar","2:03:59")==="2:03:59"',() =>{expect(Athlib.checkPerformanceForDiscipline("Mar","2:03:59")).to.be.equal("2:03:59")});
		it('checkperf("XC","27:50")==="27:50"',() =>{expect(Athlib.checkPerformanceForDiscipline("XC","27:50")).to.be.equal("27:50")});
		it('checkperf("3000m","0:11:15")==="11:15"',() =>{expect(Athlib.checkPerformanceForDiscipline("3000m","0:11:15")).to.be.equal("11:15")});
		it('checkperf("60m","7:62")==="7.62"',() =>{expect(Athlib.checkPerformanceForDiscipline("60m","7:62")).to.be.equal("7.62")});
		it('checkperf("5000","0:14:53.2")==="14:53.2"',() =>{expect(Athlib.checkPerformanceForDiscipline("5000","0:14:53.2")).to.be.equal("14:53.2")});	// Excel can prepend zeroes
		it('checkperf("5000","00:14:53.2")==="14:53.2"',() =>{expect(Athlib.checkPerformanceForDiscipline("5000","00:14:53.2")).to.be.equal("14:53.2")});
		it('checkperf("1500","3:53:17")==="3:53.17"',() =>{expect(Athlib.checkPerformanceForDiscipline("1500","3:53:17")).to.be.equal("3:53.17")});		// Autocorrect 800/1500/3000 submitted as H:M:S
		it('checkperf("DEC","5875")==="5875"',() =>{expect(Athlib.checkPerformanceForDiscipline("DEC","5875")).to.be.equal("5875")});				// Multi-events
		it('checkperf("400","52:03")==="52.03"',() =>{expect(Athlib.checkPerformanceForDiscipline("400","52:03")).to.be.equal("52.03")});			// Correct some common muddles
		it('checkperf("PEN","0")==="0"',() =>{expect(Athlib.checkPerformanceForDiscipline("PEN","0")).to.be.equal("0")});					 // low score is allowed
		it('checkperf("3000mW","0:24:15")==="24:15"',() =>{expect(Athlib.checkPerformanceForDiscipline("3000mW","0:24:15")).to.be.equal("24:15")});
		it('checkperf("3KW","0:24:15")==="24:15"',() =>{expect(Athlib.checkPerformanceForDiscipline("3KW","0:24:15")).to.be.equal("24:15")});
 
		it('checkperf("DEC","10001") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("DEC","10001")}).to.throw(Error)});
		it('checkperf("DEC","4:15.8") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("DEC","4:15.8")}).to.throw(Error)});
		it('checkperf("HJ","25") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("HJ","25")}).to.throw(Error)});
		it('checkperf("HJ","Soooo Highhhh!!!") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("HJ","Soooo Highhhh!!!")}).to.throw(Error)});
		it('checkperf("HJ","2:03") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("HJ","2:03")}).to.throw(Error)});
		it('checkperf("100m","9.73w") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("100m","9.73w")}).to.throw(Error)});	// No wind, indoor figures or suffixes
		it('checkperf("XC","27.50") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("XC","27.50")}).to.throw(Error)});
		it('checkperf("100M","1:17:42:03") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("100M","1:17:42:03")}).to.throw(Error)});  // Multi-day not supported
		it('checkperf("400","0:103") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("400","0:103")}).to.throw(Error)});  // poor format
		it('checkperf("100","8.5") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("100","8.5")}).to.throw(Error)});  // > 11.0 metres per second
		it('checkperf("5000","3:45:27") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("5000","3:45:27")}).to.throw(Error)});  // < 0.5 m/sec
		it('checkperf("3KW","2:34") throws error',()=>{expect(()=>{Athlib.checkPerformanceForDiscipline("3KW","2:34")}).to.throw(Error)});
  });
	describe('roundUpStrNum', function() {
    function mytest(prec,v,x){
      it('roundUpStrNum("'+v+'",'+prec+') == "'+x+'"',()=>{expect(Athlib.roundUpStrNum(v,prec)).to.be.equal(x)});
    }
		mytest(3, '11.9990', '11.999');
		mytest(3, '11.9991', '12.000');
		mytest(3, '11.4502', '11.451');
		mytest(3, '11.4520', '11.452');
		mytest(3, '11.4500', '11.450');
		mytest(3, '11.452', '11.452');
		mytest(3, '11.450', '11.450');
		mytest(3, '11.000', '11.000');
		mytest(3, '11.0001', '11.001');
		mytest(3, '11.45', '11.450');
		mytest(3, '11.05', '11.050');
		mytest(3, '11.4', '11.400');
		mytest(3, '11.', '11.000');
		mytest(3, '11', '11.000');
		mytest(3, '1.9990', '1.999');
		mytest(3, '1.9991', '2.000');
		mytest(3, '1.4502', '1.451');
		mytest(3, '1.4520', '1.452');
		mytest(3, '1.4500', '1.450');
		mytest(3, '1.452', '1.452');
		mytest(3, '1.450', '1.450');
		mytest(3, '1.000', '1.000');
		mytest(3, '1.0001', '1.001');
		mytest(3, '1.45', '1.450');
		mytest(3, '1.05', '1.050');
		mytest(3, '1.4', '1.400');
		mytest(3, '1.', '1.000');
		mytest(3, '1', '1.000');
		mytest(3, '0.9990', '0.999');
		mytest(3, '0.9991', '1.000');
		mytest(3, '0.4502', '0.451');
		mytest(3, '0.4520', '0.452');
		mytest(3, '0.4500', '0.450');
		mytest(3, '0.452', '0.452');
		mytest(3, '0.450', '0.450');
		mytest(3, '0.000', '0.000');
		mytest(3, '0.0001', '0.001');
		mytest(3, '0.45', '0.450');
		mytest(3, '0.05', '0.050');
		mytest(3, '0.0001', '0.001');
		mytest(3, '.0001', '0.001');
		mytest(3, '0.4', '0.400');
		mytest(3, '.4', '0.400');
		mytest(3, '0.', '0.000');
		mytest(3, '0', '0.000');
	
		mytest(2, '11.990', '11.99');
		mytest(2, '11.991', '12.00');
		mytest(2, '11.4502', '11.46');
		mytest(2, '11.450', '11.45');
		mytest(2, '11.4500', '11.45');
		mytest(2, '11.452', '11.46');
		mytest(2, '11.000', '11.00');
		mytest(2, '11.0001', '11.01');
		mytest(2, '11.45', '11.45');
		mytest(2, '11.05', '11.05');
		mytest(2, '11.4', '11.40');
		mytest(2, '11.', '11.00');
		mytest(2, '11', '11.00');
		mytest(2, '1.990', '1.99');
		mytest(2, '1.991', '2.00');
		mytest(2, '1.4502', '1.46');
		mytest(2, '1.450', '1.45');
		mytest(2, '1.4500', '1.45');
		mytest(2, '1.452', '1.46');
		mytest(2, '1.000', '1.00');
		mytest(2, '1.0001', '1.01');
		mytest(2, '1.45', '1.45');
		mytest(2, '1.05', '1.05');
		mytest(2, '1.4', '1.40');
		mytest(2, '1.', '1.00');
		mytest(2, '1', '1.00');
		mytest(2, '0.990', '0.99');
		mytest(2, '0.991', '1.00');
		mytest(2, '0.4502', '0.46');
		mytest(2, '0.450', '0.45');
		mytest(2, '0.4500', '0.45');
		mytest(2, '0.452', '0.46');
		mytest(2, '0.000', '0.00');
		mytest(2, '0.0001', '0.01');
		mytest(2, '.0001', '0.01');
		mytest(2, '0.45', '0.45');
		mytest(2, '0.05', '0.05');
		mytest(2, '0.4', '0.40');
		mytest(2, '.4', '0.40');
		mytest(2, '0.', '0.00');
		mytest(2, '0', '0.00');
	
		mytest(1, '11.90', '11.9');
		mytest(1, '11.91', '12.0');
		mytest(1, '11.402', '11.5');
		mytest(1, '11.40', '11.4');
		mytest(1, '11.4500', '11.5');
		mytest(1, '11.0', '11.0');
		mytest(1, '11.450', '11.5');
		mytest(1, '11.000', '11.0');
		mytest(1, '11.0001', '11.1');
		mytest(1, '11.45', '11.5');
		mytest(1, '11.05', '11.1');
		mytest(1, '11.4', '11.4');
		mytest(1, '11.', '11.0');
		mytest(1, '11', '11.0');
		mytest(1, '1.90', '1.9');
		mytest(1, '1.91', '2.0');
		mytest(1, '1.402', '1.5');
		mytest(1, '1.40', '1.4');
		mytest(1, '1.4500', '1.5');
		mytest(1, '1.0', '1.0');
		mytest(1, '1.450', '1.5');
		mytest(1, '1.000', '1.0');
		mytest(1, '1.0001', '1.1');
		mytest(1, '1.45', '1.5');
		mytest(1, '1.05', '1.1');
		mytest(1, '1.4', '1.4');
		mytest(1, '1.', '1.0');
		mytest(1, '1', '1.0');
		mytest(1, '0.90', '0.9');
		mytest(1, '0.91', '1.0');
		mytest(1, '0.402', '0.5');
		mytest(1, '0.40', '0.4');
		mytest(1, '0.4500', '0.5');
		mytest(1, '0.0', '0.0');
		mytest(1, '0.450', '0.5');
		mytest(1, '0.000', '0.0');
		mytest(1, '0.0001', '0.1');
		mytest(1, '.0001', '0.1');
		mytest(1, '0.45', '0.5');
		mytest(1, '0.05', '0.1');
		mytest(1, '0.4', '0.4');
		mytest(1, '.4', '0.4');
		mytest(1, '0.', '0.0');
		mytest(1, '0', '0.0');
		mytest(1, '27.3', '27.3');
		mytest(1, '0.3000000000000007', '0.3');
	
		mytest(0, '11.90', '12');
		mytest(0, '11.91', '12');
		mytest(0, '11.402', '12');
		mytest(0, '11.40', '12');
		mytest(0, '11.4500', '12');
		mytest(0, '11.0', '11');
		mytest(0, '11.450', '12');
		mytest(0, '11.000', '11');
		mytest(0, '11.0001', '12');
		mytest(0, '11.45', '12');
		mytest(0, '11.05', '12');
		mytest(0, '11.4', '12');
		mytest(0, '11.', '11');
		mytest(0, '11', '11');
		mytest(0, '1.90', '2');
		mytest(0, '1.91', '2');
		mytest(0, '1.402', '2');
		mytest(0, '1.40', '2');
		mytest(0, '1.4500', '2');
		mytest(0, '1.0', '1');
		mytest(0, '1.450', '2');
		mytest(0, '1.000', '1');
		mytest(0, '1.0001', '2');
		mytest(0, '1.45', '2');
		mytest(0, '1.05', '2');
		mytest(0, '1.4', '2');
		mytest(0, '1.', '1');
		mytest(0, '1', '1');
		mytest(0, '0.90', '1');
		mytest(0, '0.91', '1');
		mytest(0, '0.402', '1');
		mytest(0, '0.40', '1');
		mytest(0, '0.4500', '1');
		mytest(0, '0.0', '0');
		mytest(0, '0.450', '1');
		mytest(0, '0.000', '0');
		mytest(0, '0.0001', '1');
		mytest(0, '.0001', '1');
		mytest(0, '0.45', '1');
		mytest(0, '0.05', '1');
		mytest(0, '0.4', '1');
		mytest(0, '.4', '1');
		mytest(0, '0.', '0');
		mytest(0, '0', '0');
  });
});
