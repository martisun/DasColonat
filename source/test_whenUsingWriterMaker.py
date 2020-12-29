from source.extended_testcase import ExtendedTestCase

from source.writer_adapter import WriterAdapter
from source.writer_maker import WriterMaker
from source.record_data import WriterData

class whenUsingWriterMaker(ExtendedTestCase):
    def test_whenWritingTemplateWithAttribute(self):
        """Tests whether a template is accessible with a person
        attribute."""
        dataDict = {'date':{'day':'1','month':'2','year':'1823'}}
        self.__doTestWhenWritingTemplateWithDateAttribute(dataDict)
        
    def test_whenWritingTemplateWithLengthOneListAttribute(self):
        """Tests whether a template is accessible with a person
        attribute dict of list of length one."""
        dataDict = {'date':[{'day':'1','month':'2','year':'1823'}]}
        self.__doTestWhenWritingTemplateWithDateAttribute(dataDict)
        
    def __doTestWhenWritingTemplateWithDateAttribute(self,dataDict):    
        expectedOutput = 'on the 1\supscr{st} of February 1823'
        self.__assertOutputDateWrittenGivenInputDict(dataDict,expectedOutput)
        
    def test_whenWritingTemplateWithLengthOneListAttribute(self):
        """Tests whether a double date-entry can be printed if provided
        when only the day is differing."""
        dataDict = {'date':[{'day':'30','month':'8','year':'1736'},
                            {'day':'31','month':'8','year':'1736'}]}
        expectedOutput = 'on the 30\supscr{th} and 31\supscr{st} of August 1736'
        self.__assertOutputDateWrittenGivenInputDict(dataDict,expectedOutput)  
        
    def __assertOutputDateWrittenGivenInputDict(self,dataDict,expectedOutput): 
        summaryWriter = self.__getTestSummaryWriterForTemplate('$onTheDate(date)')
        actualOutput = summaryWriter.write(dataDict)
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
        dataDict = {'date':{'day':day}}
        expectedOutput = '%d\supscr{%s}'%(day,ordinal)
        summaryWriter = self.__getTestSummaryWriterForTemplate('$dayOrdinal(+day)')
        actualOutput = summaryWriter.write(dataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        
    def test_whenWritingBaptismClauseWithMultipleDates(self):
        """Tests whether a double date-entry can be printed if provided
        when only the day is differing."""
        actualOutput = self.__getBaptismOnlyClauseOutputGivenDataDict(DOUBLE_BAPTISM_ENTRY_CHILD)
        self._assertActualEqualsExpected(actualOutput,DOUBLE_BAPTISM_BAPTISM_ONLY_CLAUSE) 
        
    def test_whenWritingChildDescriptionWithMultipleDates(self):
        """Tests whether a child description can be printed given a double 
        date-entry with just the date differing."""
        dataDict = DOUBLE_BAPTISM_ENTRY_CHILD
        baptismOnlyOutput      = self.__getBaptismOnlyClauseOutputGivenDataDict(dataDict)
        childDescriptionOutput = self.__getChildDescriptionClauseOutputGivenDataDict(dataDict)
        expectedOutput = ADD_DOUBLE_BAPTISM_CHILD_DESCRIPTION+baptismOnlyOutput
        self._assertActualEqualsExpected(childDescriptionOutput,expectedOutput)
        
    def test_whenWritingChildDescriptionWithSingleDate(self):
        """Tests whether a child description can be printed given a single 
        date-entry"""
        dataDict = SINGLE_BAPTISM_ENTRY_CHILD
        childDescriptionOutput = self.__getChildDescriptionClauseOutputGivenDataDict(dataDict)
        self._assertActualEqualsExpected(childDescriptionOutput,SINGLE_BAPTISM_CHILD_DESCRIPTION)
    
    def test_whenWritingChildDescriptionListing(self):
        """Tests whether a child description listing can be printed given two children 
        data-entries. """
        dataDict = {'children':[SINGLE_BAPTISM_ENTRY_CHILD['main'], 
                                DOUBLE_BAPTISM_ENTRY_CHILD['main']]}
        childrenListing = self.__getChildDescriptionListingGivenDataDict(dataDict)
        expectedChildrenListing = self.__getExpectedChildDescriptionListingGivenDataDict(dataDict)
        self._assertActualEqualsExpected(childrenListing,expectedChildrenListing)   
    
    def __getBaptismOnlyClauseOutputGivenDataDict(self,dataDict):
        summaryWriter = self.__getTestSummaryWriterForTemplate('$baptismOnly(main)')
        return summaryWriter.write(dataDict) 
    
    def __getChildDescriptionClauseOutputGivenDataDict(self,dataDict):
        summaryWriter = self.__getTestSummaryWriterForTemplate('$childDescription(main)')
        return summaryWriter.write(dataDict) 
    
    def __getChildDescriptionListingGivenDataDict(self,dataDict):
        summaryWriter = self.__getTestSummaryWriterForTemplate('$childrenListing(children)')
        return summaryWriter.write(dataDict) 
    
    def __getExpectedChildDescriptionListingGivenDataDict(self,dataDict):
        firstChildOutput = self.__getChildDescriptionClauseOutputGivenDataDict( 
            SINGLE_BAPTISM_ENTRY_CHILD)
        secondChildOutput = self.__getChildDescriptionClauseOutputGivenDataDict( 
            DOUBLE_BAPTISM_ENTRY_CHILD)
        return CHILDREN_LISTING%(firstChildOutput,secondChildOutput)
        
    def __getTestSummaryWriterForTemplate(self,templateText):
        summaryWriter = WriterAdapter.forTemplatePattern(templateText)
        writerMaker  = WriterMaker.inLanguage('test')
        summaryWriter.setMakerTo(writerMaker)
        return summaryWriter
        

SINGLE_BAPTISM_ENTRY_CHILD = {'main':{'PID':'(Fr1.1.1)','foreNames':'Thele Marie','gender':'f',
                              'date':[{'day':'18','month':'9','year':'1734'}],
                              'denom':['ref']}}
        
DOUBLE_BAPTISM_ENTRY_CHILD = {'main':{'PID':'(Fr1.1.2)','foreNames':'Bernardus','gender':'m',
                            'date':[{'day':'30','month':'8','year':'1736'},
                                  {'day':'31','month':'8','year':'1736'}],
                            'nameOfParish':'St. Vitus','denom':['rc','ref']}} 

DOUBLE_BAPTISM_BAPTISM_ONLY_CLAUSE = ' was baptised on the 30\supscr{th} and 31\supscr{st}'+\
                         ' of August 1736 before the catholic church of the {\it St. Vitus}'+\
                         ' parish and the reformed church, both at Freren, respectively.'
        
ADD_DOUBLE_BAPTISM_CHILD_DESCRIPTION =  'Bernardus~(\textbf{\Mars})~\pids{(Fr1.1.2)}'       

SINGLE_BAPTISM_CHILD_DESCRIPTION = 'Thele Marie~(\textbf{\Venus})~\pids{(Fr1.1.1)} was baptised on the 18\supscr{th} of September 1734 before the reformed church at Freren.'

CHILDREN_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] %s
\item[\emph{\rom{2}.}] %s
\end{itemize}"""

FILLED_OUT_CHILDREN_LISTING = CHILDREN_LISTING%(SINGLE_BAPTISM_CHILD_DESCRIPTION,
         ADD_DOUBLE_BAPTISM_CHILD_DESCRIPTION+DOUBLE_BAPTISM_BAPTISM_ONLY_CLAUSE)