from source.extended_testcase import ExtendedTestCase

from source.writer_adapter import WriterAdapter
from source.writer_maker import WriterMaker

class whenUsingWriterMaker(ExtendedTestCase):
    def test_whenWritingTemplateWithAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        peopleDataDict = {'main':{'day':'1','month':'2','year':'1823'}}
        expectedOutput = 'on the 1\supscr{st} of February 1823'
        summaryWriter = WriterAdapter.forTemplatePattern('$onTheDate(main)')
        writerMaker  = WriterMaker.inLanguage('en')
        summaryWriter.setMakerTo(writerMaker)
        actualOutput = summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        
    def test_whenWritingDayWithOnlyDayAsAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        peopleDataDict = {'main':{'day':'1'}}
        expectedOutput = '1\supscr{st}'
        summaryWriter = WriterAdapter.forTemplatePattern('$dayOrdinalTEST(main)')
        writerMaker  = WriterMaker.inLanguage('en')
        summaryWriter.setMakerTo(writerMaker)
        actualOutput = summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)