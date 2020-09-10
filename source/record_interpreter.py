class RecordInterpreter(object):
    __roleSpecificImplicitData = {'father':{'gender':'m'},
                                  'mother':{'gender':'v'}}
    
    @staticmethod
    def withRecordToInterpretSetTo(parsedRecord):
        recordInterpreter = RecordInterpreter()
        recordInterpreter.__setParsedRecordTo(parsedRecord)
        return recordInterpreter
    
    def interpret(self):
        for role in self.__dict: self.__updateDictForRole(role)
        return self.__dict  
    
    def __setParsedRecordTo(self,parsedRecord):
        self.__dict = parsedRecord  
         
    def __updateDictForRole(self,role):
        if role in self.__roleSpecificImplicitData:
            self.__dict[role].update(self.__roleSpecificImplicitData[role])