function iaaf_scoring_key(gender,event_code){
	return (gender+'-'+event_code).toUpperCase();
	}
var _iaaf_jump_codes=new RegExp("^(LJ|PV|TJ|HJ)$","i");
var _iaaf_throw_codes=new RegExp("^(WT|JT|DT|HT)$","i");
var _iaaf_scoring_table = [{gender:"M",event_code:"100",A:25.4347,Z:18,X:1.81},{gender:"M",event_code:"200",A:5.8425,Z:38,X:1.81},{gender:"M",event_code:"400",A:1.53775,Z:82,X:1.81},{gender:"M",event_code:"800",A:0.13279,Z:235,X:1.85},{gender:"M",event_code:"1500",A:0.03768,Z:480,X:1.85},{gender:"M",event_code:"3000",A:0.0105,Z:1005,X:1.85},{gender:"M",event_code:"5000",A:0.00419,Z:1680,X:1.85},{gender:"M",event_code:"10000",A:0.000415,Z:4245,X:1.9},{gender:"M",event_code:"110H",A:5.74352,Z:28.5,X:1.92},{gender:"M",event_code:"200H",A:3.495,Z:45.5,X:1.81},{gender:"M",event_code:"400H",A:1.1466,Z:92,X:1.81},{gender:"M",event_code:"3000SC",A:0.00511,Z:1155,X:1.9},{gender:"M",event_code:"LJ",A:0.14354,Z:220,X:1.4},{gender:"M",event_code:"TJ",A:0.06533,Z:640,X:1.4},{gender:"M",event_code:"HJ",A:0.8465,Z:75,X:1.42},{gender:"M",event_code:"PV",A:0.2797,Z:100,X:1.35},{gender:"M",event_code:"SP",A:51.39,Z:1.5,X:1.05},{gender:"M",event_code:"HT",A:13.0449,Z:7,X:1.05},{gender:"M",event_code:"DT",A:12.91,Z:4,X:1.1},{gender:"M",event_code:"JT",A:10.14,Z:7,X:1.08},{gender:"M",event_code:"60",A:58.015,Z:11.5,X:1.81},{gender:"M",event_code:"60H",A:20.5173,Z:15.5,X:1.92},{gender:"M",event_code:"WT",A:47.8338,Z:1.5,X:1.05},{gender:"F",event_code:"100",A:17.857,Z:21,X:1.81},{gender:"F",event_code:"200",A:4.99087,Z:42.5,X:1.81},{gender:"F",event_code:"400",A:1.34285,Z:91.7,X:1.81},{gender:"F",event_code:"800",A:0.11193,Z:254,X:1.88},{gender:"F",event_code:"1500",A:0.02883,Z:535,X:1.88},{gender:"F",event_code:"3000",A:0.00683,Z:1150,X:1.88},{gender:"F",event_code:"5000",A:0.00272,Z:1920,X:1.88},{gender:"F",event_code:"10000",A:0.000369,Z:4920,X:1.88},{gender:"F",event_code:"100H",A:9.23076,Z:26.7,X:1.835},{gender:"F",event_code:"200H",A:2.975,Z:52,X:1.81},{gender:"F",event_code:"400H",A:0.99674,Z:103,X:1.81},{gender:"F",event_code:"3000SC",A:0.00408,Z:1320,X:1.9},{gender:"F",event_code:"LJ",A:0.188807,Z:210,X:1.41},{gender:"F",event_code:"TJ",A:0.08559,Z:600,X:1.41},{gender:"F",event_code:"HJ",A:1.84523,Z:75,X:1.348},{gender:"F",event_code:"PV",A:0.44125,Z:100,X:1.35},{gender:"F",event_code:"SP",A:56.0211,Z:1.5,X:1.05},{gender:"F",event_code:"HT",A:17.5458,Z:6,X:1.05},{gender:"F",event_code:"DT",A:12.331,Z:3,X:1.1},{gender:"F",event_code:"JT",A:15.9803,Z:3.8,X:1.04},{gender:"F",event_code:"60",A:46.0849,Z:13,X:1.81},{gender:"F",event_code:"60H",A:20.0479,Z:17,X:1.835},{gender:"F",event_code:"WT",A:52.1403,Z:1.5,X:1.05}];
function _iaaf_scoring_objects_create(){
	if(typeof _iaaf_scoring_objects=="undefined"){
		var o,n=_iaaf_scoring_table.length,i;
		_iaaf_scoring_objects = {};
		for(i=0;i<n;i++){
			o=_iaaf_scoring_table[i];
			_iaaf_scoring_objects[iaaf_scoring_key(o.gender,o.event_code)] = o;
			}
		}
	}
var iaaf_score = function(gender,event_code,value){
	_iaaf_scoring_objects_create();
	function fnew(gender,event_code,value){
		var coeffs=_iaaf_scoring_objects[iaaf_scoring_key(gender,event_code)];
		if(!coeffs) return null;
		if(event_code.match(_iaaf_jump_codes) || event_code.match(_iaaf_throw_codes)){
			return coeffs.A*Math.pow(value-coeffs.Z,coeffs.X)
			}
		return coeffs.A*Math.pow(coeffs.Z-value,coeffs.X);
		}
	iaaf_score = fnew;
	return iaaf_score(gender,event_code,value);
	}
function iaaf_unit_name(event_code){
	return event_code.match(_iaaf_jump_codes)?'centimetres':(event_code.match(_iaaf_throw_codes)?'metres':'seconds');
	}

function iaaf_performance(gender,event_code,score){
	//returns the value that creates the given score ie invert iaaf_score
	_iaaf_scoring_objects_create();
	function fnew(gender,event_code,score){
		var coeffs=_iaaf_scoring_objects[iaaf_scoring_key(gender,event_code)];
		if(!coeffs) return null;
		if(event_code.match(_iaaf_jump_codes) || event_code.match(_iaaf_throw_codes)){
			return (Math.pow(score/coeffs.A,1.0/coeffs.X)) + coeffs.Z;
			}
		return coeffs.Z-(Math.pow(score/coeffs.A,1.0/coeffs.X));
		}
	iaaf_performance = fnew;
	return iaaf_performance(gender,event_code,score);
	}
