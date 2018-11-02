var testModulesDir = process.env.npm_lifecycle_event==='unit-tests-dist' ? 'dist' : 'src';
config = {
	moduleFileExtensions: ["js", "jsx", "json", "vue"],
	transform: {
		"^.+\\.vue$": "vue-jest",
		".+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$":
			"jest-transform-stub",
		"^.+\\.jsx?$": "babel-jest"
	},
	moduleNameMapper: {
		"^@/(.*)$": "<rootDir>/"+testModulesDir+"/$1"
	},
	snapshotSerializers: ["jest-serializer-vue"],
	testMatch: [
		"**/test/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)"
	],
	testURL: "http://localhost/"
};
module.exports = config;
