from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter
from source.phrase_writer import PhraseWriter

class whenUsingEnglishPhraseWriter(ExtendedTestCase):
    def setUp(self):
        self.summaryWriter = SummaryWriter()
        self.phraseWriter = PhraseWriter.inLanguage('en')
        self.summaryWriter.setPhraseWriterTo(self.phraseWriter)
    
    def test_whenWritingSectionForFather(self):
        """Tests whether the summary writer puts out a correct section
        centred around the father of a baptism entry given the expected
        output of the file parser."""
        self.summaryWriter.setPeopleTo(FATHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['default'])
        
    def test_whenWritingSectionForMother(self):
        """Tests whether the summary writer puts out a correct section
        centred around the mother of a baptism entry given the expected
        output of the file parser."""
        self.summaryWriter.setPeopleTo(MOTHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTINGS['default'])
        
    def test_whenWritingSectionForFatherForOtherChild(self):
        """Tests whether the summary writer can also put out a section
        centred around the father of a baptism entry given a different 
        child."""
        peopleData = {**FATHER_INPUT,'children':[HERMAN_INPUT]}
        self.summaryWriter.setPeopleTo(peopleData)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+OTHER_CHILD_LISTING)
        
    def test_whenWritingSectionForFatherOfBothChildren(self):
        """Tests whether the summary writer put out a section centred
        around the father in two baptism entries. Combining previous
        tests for each seperate child."""
        peopleData = {'main':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder','gender':'m'},
                      'spouse':{'PID':'x1(Fr0)','firstName':'Alheid'},
                      'children':[WOLTER_INPUT,HERMAN_INPUT]}
        self.summaryWriter.setPeopleTo(peopleData)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,COMBINED_CHILDREN_LISTING)
        
    def test_whenBaptismSourceHasDifferentChurchDenomination(self):
        """Tests whether the summary writer puts out a section based on 
        a child baptism record for other than just the catholic denomination."""
        childData  = {**WOLTER_INPUT,'denom':['ref']}
        peopleData = {**FATHER_INPUT,'children':[childData]}
        self.summaryWriter.setPeopleTo(peopleData)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['reformed church'])

    def test_whenBaptismSourceHasMultipleChurchDenomination(self):
        """Tests whether the summary writer puts out a section based on 
        a child baptism record in case a child was baptised (on the same date)
        befor both the catholic and the reformed faith."""
        childData  = {**WOLTER_INPUT,'denom':['rc','ref']}
        peopleData = {**FATHER_INPUT,'children':[childData]}
        self.summaryWriter.setPeopleTo(peopleData)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['both churches'])    
        
    def test_whenWritingSecondSection(self):
        """This test asserts that the second section can be written, sub tests will be split of
        and this test will remain as acceptance test."""
        self.summaryWriter.setPeopleTo(TEST_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,TEST_OUTPUT)          

WOLTER_INPUT = {'PID':'(Fr0.1)','firstName':'Wolterus','day':18,'month':12,'year':1661, 'nameOfParish':'St. Vitus','denom':['rc']}
HERMAN_INPUT = {'PID':'(Fr0.2)','firstName':'Hermännus','day':1,'month':6,'year':1666, 'nameOfParish':'St. Vitus','denom':['rc']}        
        
MOTHER_INPUT = {'main':{'PID':'x1(Fr0)','firstName':'Alheid','gender':'v'},
                'spouse':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder'},
                'children':[WOLTER_INPUT]}  

FATHER_INPUT = {'main':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder','gender':'m'},
                'spouse':{'PID':'x1(Fr0)','firstName':'Alheid'},'children':[WOLTER_INPUT]} 
        
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

TEST_INPUT = {'main':{'PID':'(Fr1)','firstName':'Jan','lastName':'Sunder','gender':'m'},
              'spouse':{'PID':'x1(Fr1)','firstName':'Tela','lastName':'Mouwe'},
              'children':[{'PID':'(Fr1.1)','firstName':'Jan','day':13,'month':12,'year':1711,
                           'nameOfParish':'St. Vitus','gender':'m','denom':['rc','ref']}]} 

TEST_OUTPUT = """
\section{\pidt{(Fr1)}-- Sunder, Jan --~\Mars}\label{sec:(Fr1)}

From a relationship between Jan \textbf{S}under\pids{(Fr1)} and Tela \textbf{M}ouwe\pids{x1(Fr1)} was brought forth:
\begin{itemize}
\item[\emph{\rom{1}.}] Jan~(\textbf{\Mars})~\pids{(Fr1.1)} was baptised on the 13\supscr{th} of December 1711 before the catholic church of the {\it St. Vitus} parish and the reformed church, both at Freren.
\end{itemize}
"""