// copies athlib/VERSION (the one place the version is set) into package.json, which npm and the webpack build read;
// runs before every build script
const fs = require('fs');
const pkg = require('./package.json');
const version = fs.readFileSync(__dirname + '/../athlib/VERSION', 'utf8').trim();
if (pkg.version !== version) {
  pkg.version = version;
  fs.writeFileSync(__dirname + '/package.json', JSON.stringify(pkg, null, 2) + '\n');
}
