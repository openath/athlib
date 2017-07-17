import { expect } from 'chai';
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
    it("'jake_field expect ['xxx']",()=>{
        expect(c._compareKeys(j.attemptsByHeight,['xxx'])).to.be.equal(0);
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
    //      expect(jake_field.place).to.be.equal(4);
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
		it("c.remaining() == 0",()=>{expect(c.remaining()).to.be.equal(0)});
    });
});
