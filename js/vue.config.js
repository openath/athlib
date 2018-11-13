module.exports = {
	filenameHashing: false,
	configureWebpack: {
		output: {
			//filename: "athlib.web.js",
			//library: 'athlib',
		}
	}
}
module.exports['chainWebpack'] = config => {
  if(process.env.NOSPLITCHUNKS==='1') config.optimization.splitChunks(false);
	config.output.filename = "athlib.web.js";
}
