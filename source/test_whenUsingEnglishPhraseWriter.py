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
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING)
        
    def test_whenWritingSectionForMother(self):
        """Tests whether the summary writer puts out a correct section
        centred around the mother of a baptism entry given the expected
        output of the file parser."""
        self.summaryWriter.setPeopleTo(MOTHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTING)
        
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
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+COMBINED_CHILDREN_LISTING)    

WOLTER_INPUT = {'PID':'(Fr0.1)','firstName':'Wolterus','day':18,'month':12,'year':1661}
HERMAN_INPUT = {'PID':'(Fr0.2)','firstName':'Hermännus','day':1,'month':6,'year':1666}        
        
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

CHILD_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""

OTHER_CHILD_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Herm\"{a}nnus~(\textbf{?})~\pids{(Fr0.2)} was baptised on the 1\supscr{st} of June 1666 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""

COMBINED_CHILDREN_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\item[\emph{\rom{2}.}] Herm\"{a}nnus~(\textbf{?})~\pids{(Fr0.2)} was baptised on the 1\supscr{st} of June 1666 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""