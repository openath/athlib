import os, sys, re
from unittest import main
from runall import localpath, lexec, AthlibTestCase

class ImportTest(AthlibTestCase):

	@classmethod
	def setUpClass(cls):
		AthlibTestCase.setUpClass()
		with open(localpath(os.path.join('docs','source','athlib.rst')),'r') as f:
			cls.text = f.read()

	def test_primitive_imports(self):
		marker = ':members:'
		ML = self.text[self.text.index(marker)+len(':marker:')+1:].split('\n')
		members = []
		for line in ML:
			line = ''.join(line.split())
			if not line: break
			members.extend(filter(None,line.split(',')))

		failures = []
		for member in members:
			try:
				lexec("from athlib import %s" % member)
			except ImportError:
				failures.append(member)
		self.assertTrue(not failures,"These documented members could not be imported from athlib\n %s"
				%' \n'.join(failures))
				
	def test_athlib_all_is_mentioned(self):
		import athlib
		failures = []
		for member in athlib.__all__:
			if not re.search(r'\W'+member+r'\W',self.text,re.M):
				failures.append(member)
		self.assertTrue(not failures,"These athlib members ould not be found in docs/source/athlib.rst\n %s"
				% '\n '.join(failures))

if __name__ == '__main__':
	main()
