var testSrc=process.env.TESTSRC;
var pkg = require('./package.json');
var name = pkg.name;
var libFile = './dist/'+(pkg.library['bundle-web'] ? pkg.library['dist-web'] : pkg.library['entry']);
export default {require(libFile)};
console.log('======================= testSrc:',testSrc, 'libFile:', libFile,'module.exports:',module.exports);
