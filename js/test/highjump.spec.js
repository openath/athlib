import { expect } from 'chai';
import { assert } from 'chai';
import Athlib from '../index.js';

var ESAA_2015_HJ = [
  //Eglish Schools Senior Boys 2015 - epic jumpoff ending in a draw
  //We did not include all other jumpers
  //See http://www.esaa.net/v2/2015/tf/national/results/fcards/tf15-sb-field.pdf
  //and http://www.englandathletics.org/england-athletics-news/great-action-at-the-english-schools-aa-championships
  ["place", "order", "bib", "first_name", "last_name", "team", "category",
    "1.81", "1.86", "1.91", "1.97", "2.00", "2.03", "2.06", "2.09", "2.12", "2.12", "2.10", "2.12", "2.10", "2.12"],
  ["", 1, 85, "Harry", "Maslen", "WYork", "SB", "o", "o", "o", "xo", "xxx"],
  ["", 2, 77, "Jake", "Field", "Surrey", "SB", "xxx"],
  ["1", 4, 53, "William", "Grimsey", "Midd", "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"],
  ["1", 5, 81, "Rory", "Dwyer", "Warks",     "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"]
  ];

var _1066 = [
  // based on above, but we have a winner
  ["place", "order", "bib", "first_name", "last_name", "team", "category",
    "1.81", "1.86", "1.91", "1.97", "2.00", "2.03", "2.06", "2.09", "2.12", "2.12", "2.10", "2.12", "2.10", "2.12", "2.11"],
  ["", 1, '85', "Dafydd", "Briton", "WYork", "SB",
    "o",  "o",  "o",  "xo", "xxx"],
  ["", 2, '77', "Jake", "Saxon", "Surrey", "SB",
    "xxx"],
  ["1", 4, '53', "William", "Norman", "Midd", "SB",
  "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x", "x"],
  ["1", 5, '81', "Harald", "England", "Warks", "SB",
  "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x", "o"]
  ];

