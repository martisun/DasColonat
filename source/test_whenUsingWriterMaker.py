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
        dataDict = {'children':getTestInput()['children']}
        childrenListing = self.__getChildDescriptionListingGivenDataDict(dataDict)
        expectedChildrenListing = self.__getExpectedChildDescriptionListingGivenDataDict(dataDict)
        self._assertActualEqualsExpected(childrenListing,expectedChildrenListing)   
    
    def test_whenWritingChildDescriptionListingWithIntro(self):
        """Tests whether a child description listing with intro can be printed given 
        two children and their parents name entries. """
        dataDict = getTestInput()
        childrenListing = self.__getChildDescriptionListingWithIntroGivenDataDict(dataDict)
        expectedChildrenListing =\
                  self.__getExpectedChildDescriptionListingWithIntroGivenDataDict(dataDict)
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
    
    def __getChildDescriptionListingWithIntroGivenDataDict(self,dataDict):
        summaryWriter = self.__getTestSummaryWriterForTemplate('$childDescriptionWithIntro(all)')
        return summaryWriter.write(dataDict)     
    
    def __getExpectedChildDescriptionListingGivenDataDict(self,dataDict):
        firstChildOutput = self.__getChildDescriptionClauseOutputGivenDataDict(
            dataDict['children'][0])
        secondChildOutput = self.__getChildDescriptionClauseOutputGivenDataDict( 
            dataDict['children'][1])
        return CHILDREN_LISTING%(firstChildOutput,secondChildOutput)
        
    def __getExpectedChildDescriptionListingWithIntroGivenDataDict(self,dataDict):
        writer = self.__getTestSummaryWriterForTemplate('$childListingIntro(main,spouse,children)')
        childrenListingIntro = writer.write(dataDict)
        childrenListing = self.__getChildDescriptionListingGivenDataDict(dataDict)
        return childrenListingIntro+childrenListing
        
    def __getTestSummaryWriterForTemplate(self,templateText):
        summaryWriter = WriterAdapter.forTemplatePattern(templateText)
        writerMaker  = WriterMaker.inLanguage('test')
        summaryWriter.setMakerTo(writerMaker)
        return summaryWriter
        
SINGLE_BAPTISM_ENTRY_CHILD = {'main':{'PID':'(Fr1.1.1)','foreNames':'Thele Marie','gender':'f',
                              'date':[{'day':18,'month':9,'year':1734}],
                              'denom':['ref']}}
        
DOUBLE_BAPTISM_ENTRY_CHILD = {'main':{'PID':'(Fr1.1.2)','foreNames':'Bernardus','gender':'m',
                              'date':[{'day':30,'month':8,'year':1736},
                                      {'day':31,'month':8,'year':1736}],
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
\item[\emph{\rom{3}.}] Maria~(\textbf{\Venus})~\pids{(Fr1.1.3)} was baptised on the 6\supscr{th} of December 1738 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\item[\emph{\rom{4}.}] Joh. Christoph~(\textbf{\Mars})~\pids{(Fr1.1.4)} was baptised on the 15\supscr{th} of January 1741 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\item[\emph{\rom{5}.}] Joannis~(\textbf{\Mars})~\pids{(Fr1.1.5)} was baptised on the 8\supscr{th} of September 1743 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\item[\emph{\rom{6}.}] Henricus~(\textbf{\Mars})~\pids{(Fr1.1.6)} was baptised on the 17\supscr{th} of November 1747 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\end{itemize}"""

FATHER_ENTRY = {'PID':'(Fr1.1)','foreNames':'Jan','lastName':'Sunder','gender':'m',
                'date':[{'day':13,'month':12,'year':1711}],
                'nameOfParish':'St. Vitus','denom':['rc','ref']}

MOTHER_ENTRY = {'PID':'x1(Fr1.1)','foreNames':'Anna Maria','lastName':'Tijs','gender':'f',
                'date':{'day':8,'month':7,'year':1712},'denom':['ref'],
                'father':{'foreNames':'Herman','lastName':'Tijs'},
                'mother':{'foreNames':'Fenne','lastName':'Wemerschlage'}}

FILLED_OUT_CHILDREN_LISTING = CHILDREN_LISTING%(SINGLE_BAPTISM_CHILD_DESCRIPTION,
         ADD_DOUBLE_BAPTISM_CHILD_DESCRIPTION+DOUBLE_BAPTISM_BAPTISM_ONLY_CLAUSE)

def getTestInput():
    return {'main':FATHER_ENTRY,'spouse':MOTHER_ENTRY,
            'father':{'PID':'(Fr1)','foreNames':'Jan','lastName':'Sunder'},
            'mother':{'PID':'x1(Fr1)','foreNames':'Tela','lastName':'Mouwe'},
            'children':[SINGLE_BAPTISM_ENTRY_CHILD['main'], 
                        DOUBLE_BAPTISM_ENTRY_CHILD['main'],
                        {'PID':'(Fr1.1.3)','foreNames':'Maria','gender':'f',
                         'date':{'day':6,'month':12,'year':1738},
                         'nameOfParish':'St. Vitus','denom':['rc','ref']},
                        {'PID':'(Fr1.1.4)','foreNames':'Joh. Christoph','gender':'m',
                         'date':{'day':15,'month':1,'year':1741},
                         'nameOfParish':'St. Vitus','denom':['rc','ref']},
                        {'PID':'(Fr1.1.5)','foreNames':'Joannis','gender':'m',
                         'date':{'day':8,'month':9,'year':1743},
                         'nameOfParish':'St. Vitus','denom':['rc','ref']},
                        {'PID':'(Fr1.1.6)','foreNames':'Henricus','gender':'m',
                         'date':{'day':17,'month':11,'year':1747},
                         'nameOfParish':'St. Vitus','denom':['rc','ref']}]}