Athlib Javascript
=================

This is the athlib.js library containing code related to athletics. The node version is inlib, the web version is in dist.


ES6 library
===========

This repository contains ES6 code and tests.


## Detailed overview

### Installation
After cloning this repository, make changes in `package.json` so they match your ideas.
```sh
#optionally rm -rf package-lock.json node_modules
npm install --no-optional   #ignore warnings
npm audit
```

### Build and test the library in umd production format
```sh
npm run build  #produces dist/athlib.web.js
```

### Build and test the library in umd debug format
```sh
npm run build-debug  #produce dist/athlib.web.js.map as well
```

### Build the library in umd debug format
```sh
npm run build-debug-only
```

### Watch and rebuild the library in umd production format
```sh
npm run dev    #no testing just watches and rebuilds
```

### Check formatting with eslint
```sh
npm run eslint
```

### Check and fix formatting with eslint
```sh
npm run eslint-fix
```

### Tests web code in node mode
```sh
npm run test-node
```

### Watches and tests web code
```sh
npm run test:watch
```

### Produce a test coverage report
```sh
npm run test:cover
```

### Run a node repl on dist/athlib.web.js
```sh
npm run repl
```

## License
Apache-2.0
