/* global __dirname, require, module*/
const webpack = require('webpack');
const path = require('path');
const pkg = require('./package.json');
const CWP = require('clean-webpack-plugin');
const write = require('write');

module.exports = function (env) {
	const libraryName = pkg.name;
	const isProd  = env.prod === 1;
	write.sync(__dirname + '/src/version.js', "const version = '"+pkg.version+"';\n\nmodule.exports = {version};\n");
	const config = {
		mode: isProd ? 'production' : 'development',
		entry: __dirname + '/src/athlib.js',
    devtool: 'source-map',
		output: {
			path: __dirname + '/dist',
			filename: libraryName + '.web.js',
			library: libraryName,
			libraryTarget: 'umd',
			umdNamedDefine: true,
			globalObject: "typeof self !== 'undefined' ? self : this"
		},
		module: {
			rules: [
				{
					test: /(\.jsx|\.js)$/,
					loader: 'babel-loader',
					exclude: /(node_modules|bower_components)/
				},
				{
					test: /(\.jsx|\.js)$/,
					loader: 'eslint-loader',
					exclude: /node_modules/
				}
			]
		},
    optimization: {minimize: isProd},
    plugins: [],
		resolve: {
			modules: [path.resolve('./node_modules'), path.resolve('./src')],
			extensions: ['.json', '.js']
		}
	}
	var cwp = CWP;
	if (cwp.hasOwnProperty('CleanWebpackPlugin')) cwp = cwp.CleanWebpackPlugin;
  config.plugins.push(new cwp());
	return config;
}
