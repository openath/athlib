module.exports = {
	filenameHashing: false,
	configureWebpack: {
		output: {
			filename: "athlib.web.js",
			library: 'Athlib',
      libraryTarget: 'umd',
      umdNamedDefine: true,
			libraryExport: 'athlib'
		}
	}
}
if(process.env.NOSPLITCHUNKS==='1'){
	module.exports['chainWebpack'] = config => {config.optimization.splitChunks(false)}
}
