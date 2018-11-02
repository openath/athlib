Athlib Javascript
=================

This is the athlib.js library containing code related to athletics. The node version is inlib, the web version is in dist.


ES6 library
===========

This repository contains ES6 code and tests.


## Detailed overview

### Installation
After cloning this repository, make sure to change all the relevant entries in `package.json` so they match your library.
```sh
npm install
```

### Build for the web
```sh
npm run build
```
This will:
 1. run vue-service build on src/athlib.js to create minified dist/athlib.umd.min.js and associated maps suitable for web.
 2. rename the outputs to dist/athlib.web.js & dist/athlib.web.js.map
 3. run jest tests/*.spec.js using dist/athlib.web.js as library.


### Build for web
```sh
npm run build-node
```
This will:
 1. run vue-service build on src/athlib.js to create lib/athlib.common.js and associated maps suitable for commonjs environment.
 2. rename the outputs to lib/athlib.js & lib/athlib.js.map
 3. run jest tests/*.spec.js using lib/athlib.js as library.

### Tests
```sh
npm run test
```
This runs jest tests on the source
```sh
npm run test-dist
```
This runs jest tests on dist/athlib.web.js
```sh
npm run test-node
```
This runs jest tests on dist/athlib.js

### Other commands
```sh
npm run lint
```
show up your errors

```sh
npm run lint-fix
```
show up your errors & try to fix them

```sh
npm run clean
```
clean out lib & dist and any jest cache

```sh
npm run dist-clean
```
clean more thoroughly (removes node_modules)

### Configuration
if you want to adapt for your library change all the relevant entries in `package.json` so they match your library.<br/>
Under the section `library`, you can configure:
 1. Library name (defaults to `"Library"`)
 2. Webpack entry point (defaults to `library.js`)
 3. Dist folder for Node (defaults to `lib`)
 4. Dist folder for Web (defaults to `dist`)

## License
Apache-2.0
