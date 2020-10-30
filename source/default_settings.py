DEFAULT_TEST_SETTINGS_DATA = {'filesToLoadFrom':['baptism.csv'],\
                              'filesToSaveTo':'summary.tex'}

PRIMAL_TEST_HEADER_DATA = 'father;;;mother;;infant;;;;;;\n'+\
                          'PID;foreNames;lastName;PID;foreNames;PID;'+\
                          'foreNames;day;month;year;denom_0;nameOfParish' 

PRIMAL_TEST_INTERMED_INPUT_FOR_FATHER =\
{'main':{'PID':'(Fr0)','foreNames':'Jois','lastName':'Sunder','gender':'m'},
 'spouse':{'PID':'x1(Fr0)','foreNames':'Alheid'},
 'children':[{'PID':'(Fr0.1)','foreNames':'Wolterus','day':18,'month':12,'year':1661, 
              'nameOfParish':'St. Vitus','denom':['rc']}]}   

PRIMAL_TEST_OUTPUT_FOR_FATHER = """
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

From a relationship between Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)} was brought forth:
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""

def getDefaultTestSettings():
    return DEFAULT_TEST_SETTINGS_DATA.copy()

def getPrimalTestHeader():
    return PRIMAL_TEST_HEADER_DATA

def getPrimalTestIntermediateInputForFather():
    return PRIMAL_TEST_INTERMED_INPUT_FOR_FATHER.copy()
                                            
def getPrimalTestOutputForFather():
    return PRIMAL_TEST_OUTPUT_FOR_FATHER                                 
                                            