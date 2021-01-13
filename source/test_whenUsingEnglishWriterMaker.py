from source.extended_testcase import ExtendedTestCase

from source.writer_adapter import WriterAdapter
from source.writer_maker import WriterMaker

from source.default_settings import getPrimalTestIntermediateInputForFather, getPrimalTestIntermediateInputForMother,PrimalTestOutput 

from source.test_whenUsingWriterMaker import getTestInput,FILLED_OUT_CHILDREN_LISTING

class whenUsingEnglishWriterMaker(ExtendedTestCase):
    def setUp(self):
        self.summaryWriter = WriterAdapter.forTemplatePattern('$summary(all)')
        self.__setSummaryWriterToLanguage('test')
        
    def test_whenWritingSectionForFather(self):
        """Tests whether the summary writer puts out a correct section
        centred around the father of a baptism entry given the expected
        output of the file parser."""
        peopleDataDict = getPrimalTestIntermediateInputForFather()
        expectedOutput = PrimalTestOutput().forFather() 
        actualOutput = self.summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        
    def test_whenWritingSectionForMother(self):
        """Tests whether the summary writer puts out a correct section
        centred around the mother of a baptism entry given the expected
        output of the file parser."""
        peopleDataDict = getPrimalTestIntermediateInputForMother()
        expectedOutput = PrimalTestOutput().forMother() 
        actualOutput = self.summaryWriter.write(peopleDataDict)
        self._assertActualEqualsExpected(actualOutput,expectedOutput)
        
    def test_whenWritingSectionForFatherForOtherChild(self):
        """Tests whether the summary writer can also put out a section
        centred around the father of a baptism entry given a different 
        child."""
        peopleDataDict = getPrimalTestIntermediateInputForFather()
        peopleData = {**peopleDataDict,'children':[HERMAN_INPUT]}
        actual = self.summaryWriter.write(peopleData)
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+OTHER_CHILD_LISTING)
        
    def test_whenWritingSectionForFatherOfBothChildren(self):
        """Tests whether the summary writer put out a section centred
        around the father in two baptism entries. Combining previous
        tests for each seperate child."""
        peopleData = {'main':{'PID':'(Fr0)','foreNames':'Jois','lastName':'Sunder','gender':'m'},
                      'spouse':{'PID':'x1(Fr0)','foreNames':'Alheid'},
                      'children':[WOLTER_INPUT,HERMAN_INPUT]}
        actual = self.summaryWriter.write(peopleData)
        self._assertActualEqualsExpected(actual,COMBINED_CHILDREN_LISTING)
        
    def test_whenBaptismSourceHasDifferentChurchDenomination(self):
        """Tests whether the summary writer puts out a section based on 
        a child baptism record for other than just the catholic denomination."""
        childData  = {**WOLTER_INPUT,'denom':['ref']}
        peopleDataDict = getPrimalTestIntermediateInputForFather()
        peopleData = {**peopleDataDict,'children':[childData]}
        actual = self.summaryWriter.write(peopleData)
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['reformed church'])

    def test_whenBaptismSourceHasMultipleChurchDenomination(self):
        """Tests whether the summary writer puts out a section based on 
        a child baptism record in case a child was baptised (on the same date)
        befor both the catholic and the reformed faith."""
        childData  = {**WOLTER_INPUT,'denom':['rc','ref']}
        peopleDataDict = getPrimalTestIntermediateInputForFather()
        peopleData = {**peopleDataDict,'children':[childData]}
        actual = self.summaryWriter.write(peopleData)
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['both churches']) 
        
    def test_whenParentsRecordedButNoLifeEvent(self):
        """Tests whether the summary writer puts out a section for a child
        with known parents but no other known life-events."""
        peopleData = {'father':{'PID':'(Fr0)','foreNames':'Jois','lastName':'Sunder'},
                      'mother':{'PID':'x1(Fr0)','foreNames':'Alheid'},
                      'main':{'PID':'(Fr0.1)','foreNames':'Wolterus','lastName':'Sunder'}}
        actual = self.summaryWriter.write(peopleData)
        self._assertActualEqualsExpected(actual,CHILD_LISTINGS['no life-events'])         
        
    def test_whenWritingSecondSection(self):
        """This test asserts that the second section can be written, sub tests will be split of
        and this test will remain as acceptance test."""
        actual = self.summaryWriter.write(TEST_INPUT['(Fr1)'])
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1)'])  
        
    def test_whenWritingThirdSection(self):
        """This test asserts that the third section can be written, sub tests will be split of
        and this test will remain as acceptance test."""
        actual = self.summaryWriter.write(getTestInput())
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1.1)'])
        
    def __setSummaryWriterToLanguage(self,languageTag):
        writerMaker  = WriterMaker.inLanguage(languageTag)
        self.summaryWriter.setMakerTo(writerMaker)
        

