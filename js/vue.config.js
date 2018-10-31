module.exports = {
	filenameHashing: false,
	configureWebpack: {
		output: {
      libraryTarget: 'umd',
			libraryExport: 'default',
      umdNamedDefine: true
		}
	}
}
if(process.env.NOSPLITCHUNKS==='1'){
	module.exports['chainWebpack'] = config => {config.optimization.splitChunks(false)}
}
