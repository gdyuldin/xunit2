from nose.plugins import Plugin
from nose.plugins.xunit import Xunit, id_split, format_exception, nice_classname, exc_message, escape_cdata
from nose.exc import SkipTest


class Xunit2(Xunit):

    name = 'xunit2'

    def options(self, parser, env):
        """Sets additional command line options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            '--xunit2-file', action='store',
            dest='xunit_file', metavar="FILE",
            default=env.get('NOSE_XUNIT_FILE', 'nosetests.xml'),
            help=("Path to xml file to store the xunit report in. "
                  "Default is nosetests.xml in the working directory "
                  "[NOSE_XUNIT_FILE]"))

        parser.add_option(
            '--xunit2-testsuite-name', action='store',
            dest='xunit_testsuite_name', metavar="PACKAGE",
            default=env.get('NOSE_XUNIT_TESTSUITE_NAME', 'nosetests'),
            help=("Name of the testsuite in the xunit xml, generated by plugin. "
                  "Default test suite name is nosetests."))

    def get_doc(self, test):
        doc = test.test._testMethodDoc
        if doc is not None:
            doc = doc.strip()
            return ":%s" % doc
        else:
            return ""

    def addError(self, test, err, capt=None):
        """Add error output to Xunit report.
        """
        taken = self._timeTaken()

        if issubclass(err[0], SkipTest):
            type = 'skipped'
            self.stats['skipped'] += 1
        else:
            type = 'error'
            self.stats['errors'] += 1

        tb = format_exception(err, self.encoding)
        id = test.id()
        doc = self.get_doc(test)

        self.errorlist.append(
            u'<testcase classname=%(cls)s name=%(name)s time="%(taken).3f">'
            u'<%(type)s type=%(errtype)s message=%(message)s><![CDATA[%(tb)s]]>'
            u'</%(type)s>%(systemout)s%(systemerr)s</testcase>' %
            {'cls': self._quoteattr(id_split(id)[0]),
             'name': self._quoteattr(id_split(id)[-1] + doc),
             'taken': taken,
             'type': type,
             'errtype': self._quoteattr(nice_classname(err[0])),
             'message': self._quoteattr(exc_message(err)),
             'tb': escape_cdata(tb),
             'systemout': self._getCapturedStdout(),
             'systemerr': self._getCapturedStderr(),
             })

    def addFailure(self, test, err, capt=None, tb_info=None):
        """Add failure output to Xunit report.
        """
        taken = self._timeTaken()
        tb = format_exception(err, self.encoding)
        self.stats['failures'] += 1
        id = test.id()
        doc = self.get_doc(test)

        self.errorlist.append(
            u'<testcase classname=%(cls)s name=%(name)s time="%(taken).3f">'
            u'<failure type=%(errtype)s message=%(message)s><![CDATA[%(tb)s]]>'
            u'</failure>%(systemout)s%(systemerr)s</testcase>' %
            {'cls': self._quoteattr(id_split(id)[0]),
             'name': self._quoteattr(id_split(id)[-1] + doc),
             'taken': taken,
             'errtype': self._quoteattr(nice_classname(err[0])),
             'message': self._quoteattr(exc_message(err)),
             'tb': escape_cdata(tb),
             'systemout': self._getCapturedStdout(),
             'systemerr': self._getCapturedStderr(),
             })

    def addSuccess(self, test, capt=None):
        """Add success output to Xunit report.
        """
        taken = self._timeTaken()
        self.stats['passes'] += 1
        id = test.id()
        doc = self.get_doc(test)
        self.errorlist.append(
            '<testcase classname=%(cls)s name=%(name)s '
            'time="%(taken).3f">%(systemout)s%(systemerr)s</testcase>' %
            {'cls': self._quoteattr(id_split(id)[0]),
             'name': self._quoteattr(id_split(id)[-1] + doc),
             'taken': taken,
             'systemout': self._getCapturedStdout(),
             'systemerr': self._getCapturedStderr(),
             })