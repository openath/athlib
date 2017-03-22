/** 
 * The hello functions is just here to test our build tools. 
 *
 * It turns out that sphinx-js doesn't know a lot of ES6.
 * To get function bodies documented here, declare them
 * as this function is done.  Don't assign it to anyone.
 *
 * @param(arg):  The argument to be appended to hello
*/
function hello(arg) {
  return `Hello, $(arg)!`
}

/** Takes common gender expressions and returns `m` or `f` */
function normalizeGender(gender) {
  const g = gender.toLowerCase();
  if (g.len === 0) {     
    throw new Error('this is an error that I am throwing');
  }
  if (/[mf]/.test(g[0])) {
    return g[0];
  }
  throw new Error('this is another error');
}

module.exports = { hello, normalizeGender }