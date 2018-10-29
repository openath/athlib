var Athlib = require(process.env.TESTSRC==='src' ? '../src/library.js' : '../dist/athlib.web.js');

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

describe('Given an instance of Athlib.HighJumpCompetition', () => {
  describe('Tests basic creation of athletes with names and bibs', () => {
  var c=createEmptyCompetition(ESAA_2015_HJ);
  test('last of jumpers should be named Dwyer', ()=>{
    expect(c.jumpers[c.jumpers.length-1].last_name).toEqual('Dwyer');
    });
  test('jumpersByBib[85] should be named Maslen', ()=>{
    expect(c.jumpersByBib[85].last_name).toEqual('Maslen');
    });
  });
  describe('Tests progression',() => {
  var c = createEmptyCompetition(ESAA_2015_HJ);
  var h1 = 1.81;
  c.setBarHeight(h1);

  // round 1
  c.cleared(85);

  var j = c.jumpersByBib[85];
  test("'bib85 expect ['o']", ()=>{
    expect(c._compareKeys(j.attemptsByHeight,['o'])).toEqual(0);
    });
  test("'expect highest cleared="+h1, ()=>{
    expect(j.highestCleared).toEqual(h1);
    });
  c.failed(77);
  c.failed(77);
  c.failed(77);

  var jake_field = c.jumpersByBib[77];
  test("'expect highest cleared=0", ()=>{
    expect(jake_field.highestCleared).toEqual(0);
    });
  test("jake_field expect ['xxx']", ()=>{
    expect(c._compareKeys(jake_field.attemptsByHeight,['xxx'])).toEqual(0);
    });
  test("'jake_field eliminated true", ()=>{
    expect(jake_field.eliminated).toEqual(true);
    });
  var harry_maslen = c.jumpersByBib[85];

  //attempt at fourth jump should fail
  test("'jake_field 4th jump not allowed", ()=>{
    var r=0,e;
    try{
      c.failed(77);
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });
  // the rules do not define whether someone who failed
  // 3 times at the first height is 'worse' then someone
  // who has not jumped at all.  Only relevant at interim
  // stage.  Should refine code to have a 'jumped_yet'
  // fourth key.
  // it("'jake_field 4th",()=>{
  //    expect(jake_field.place).toEqual(4);
  //  });
  //self.assertEquals(harry_maslen.place, 1)
  test("harry_maslen 1st", ()=>{expect(harry_maslen.place).toEqual(1);});
  });



  describe('Test replay to jumpoff',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(ESAA_2015_HJ,9);

    // see who is winning
    const maslen = c.jumpersByBib['85'];
    const field = c.jumpersByBib['77'];
    const grimsey = c.jumpersByBib['53'];
    const dwyer = c.jumpersByBib['81'];

    test("field.place == 4", ()=>{expect(field.place).toEqual(4)});
    test("maslen.place == 3", ()=>{expect(maslen.place).toEqual(3)});
    test("grimsey.place == 1", ()=>{expect(grimsey.place).toEqual(1)});
    test("dwyer.place == 1", ()=>{expect(dwyer.place).toEqual(1)});
    test("c.remaining.length == 2", ()=>{expect(c.remaining.length).toEqual(2)});
    test("c.state == jumpoff", ()=>{expect(c.state).toEqual('jumpoff')});
  });
  describe('Test replay through jumpoff to draw',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(ESAA_2015_HJ);
  test("53 is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('53');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });

    // see who is winning
    const maslen = c.jumpersByBib['85'];
    const field = c.jumpersByBib['77'];
    const grimsey = c.jumpersByBib['53'];
    const dwyer = c.jumpersByBib['81'];

    test("field.place == 4", ()=>{expect(field.place).toEqual(4)});
    test("maslen.place == 3", ()=>{expect(maslen.place).toEqual(3)});
    test("grimsey.place == 1", ()=>{expect(grimsey.place).toEqual(1)});
    test("dwyer.place == 1", ()=>{expect(dwyer.place).toEqual(1)});
    test("c.remaining.length == 2", ()=>{expect(c.remaining.length).toEqual(2)});
    test("c.state == jumpoff", ()=>{expect(c.state).toEqual('jumpoff')});
  });
  describe('Test replay through jumpoff to final winner',() => {
    // Run through to where the jumpoff began - ninth bar position
  const c = Athlib.HighJumpCompetition.fromMatrix(_1066);
  test("53 is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('53');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });
  test("81 is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('81');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });

    // see who is winning
    const briton = c.jumpersByBib['85'];
    const saxon = c.jumpersByBib['77'];
    const norman = c.jumpersByBib['53'];
    const england = c.jumpersByBib['81'];

    test("saxon.place == 4", ()=>{expect(saxon.place).toEqual(4)});
    test("briton.place == 3", ()=>{expect(briton.place).toEqual(3)});
    test("norman.place == 2", ()=>{expect(norman.place).toEqual(2)});
    test("england.place == 1", ()=>{expect(england.place).toEqual(1)});
    test("c.remaining.length == 1", ()=>{expect(c.remaining.length).toEqual(1)});
    test("c.state == finished", ()=>{expect(c.state).toEqual('finished')});
    test("england.highestCleared == 2.11", ()=>{expect(england.highestCleared).toEqual(2.11)});

    test("can't set height 2.12 in finished competition",
      ()=>{expect(()=>{c.setBarHeight(2.12)}).toThrow(Error)}
      );
      
  });
  describe('Test countback to tie',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o",  "xo",   "xo",   "xxx"],
        ["",    2,     'B',  "William", "Norman",    "o",  "o",  "o",  "xxo",  "xxx"],
        ]
      );
  test("A is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('A');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });
  test("81 is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });

    // see who is winning
    const A = c.jumpersByBib['A'];
    const B = c.jumpersByBib['B'];

  test("A.place == 1", ()=>{expect(A.place).toEqual(1)});
  test("B.place == 2", ()=>{expect(B.place).toEqual(2)});
  test("c.remaining.length == 0", ()=>{expect(c.remaining.length).toEqual(0)});
  test("c.state == finished", ()=>{expect(c.state).toEqual('finished')});
  test(
    "A.highestCleared == 2.12",
    ()=>{expect(A.highestCleared).toEqual(2.12)}
  );
  test(
    "B.highestCleared == 2.12",
    ()=>{expect(B.highestCleared).toEqual(2.12)}
  );
  test(
    "A.rankingKey == [-2.12, 1, 5]",
    ()=>{expect(c._compareKeys(A.rankingKey,[-2.12, 1, 5])).toEqual(0)}
  );
  test(
    "B.rankingKey == [-2.12, 2, 5]",
    ()=>{expect(c._compareKeys(B.rankingKey,[-2.12, 2, 5])).toEqual(0)}
  );
  });
  describe('Test total failure rank',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o"],
        ["",    2,     'B',  "William", "Norman",    "xxx"],
        ]
      );
  test("B is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });

    // see who is winning
  const A = c.jumpersByBib['A'];
  const B = c.jumpersByBib['B'];

  test("A.place == 1", ()=>{expect(A.place).toEqual(1)});
  test("B.place == 2", ()=>{expect(B.place).toEqual(2)});
  test("c.remaining.length == 1", ()=>{expect(c.remaining.length).toEqual(1)});
  test("c.state == won", ()=>{expect(c.state).toEqual('won')});
  test(
    "A.highestCleared == 2.08",
    ()=>{expect(A.highestCleared).toEqual(2.08)}
  );
  test("B.highestCleared == 0", ()=>{expect(B.highestCleared).toEqual(0)});
  test(
    "A.rankingKey == [-2.08, 0, 0]",
    ()=>{expect(c._compareKeys(A.rankingKey,[-2.08, 0, 0])).toEqual(0)}
  );
  test(
    "B.rankingKey == [-0, 3, 3]",
    ()=>{expect(c._compareKeys(B.rankingKey,[-0, 3, 3])).toEqual(0)}
  );
  });
  describe('Test countback to total failures',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(
        [
        ["place", "order", "bib", "first_name", "last_name", "2.06", "2.08", "2.10", "2.12", "2.14"],
        ["",    1,     'A',  "Harald", "England",    "o",  "o",  "xo",   "xo",   "xxx"],
        ["",    2,     'B',  "William", "Norman",    "o",  "xo",   "xo",   "xo",   "xxx"],
        ]
      );
  test("A is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('A');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });
  test("81 is not allowed to jump again", ()=>{
    var r=0,e;
    try{
      c.failed('B');
      }
    catch(e){
      r=1;
      }
    expect(r).toEqual(1);
    });

    // see who is winning
    const A = c.jumpersByBib['A'];
    const B = c.jumpersByBib['B'];

  test("A.place == 1", ()=>{expect(A.place).toEqual(1)});
  test("B.place == 2", ()=>{expect(B.place).toEqual(2)});
  test("c.remaining.length == 0", ()=>{expect(c.remaining.length).toEqual(0)});
  test("c.state == finished", ()=>{expect(c.state).toEqual('finished')});
  test(
    "A.highestCleared == 2.12",
    ()=>{expect(A.highestCleared).toEqual(2.12)}
  );
  test(
    "B.highestCleared == 2.12",
    ()=>{expect(B.highestCleared).toEqual(2.12)}
  );
  test(
    "A.rankingKey == [-2.12, 1, 5]",
    ()=>{expect(c._compareKeys(A.rankingKey,[-2.12, 1, 5])).toEqual(0)}
  );
  test(
    "B.rankingKey == [-2.12, 1, 6]",
    ()=>{expect(c._compareKeys(B.rankingKey,[-2.12, 1, 6])).toEqual(0)}
  );
  });
  describe('Test won ending',() => {
	test("test scheduled-->started-->won-->finished", ()=>{
	const mx = [
				["place", "order", "bib", "first_name", "last_name", "team", "category"],
				["1", 1, '53', "William", "Norman", "Midd", "SB"],
				["1", 2, '81', "Harald", "England", "Warks", "SB"],
				];
	const c = Athlib.HighJumpCompetition.fromMatrix(mx);
	expect(c.state).toEqual('scheduled');
	expect(c.remaining.length).toEqual(2);
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
		expect(c.state).toEqual(xstate);
		expect(c.remaining.length).toEqual(lenremj);
		}
	});
  });
  describe('Reproduce Rio Olympic results',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition.fromMatrix(RIO_MENS_HJ);

    test(
      "drouin.place == 1",
      ()=>{expect(c.jumpersByBib['2197'].place).toEqual(1)}
    );
    test(
      "barshim.place == 2",
      ()=>{expect(c.jumpersByBib['2878'].place).toEqual(2)}
    );
    test(
      "bondarenko.place == 3",
      ()=>{expect(c.jumpersByBib['3026'].place).toEqual(3)}
    );
    test(
      "grabarz.place == 4",
      ()=>{expect(c.jumpersByBib['2456'].place).toEqual(4)}
    );
    test(
      "protsenko.place == 4",
      ()=>{expect(c.jumpersByBib['3032'].place).toEqual(4)}
    );
    test(
      "kynard.place == 6",
      ()=>{expect(c.jumpersByBib['3084'].place).toEqual(6)}
    );
    test(
      "ghazal.place == 7",
      ()=>{expect(c.jumpersByBib['2961'].place).toEqual(7)}
    );
    test(
      "iouannou.place == 7",
      ()=>{expect(c.jumpersByBib['2294'].place).toEqual(7)}
    );
    test(
      "thomas.place == 7",
      ()=>{expect(c.jumpersByBib['2076'].place).toEqual(7)}
    );
    test(
      "ivanov.place == 10",
      ()=>{expect(c.jumpersByBib['2182'].place).toEqual(10)}
    );
    test(
      "barry.place == 11",
      ()=>{expect(c.jumpersByBib['2062'].place).toEqual(11)}
    );
    test(
      "chondrokoukis.place == 12",
      ()=>{expect(c.jumpersByBib['2293'].place).toEqual(12)}
    );
    test(
      "castro.place == 13",
      ()=>{expect(c.jumpersByBib['2871'].place).toEqual(13)}
    );
    test(
      "bába.place == 14",
      ()=>{expect(c.jumpersByBib['2297'].place).toEqual(14)}
    );
    test(
      "starc.place == 15",
      ()=>{expect(c.jumpersByBib['2052'].place).toEqual(15)}
    );
  });
  describe('test dismissed',() => {
    // Run through to where the jumpoff began - ninth bar position
    const c = Athlib.HighJumpCompetition();
	c.addJumper({bib:'A',first_name:'Harald',last_names:'England'});
	c.addJumper({bib:'B',first_name:'William',last_names:'Norman'});
	test(
      "cleared should raise an error",
      ()=>{expect(()=>{c.cleared('A')}).toThrow(Error)}
    );
	test(
      "passed should raise an error",
      ()=>{expect(()=>{c.passed('A')}).toThrow(Error)}
    );
	test(
      "failed should raise an error",
      ()=>{expect(()=>{c.failed('A')}).toThrow(Error)}
    );
	test(
      "retired should raise an error",
      ()=>{expect(()=>{c.retired('A')}).toThrow(Error)}
    );
	c.setBarHeight(2.00);
	const A=c.jumpersByBib['A'];
	const B=c.jumpersByBib['B'];
	(function (){
		const a=A.dismissed,b=B.dismissed;
		test("A.dismissed should be false 1", ()=>{expect(a).toEqual(false)});
		test("B.dismissed should be false 1", ()=>{expect(b).toEqual(false)});
		})();
	c.cleared('A');
	c.passed('B');
	(function (){
		const a=A.dismissed,b=B.dismissed;
		test("A.dismissed should be true 2", ()=>{expect(a).toEqual(true)});
		test("B.dismissed should be true 2", ()=>{expect(b).toEqual(true)});
		})();
	c.setBarHeight(2.02);
	(function (){
		const a=A.dismissed,b=B.dismissed;
		test("A.dismissed should be false 3", ()=>{expect(a).toEqual(false)});
		test("B.dismissed should be false 3", ()=>{expect(b).toEqual(false)});
		})();
	c.cleared('A');
	c.failed('B');
	(function (){
		const a=A.dismissed,b=B.dismissed;
		test("A.dismissed should be true 4", ()=>{expect(a).toEqual(true)});
		test("B.dismissed should be false 4", ()=>{expect(b).toEqual(false)});
		})();
	c.passed('B');
	test("B.dismissed should be true", ()=>{expect(B.dismissed).toEqual(true)});
  });
});