WOLTER_INPUT = {'PID':'(Fr0.1)','foreNames':'Wolterus',
                'date':{'day':18,'month':12,'year':1661},
                'nameOfParish':'St. Vitus','denom':['rc']}
HERMAN_INPUT = {'PID':'(Fr0.2)','foreNames':'Hermännus',
                'date':{'day':1,'month':6,'year':1666},
                'nameOfParish':'St. Vitus','denom':['rc']}
        
FATHER_OUTPUT="""
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

From a relationship between Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)} was brought forth:"""  

MOTHER_OUTPUT="""
\section{\pidt{x1(Fr0)}-- Alheid --~\Venus}\label{sec:x1(Fr0)}

From a relationship between Alheid\pids{x1(Fr0)} and Jois \textbf{S}under\pids{(Fr0)} was brought forth:"""

CHILD_LISTINGS = {
    'default':"""
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
""",'reformed church':"""
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the reformed church at Freren.
\end{itemize}
""",'both churches':"""
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\end{itemize}
""",'no life-events':"""
\section{\pidt{(Fr0.1)}-- Sunder, Wolterus --~?}\label{sec:(Fr0.1)}

Wolterus \textbf{S}under\pids{(Fr0.1)} is a child of Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)}.
"""}

OTHER_CHILD_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Herm\"{a}nnus~(\textbf{?})~\pids{(Fr0.2)} was baptised on the 1\supscr{st} of June 1666 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""

COMBINED_CHILDREN_LISTING = """
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

From a relationship between Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)} were brought forth:
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\item[\emph{\rom{2}.}] Herm\"{a}nnus~(\textbf{?})~\pids{(Fr0.2)} was baptised on the 1\supscr{st} of June 1666 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""

TEST_INPUT = {'(Fr1)':{'main':{'PID':'(Fr1)','foreNames':'Jan','lastName':'Sunder','gender':'m'},
              'spouse':{'PID':'x1(Fr1)','foreNames':'Tela','lastName':'Mouwe'},
              'children':[{'PID':'(Fr1.1)','foreNames':'Jan','gender':'m',
                           'date':{'day':13,'month':12,'year':1711},
                           'nameOfParish':'St. Vitus','denom':['rc','ref']},
                          {'PID':'(Fr1.2)','foreNames':'Maria Elisabet','gender':'f',
                           'date':{'day':8,'month':7,'year':1714},'denom':['ref']},
                          {'PID':'(Fr1.3)','foreNames':'Berend','gender':'m',
                           'date':{'day':31,'month':5,'year':1717},'denom':['ref']},
                          {'PID':'(Fr1.4)','foreNames':'Berend','gender':'m',
                           'date':{'day':12,'month':2,'year':1719},'denom':['ref']}]},
             '(Fr1.1)':getTestInput()} 

TEST_OUTPUT = {'(Fr1)':"""
\section{\pidt{(Fr1)}-- Sunder, Jan --~\Mars}\label{sec:(Fr1)}

From a relationship between Jan \textbf{S}under\pids{(Fr1)} and Tela \textbf{M}ouwe\pids{x1(Fr1)} were brought forth:
\begin{itemize}
\item[\emph{\rom{1}.}] Jan~(\textbf{\Mars})~\pids{(Fr1.1)} was baptised on the 13\supscr{th} of December 1711 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\item[\emph{\rom{2}.}] Maria Elisabet~(\textbf{\Venus})~\pids{(Fr1.2)} was baptised on the 8\supscr{th} of July 1714 before the reformed church at Freren.
\item[\emph{\rom{3}.}] Berend~(\textbf{\Mars})~\pids{(Fr1.3)} was baptised on the 31\supscr{st} of May 1717 before the reformed church at Freren.
\item[\emph{\rom{4}.}] Berend~(\textbf{\Mars})~\pids{(Fr1.4)} was baptised on the 12\supscr{th} of February 1719 before the reformed church at Freren.
\end{itemize}
""",
              '(Fr1.1)':"""
\section{\pidt{(Fr1.1)}-- Sunder, Jan --~\Mars}\label{sec:(Fr1.1)}

Jan \textbf{S}under\pids{(Fr1.1)}, son of Jan \textbf{S}under\pids{(Fr1)} and Tela \textbf{M}ouwe\pids{x1(Fr1)}, was baptised on the 13\supscr{th} of December 1711 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.

From a relationship between Jan \textbf{S}under\pids{(Fr1.1)} and Anna Maria \textbf{T}ijs\pids{x1(Fr1.1)} were brought forth:%s
His spouse Anna Maria \textbf{T}ijs\pids{x1(Fr1.1)}, daughter of Herman \textbf{T}ijs and Fenne \textbf{W}emerschlage, was baptised on the 8\supscr{th} of July 1712 before the reformed church at Freren.
"""%FILLED_OUT_CHILDREN_LISTING}