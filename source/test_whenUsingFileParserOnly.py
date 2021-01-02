from source.extended_testcase import ExtendedTestCase

from source.file_parser import FileParser

class whenUsingFileParserOnly(ExtendedTestCase):
    def test_whenParsingSingleDate(self):
        """Tests whether the date-format of a single date can be
        parsed."""
        dataDict = {'date':{'day':'1','month':'2','year':'1823'}}
        fileContent = 'date;;\n'+\
                      'day;month;year\n'+\
                      '1;2;1823'
        parsedFile = FileParser.parseString(fileContent)
        print('l.13 test_whenUsingFileParserOnly refactoring')
        self.__assertDataStructureActualMatchesExpected(parsedFile[0],dataDict)  
        
    def test_whenParsingSingleDateList(self):
        """Tests whether the date-format of a single date can be
        parsed when in a list"""
        dataDict = {'date':[{'day':'1','month':'2','year':'1823'}]}
        fileContent = 'date_0;;\n'+\
                      'day;month;year\n'+\
                      '1;2;1823'
        parsedFile = FileParser.parseString(fileContent)
        print('l.13 test_whenUsingFileParserOnly refactoring')
        self.__assertDataStructureActualMatchesExpected(parsedFile[0],dataDict)     
        
    def test_whenParsingDoubleDateList(self):
        """Tests whether a double date-entry date-format can be parsed
        with only the day differing."""
        dataDict = {'date':[{'day':'30','month':'8','year':'1736'},
                            {'day':'31','month':'8','year':'1736'}]}
        fileContent = 'date_0;;;date_1;;\n'+\
                      'day;month;year;day;month;year\n'+\
                      '30;8;1736;31;8;1736'
        parsedFile = FileParser.parseString(fileContent)
        print('l.13 test_whenUsingFileParserOnly refactoring')
        self.__assertDataStructureActualMatchesExpected(parsedFile[0],dataDict)   
        
    def test_whenParsingSingleDateBaptismEntry(self):
        """Tests whether a a single baptism entry can be parsed."""
        dataDict = DOUBLE_BAPTISM_ENTRY_CHILD
        fileContent = 'main;;;;;;;;;;;\n'+\
                      ';;;;;;date_0;;;date_1;;\n'+\
                      'PID;foreNames;gender;nameOfParish;denom_0;denom_1;'+\
                      'day;month;year;day;month;year\n'+\
                      '(Fr1.1.2);Bernardus;m;St. Vitus;rc;ref;30;8;1736;31;8;1736'
        parsedFile = FileParser.parseString(fileContent)
        self.__assertDataStructureActualMatchesExpected(parsedFile[0],dataDict)  
        
    def __assertDataStructureActualMatchesExpected(self,actual,expected):
        assertion = (actual == expected)
        if not assertion: 
            print('\nData structures are not equal!')
            print('\nactual:',actual)
            print('\nexpected:',expected)
        self.assertTrue(assertion) 
        
        
DOUBLE_BAPTISM_ENTRY_CHILD = {'main':{'PID':'(Fr1.1.2)','foreNames':'Bernardus','gender':'m',
                              'nameOfParish':'St. Vitus','denom':['rc','ref'],
                              'date':[{'day':'30','month':'8','year':'1736'},
                                      {'day':'31','month':'8','year':'1736'}]}}         
        
           