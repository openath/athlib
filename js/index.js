var pkg = require('./package.json');
var name = pkg.name;
var libFile = (pkg.library['bundle-web'] ? 'dist/'+pkg.library['dist-web'] : 'lib/'+pkg.library['dist-node']);
export default {require(libFile)};
