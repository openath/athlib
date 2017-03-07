export default () => (
    {
        entry: './index.js',
        output: {
            path: './dist',
            filename: 'athlib.js',
            libraryTarget: 'umd',
            library: 'athlib'
        },
        externals: {
            'lodash': {
                commonjs: 'lodash',
                commonjs2: 'lodash',
                amd: 'lodash',
                root: '_'
            }
        },
        module: {
            rules: [
                {test: /\.js$/, exclude: /node_modules/, loader: "babel-loader"}
            ]
        },
    }
);