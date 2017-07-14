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
	["1", 5, 81, "Rory", "Dwyer", "Warks",	   "SB", "", "", "", "o", "o", "o", "o", "o", "xxx", "x", "o", "x", "o", "x"]
	];

function create_empty_competition(matrix){
	//Creates from an array similar to above; named athletes with bibs
	var c = Athlib.HighJumpCompetition();
	var i, j;
	for(i=1;i<matrix.length;i++){
		var kwds={};
		for(j=1;j<7;j++) kwds[matrix[0][j]] = matrix[i][j];
		c.add_jumper(kwds);
		}
	return c;
	}

describe('Given an instance of Athlib.HighJumpCompetition',function(){
  describe('Tests basic creation of athletes with names and bibs',function(){
    var c=create_empty_competition(ESAA_2015_HJ);
    it('last of jumpers should be named Dwyer',()=>{
      	expect(c.jumpers[jumpers.length-1].last_name).to.be.equal('Dwyer');
    	});
    it('jumpers_by_bib[85] should be named Dwyer',()=>{
      	expect(c.jumpers_by_bib[85].last_name).to.be.equal('Maslin');
    	});
  	});
	});
