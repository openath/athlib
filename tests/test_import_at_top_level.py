import os, sys, re, inspect
from unittest import main, skipIf
from runall import AthlibTestCase
from athlib.utils import localpath, lexec

def have_docs():
    path = localpath(os.path.join('docs', 'source', 'athlib.rst'))
    if os.path.isfile(path):
        return path

class ImportTest(AthlibTestCase):

    @classmethod
    def setUpClass(cls):
        AthlibTestCase.setUpClass()
        path = have_docs()
        if path:
            with open(path, 'r') as f:
                cls.text = f.read()
        else:
            cls.text = None

    @skipIf(not have_docs(),'no docs found')
    def test_primitive_imports(self):
        marker = ':members:'
        ML = self.text[self.text.index(
            marker) + len(':marker:') + 1:].split('\n')
        members = []
        for line in ML:
            line = ''.join(line.split())
            if not line:
                break
            members.extend(filter(None, line.split(',')))

        failures = []
        for member in members:
            try:
                lexec("from athlib import %s" % member)
            except ImportError:
                failures.append(member)
        self.assertTrue(not failures, "These documented members could not"
                        "be imported from athlib\n %s"
                        % ' \n'.join(failures))

    @skipIf(not have_docs(),'no docs found')
    def test_athlib_all_is_mentioned(self):
        import athlib
        failures = []
        for member in athlib.__all__:
            if not re.search(r'\W' + member + r'\W', self.text, re.M):
                failures.append(member)
        self.assertTrue(not failures,
                        "These athlib members are not documented "
                        "in docs/source/athlib.rst\n %s"
                        % '\n '.join(failures))

    fakers = [
            # ('wma_age_grade','ag2015','calculate_age_grade'),
            # ('wma_age_factor','ag2015','calculate_factor'),
            # ('wma_world_best','ag2015','world_best'),
            ('wma_athlon_age_grade','aag','calculate_age_grade'),
            ('wma_athlon_age_factor','aag','calculate_factor'),
            ]
    def test_fake_doc_strings(self):
        failures = []
        def bad_test(a,b):
            ad = ' '.join(a.__doc__.split())
            bd = ' '.join(b.__doc__.split())
            if not ad.startswith(bd):
                return ad, bd
        for faker, obj, meth in self.fakers:
            ns = {}
            lexec('from athlib import %s as faker' % faker,ns)
            lexec('from athlib import %s as obj' % obj, ns)
            bad = bad_test(getattr(ns['obj'],meth),ns['faker'])
            if bad:
                failures.append('athlib.%s.__doc__ does not start like athlib.%s.%s.__doc__\n  %r\n %r...' %(faker,obj,meth,bad[1],bad[0][:len(bad[1])]))
        self.assertTrue(not failures,'athlib member __doc__ failures\n %s' % '\n '.join(failures))

    def test_fake_signatures(self):
        failures = []
        def bad_test(a,b):
            asig = getattr(inspect,'getfullargspec',inspect.getargspec)(a)
            del asig.args[0]
            bsig = getattr(inspect,'getfullargspec',inspect.getargspec)(b)
            if asig!=bsig:
                return asig,bsig

        for faker, obj, meth in self.fakers:
            ns = {}
            lexec('from athlib import %s as faker' % faker,ns)
            lexec('from athlib import %s as obj' % obj, ns)
            bad = bad_test(getattr(ns['obj'],meth),ns['faker'])
            if bad:
                failures.append('athlib.%s has signature\n  %r\nnot the expected\n  %r' % (faker,bad[1],bad[0]))
        self.assertTrue(not failures,'athlib member signature failures\n %s' % '\n '.join(failures))

if __name__ == '__main__':
    main()
