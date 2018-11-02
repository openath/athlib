module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: ["plugin:vue/essential", "@vue/prettier"],
  rules: {
		"vue/no-invalid-v-for": "off",
		//"prettier/prettier": "off",
    "no-console": process.env.NODE_ENV === "production" ? "error" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off"
  },
  parserOptions: {
    parser: "babel-eslint"
  }
};