var RIO_MENS_HJ = [  // pasted from Wikipedia
  ["place", "order", "bib", "first_name", "last_name", "team", "category", "2.20", "2.25", "2.29", "2.33", "2.36", "2.38", "2.40", "best", "note"],
  ["1", 7, 2197, "Derek", "Drouin", "CAN", "M", "o", "o", "o", "o", "o", "o", "x", 2.38, ""],
  ["2", 9, 2878, "Mutaz", "Essa Barshim", "QAT", "M", "o", "o", "o", "o", "o", "xxx", "", 2.36, ""],
  ["3", 3, 3026, "Bohdan", "Bondarenko", "UKR", "M", "-", "o", "-", "o", "-", "xx-", "x", 2.33, ""],
  ["4=", 8, 2456, "Robert", "Grabarz", "GBR", "M", "o", "xo", "o", "o", "xxx", "", "", 2.33, "=SB"],
  ["4=", 15, 3032, "Andriy", "Protsenko", "UKR", "M", "o", "o", "xo", "o", "xxx", "", "", 2.33, "SB"],
  ["6", 6, 3084, "Erik", "Kynard", "USA", "M", "o", "xo", "o", "xxo", "xxx", "", "", 2.33, ""],
  ["7=", 5, 2961, "Majededdin", "Ghazal", "SYR", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
  ["7=", 12, 2294, "Kyriakos", "Ioannou", "CYP", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
  ["7=", 13, 2076, "Donald", "Thomas", "BAH", "M", "o", "o", "o", "xxx", "", "", "", 2.29, ""],
  ["10", 1, 2182, "Tihomir", "Ivanov", "BUL", "M", "o", "xo", "o", "xxx", "", "", "", 2.29, "=PB"],
  ["11", 10, 2062, "Trevor", "Barry", "BAH", "M", "o", "o", "xxx", "", "", "", "", 2.25, ""],
  ["12", 4, 2293, "Dimitrios", "Chondrokoukis", "M", "CYP", "xo", "o", "xxx", "", "", "", "", 2.25, ""],
  ["13", 11, 2871, "Luis", "Castro", "PUR", "M", "o", "xxo", "xxx", "", "", "", "", 2.25, ""],
  ["14", 14, 2297, "Jaroslav", "Bába", "CZE", "M", "o", "xxx", "", "", "", "", "", 2.2, ""],
  ["15", 2, 2052, "Brandon", "Starc", "AUS", "M", "xo", "xxx", "", "", "", "", "", 2.2, ""]
  ];

function createEmptyCompetition(matrix){
  //Creates from an array similar to above; named athletes with bibs
  var c = Athlib.HighJumpCompetition();
  var i, j;
  for(i=1;i<matrix.length;i++){
    var kwds={};
    for(j=1;j<7;j++) kwds[matrix[0][j]] = matrix[i][j];
    c.addJumper(kwds);
    }
  return c;
  }

describe('Given an instance of Athlib.HighJumpCompetition', function(){
  describe('Tests basic creation of athletes with names and bibs', function(){
  var c=createEmptyCompetition(ESAA_2015_HJ);
  it('last of jumpers should be named Dwyer',()=>{
    expect(c.jumpers[c.jumpers.length-1].last_name).to.be.equal('Dwyer');
    });
  it('jumpersByBib[85] should be named Maslen',()=>{
    expect(c.jumpersByBib[85].last_name).to.be.equal('Maslen');
    });
  });
  describe('Tests progression',function(){
  var c = createEmptyCompetition(ESAA_2015_HJ);
  var h1 = 1.81;
  c.setBarHeight(h1);

  // round 1
  c.cleared(85);

  var j = c.jumpersByBib[85];
  it("'bib85 expect ['o']",()=>{
    expect(c._compareKeys(j.attemptsByHeight,['o'])).to.be.equal(0);
    });
  it("'expect highest cleared="+h1,()=>{
    expect(j.highestCleared).to.be.equal(h1);
    });
  c.failed(77);
  c.failed(77);
  c.failed(77);

  var jake_field = c.jumpersByBib[77];
  it("'expect highest cleared=0",()=>{
    expect(jake_field.highestCleared).to.be.equal(0);
    });
  it("jake_field expect ['xxx']",()=>{
    expect(c._compareKeys(jake_field.attemptsByHeight,['xxx'])).to.be.equal(0);
    });
  it("'jake_field eliminated true",()=>{
    expect(jake_field.eliminated).to.be.equal(true);
    });
  var harry_maslen = c.jumpersByBib[85];

  //attempt at fourth jump should fail
  it("'jake_field 4th jump not allowed",()=>{
    var r=0,e;
    try{
      c.failed(77);
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });
  // the rules do not define whether someone who failed
  // 3 times at the first height is 'worse' then someone
  // who has not jumped at all.  Only relevant at interim
  // stage.  Should refine code to have a 'jumped_yet'
  // fourth key.
  // it("'jake_field 4th",()=>{
  //    expect(jake_field.place).to.be.equal(4);
  //  });
  //self.assertEquals(harry_maslen.place, 1)
  it("harry_maslen 1st",()=>{
    expect(harry_maslen.place).to.be.equal(1);
    });
  });
  describe('Test replay to jumpoff',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(ESAA_2015_HJ,9);

    // see who is winning
    const maslen = c.jumpersByBib['85'];
    const field = c.jumpersByBib['77'];
    const grimsey = c.jumpersByBib['53'];
    const dwyer = c.jumpersByBib['81'];

    it("field.place == 4",()=>{expect(field.place).to.be.equal(4)});
    it("maslen.place == 3",()=>{expect(maslen.place).to.be.equal(3)});
    it("grimsey.place == 1",()=>{expect(grimsey.place).to.be.equal(1)});
    it("dwyer.place == 1",()=>{expect(dwyer.place).to.be.equal(1)});
    it("c.remaining.length == 2",()=>{expect(c.remaining.length).to.be.equal(2)});
    it("c.state == jumpoff",()=>{expect(c.state).to.be.equal('jumpoff')});
  });
  describe('Test replay through jumpoff to draw',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(ESAA_2015_HJ);
  it("53 is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('53');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });

    // see who is winning
    const maslen = c.jumpersByBib['85'];
    const field = c.jumpersByBib['77'];
    const grimsey = c.jumpersByBib['53'];
    const dwyer = c.jumpersByBib['81'];

    it("field.place == 4",()=>{expect(field.place).to.be.equal(4)});
    it("maslen.place == 3",()=>{expect(maslen.place).to.be.equal(3)});
    it("grimsey.place == 1",()=>{expect(grimsey.place).to.be.equal(1)});
    it("dwyer.place == 1",()=>{expect(dwyer.place).to.be.equal(1)});
    it("c.remaining.length == 2",()=>{expect(c.remaining.length).to.be.equal(2)});
    it("c.state == jumpoff",()=>{expect(c.state).to.be.equal('jumpoff')});
  });
  describe('Test replay through jumpoff to final winner',function(){
    // Run through to where the jumpoff began - ninth bar position
  const c = Athlib.HighJumpCompetition.fromMatrix(_1066);
  it("53 is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('53');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });
  it("81 is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('81');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });

    // see who is winning
    const briton = c.jumpersByBib['85'];
    const saxon = c.jumpersByBib['77'];
    const norman = c.jumpersByBib['53'];
    const england = c.jumpersByBib['81'];

    it("saxon.place == 4",()=>{expect(saxon.place).to.be.equal(4)});
    it("briton.place == 3",()=>{expect(briton.place).to.be.equal(3)});
    it("norman.place == 2",()=>{expect(norman.place).to.be.equal(2)});
    it("england.place == 1",()=>{expect(england.place).to.be.equal(1)});
    it("c.remaining.length == 1",()=>{expect(c.remaining.length).to.be.equal(1)});
    it("c.state == finished",()=>{expect(c.state).to.be.equal('finished')});
    it("england.highestCleared == 2.11",()=>england.highestCleared==2.11);

    it("can't set height 2.12 in finished competition",() => {
    var r=0, e;
    try {
      c.setBarHeight(2.12);
    } catch(e) {
     r=1;
    }
     return r===1;
    });
  });
  describe('Test countback to tie',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o",  "xo",   "xo",   "xxx"],
        ["",    2,     'B',  "William", "Norman",    "o",  "o",  "o",  "xxo",  "xxx"],
        ]
      );
  it("A is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('A');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });
  it("81 is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });

    // see who is winning
    const A = c.jumpersByBib['A'];
    const B = c.jumpersByBib['B'];

  it("A.place == 1",()=>{expect(A.place).to.be.equal(1)});
  it("B.place == 2",()=>{expect(B.place).to.be.equal(2)});
  it("c.remaining.length == 0",()=>{expect(c.remaining.length).to.be.equal(0)});
  it("c.state == finished",()=>{expect(c.state).to.be.equal('finished')});
  it("A.highestCleared == 2.12",()=>{expect(A.highestCleared).to.be.equal(2.12)});
  it("B.highestCleared == 2.12",()=>{expect(B.highestCleared).to.be.equal(2.12)});
  it("A.rankingKey == [-2.12, 1, 5]",()=>{expect(c._compareKeys(A.rankingKey,[-2.12, 1, 5])).to.be.equal(0)});
  it("B.rankingKey == [-2.12, 2, 5]",()=>{expect(c._compareKeys(B.rankingKey,[-2.12, 2, 5])).to.be.equal(0)});
  });
  describe('Test total failure rank',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o"],
        ["",    2,     'B',  "William", "Norman",    "xxx"],
        ]
      );
  it("B is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });

    // see who is winning
  const A = c.jumpersByBib['A'];
  const B = c.jumpersByBib['B'];

  it("A.place == 1",()=>{expect(A.place).to.be.equal(1)});
  it("B.place == 2",()=>{expect(B.place).to.be.equal(2)});
  it("c.remaining.length == 1",()=>{expect(c.remaining.length).to.be.equal(1)});
  it("c.state == won",()=>{expect(c.state).to.be.equal('won')});
  it("A.highestCleared == 2.08",()=>{expect(A.highestCleared).to.be.equal(2.08)});
  it("B.highestCleared == 0",()=>{expect(B.highestCleared).to.be.equal(0)});
  it("A.rankingKey == [-2.08, 0, 0]",()=>{expect(c._compareKeys(A.rankingKey,[-2.08, 0, 0])).to.be.equal(0)});
  it("B.rankingKey == [-0, 3, 3]",()=>{expect(c._compareKeys(B.rankingKey,[-0, 3, 3])).to.be.equal(0)});
  });
  describe('Test countback to total failures',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o",  "xo",   "xo",   "xxx"],
        ["",    2,     'B',  "William", "Norman",    "o",  "xo",   "xo",   "xo",   "xxx"],
        ]
      );
  it("A is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('A');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });
  it("81 is not allowed to jump again",()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).to.be.equal(1);
    });

    // see who is winning
    const A = c.jumpersByBib['A'];
    const B = c.jumpersByBib['B'];

  it("A.place == 1",()=>{expect(A.place).to.be.equal(1)});
  it("B.place == 2",()=>{expect(B.place).to.be.equal(2)});
  it("c.remaining.length == 0",()=>{expect(c.remaining.length).to.be.equal(0)});
  it("c.state == finished",()=>{expect(c.state).to.be.equal('finished')});
  it("A.highestCleared == 2.12",()=>{expect(A.highestCleared).to.be.equal(2.12)});
  it("B.highestCleared == 2.12",()=>{expect(B.highestCleared).to.be.equal(2.12)});
  it("A.rankingKey == [-2.12, 1, 5]",()=>{expect(c._compareKeys(A.rankingKey,[-2.12, 1, 5])).to.be.equal(0)});
  it("B.rankingKey == [-2.12, 1, 6]",()=>{expect(c._compareKeys(B.rankingKey,[-2.12, 1, 6])).to.be.equal(0)});
  });
  describe('Test won ending',function(){
	it("test scheduled-->started-->won-->finished",()=>{
	const mx = [
				["place", "order", "bib", "first_name", "last_name", "team", "category"],
				["1", 1, '53', "William", "Norman", "Midd", "SB"],
				["1", 2, '81', "Harald", "England", "Warks", "SB"],
				];
	const c = Athlib.HighJumpCompetition.fromMatrix(mx);
	assert.equal(c.state,'scheduled');
	assert.equal(c.remaining.length,2);
	const delta = [
		[2.11,["o","o"],'started',2],
		[2.12,["o","o"],'started',2],
		[2.13,["o","o"],'started',2],
		[2.14,["xxx","o"],'won',1],
		[2.16,["","o"],'won',1],
		[2.17,["","xxo"],'won',1],
		[2.18,["","xxx"],'finished',0]];
	for(var k=0;k<delta.length;k++){
		const height=delta[k][0],perfs=delta[k][1],xstate=delta[k][2],lenremj=delta[k][3];
		c.setBarHeight(height)
		for(var i=0;i<3;i++){
			for(var j=0;j<perfs.length;j++){
				const p=perfs[j];
				if(p.length<i+1)continue;
				c.bibTrial(mx[1+j][2],p[i]);
				}
			}
		assert.equal(c.state,xstate);
		assert.equal(c.remaining.length,lenremj);
		}
	});
  });
  describe('Reproduce Rio Olympic results',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(RIO_MENS_HJ);

    it("drouin.place == 1",()=>{expect(c.jumpersByBib['2197'].place).to.be.equal(1)});
    it("barshim.place == 2",()=>{expect(c.jumpersByBib['2878'].place).to.be.equal(2)});
    it("bondarenko.place == 3",()=>{expect(c.jumpersByBib['3026'].place).to.be.equal(3)});
    it("grabarz.place == 4",()=>{expect(c.jumpersByBib['2456'].place).to.be.equal(4)});
    it("protsenko.place == 4",()=>{expect(c.jumpersByBib['3032'].place).to.be.equal(4)});
    it("kynard.place == 6",()=>{expect(c.jumpersByBib['3084'].place).to.be.equal(6)});
    it("ghazal.place == 7",()=>{expect(c.jumpersByBib['2961'].place).to.be.equal(7)});
    it("iouannou.place == 7",()=>{expect(c.jumpersByBib['2294'].place).to.be.equal(7)});
    it("thomas.place == 7",()=>{expect(c.jumpersByBib['2076'].place).to.be.equal(7)});
    it("ivanov.place == 10",()=>{expect(c.jumpersByBib['2182'].place).to.be.equal(10)});
    it("barry.place == 11",()=>{expect(c.jumpersByBib['2062'].place).to.be.equal(11)});
    it("chondrokoukis.place == 12",()=>{expect(c.jumpersByBib['2293'].place).to.be.equal(12)});
    it("castro.place == 13",()=>{expect(c.jumpersByBib['2871'].place).to.be.equal(13)});
    it("bába.place == 14",()=>{expect(c.jumpersByBib['2297'].place).to.be.equal(14)});
    it("starc.place == 15",()=>{expect(c.jumpersByBib['2052'].place).to.be.equal(15)});
  });
  describe('test dismissed',function(){
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition();
	c.addJumper({bib:'A',first_name:'Harald',last_names:'England'});
	c.addJumper({bib:'B',first_name:'William',last_names:'Norman'});
	it("cleared should raise an error",()=>{expect(()=>{c.cleared('A')}).to.throw(Error)});
	it("passed should raise an error",()=>{expect(()=>{c.passed('A')}).to.throw(Error)});
	it("failed should raise an error",()=>{expect(()=>{c.failed('A')}).to.throw(Error)});
	it("retired should raise an error",()=>{expect(()=>{c.retired('A')}).to.throw(Error)});
	c.setBarHeight(2.00);
	const A=c.jumpersByBib['A'];
	const B=c.jumpersByBib['B'];
	(function (){
		const a=A.dismissed,b=B.dismissed;
		it("A.dismissed should be false 1",()=>{expect(a).to.be.equal(false)});
		it("B.dismissed should be false 1",()=>{expect(b).to.be.equal(false)});
		})();
	c.cleared('A');
	c.passed('B');
	(function (){
		const a=A.dismissed,b=B.dismissed;
		it("A.dismissed should be true 2",()=>{expect(a).to.be.equal(true)});
		it("B.dismissed should be true 2",()=>{expect(b).to.be.equal(true)});
		})();
	c.setBarHeight(2.02);
	(function (){
		const a=A.dismissed,b=B.dismissed;
		it("A.dismissed should be false 3",()=>{expect(a).to.be.equal(false)});
		it("B.dismissed should be false 3",()=>{expect(b).to.be.equal(false)});
		})();
	c.cleared('A');
	c.failed('B');
	(function (){
		const a=A.dismissed,b=B.dismissed;
		it("A.dismissed should be true 4",()=>{expect(a).to.be.equal(true)});
		it("B.dismissed should be false 4",()=>{expect(b).to.be.equal(false)});
		})();
	c.passed('B');
	it("B.dismissed should be true",()=>{expect(B.dismissed).to.be.equal(true)});
  });
  describe('test trials',function(){
    const c = Athlib.HighJumpCompetition();
		c.addJumper({bib:'A',first_name:'Harald',last_names:'England'});
		c.addJumper({bib:'B',first_name:'William',last_names:'Norman'});
		c.setBarHeight(1.10);
		c.cleared('A');
		c.cleared('B');
		c.setBarHeight(1.15);
		c.failed('A');
		c.failed('B');
		c.failed('A');
		c.failed('B');
		c.failed('A');
		c.failed('B');
		(function(){
			const state=c.state;
			it("state now jumpoff'",()=>{expect(state).to.equal('jumpoff')});
		})();
		c.setBarHeight(1.14);
		(function(){
			const trials=c.trials.slice();
			it("check trials at start of jumpoff",()=>{expect(trials).to.eql([['A',1.10,'o'],['B',1.10,'o'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x']])});
		})();
		c.failed('A');
		(function(){
			const state=c.state;
			const trials=c.trials.slice();
			it("state still 'jumpoff'",()=>{expect(state).to.equal('jumpoff')});
			it("check trials after A fails",()=>{expect(trials).to.eql([['A',1.10,'o'],['B',1.10,'o'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x'],['A',1.14,'x']])});
		})();
		c.cleared('B');
		(function(){
			const state=c.state;
			const trials=c.trials.slice();
			it("state now 'finished'",()=>{expect(state).to.equal('finished')});
			it("check trials after B clears",()=>{expect(trials).to.eql([['A',1.10,'o'],['B',1.10,'o'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x'],['A',1.15,'x'],['B',1.15,'x'],['A',1.14,'x'],['B',1.14,'o']])});
		})();
  });
  describe('test actionLetter',function(){
    const c = Athlib.HighJumpCompetition();
		it("actionLetter('cleared')==='o'",()=>{expect(c.actionLetter.cleared).to.be.equal('o')});
		it("actionLetter('failed')==='x'",()=>{expect(c.actionLetter.failed).to.be.equal('x')});
		it("actionLetter('passed')==='-'",()=>{expect(c.actionLetter.passed).to.be.equal('-')});
		it("actionLetter('retired')==='r'",()=>{expect(c.actionLetter.retired).to.be.equal('r')});
  });
});
