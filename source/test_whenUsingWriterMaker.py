from source.extended_testcase import ExtendedTestCase

from source.writer_adapter import WriterAdapter
from source.writer_maker import WriterMaker
from source.record_data import WriterData

class whenUsingWriterMaker(ExtendedTestCase):
    def test_whenWritingTemplateWithAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        peopleDataDict = {'date':{'day':'1','month':'2','year':'1823'}}
        expectedOutput = 'on the 1\supscr{st} of February 1823'
        summaryWriter = WriterAdapter.forTemplatePattern('$onTheDate(date)')
        writerMaker  = WriterMaker.inLanguage('en')
        summaryWriter.setMakerTo(writerMaker)
        actualOutput = summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        
    def test_whenWritingDayWithOnlyDayAsAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        self.__doTestWhenWritingDayWithOnlyDayAsAttribute(1,'st') 
        
    def test_whenWritingDayWithOnlyDayZeroAsAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        self.__doTestWhenWritingDayWithOnlyDayAsAttribute(0,'th') 
        
    def test_whenWritingDayWithOnlyDayFourAsAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        self.__doTestWhenWritingDayWithOnlyDayAsAttribute(4,'th')
        
    def __doTestWhenWritingDayWithOnlyDayAsAttribute(self,day,ordinal):
        peopleDataDict = {'date':{'day':day}}
        expectedOutput = '%d\supscr{%s}'%(day,ordinal)
        summaryWriter = WriterAdapter.forTemplatePattern('$dayOrdinal(+day)')
        writerMaker  = WriterMaker.inLanguage('en')
        summaryWriter.setMakerTo(writerMaker)
        actualOutput = summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        