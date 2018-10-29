module.exports = {
    mode: "production",
    entry: "src/library.js",
    output: {
        path: __dirname+'/dist',
        filename: "athlib.web.js",
        //filename: `${moduleName}.js`,
        library: 'Athlib',
        libraryExport: 'Athlib',
        libraryTarget: 'var',
        umdNamedDefine: false
      },
    "devtool": "source-map",
    "module": {
        "rules": [
            {
                "test": /\.js$/,
                "exclude": /node_modules/,
                "use": {
                    "loader": "babel-loader",
                    "options": {
                        "presets": [
                            "@babel/env"
                        ]
                    }
                }
            }
        ]
    }
}
