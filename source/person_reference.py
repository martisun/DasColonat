class PersonReference(object):
    @staticmethod
    def makeFrom(inputData):
        if type(inputData) == list: return PersonReference.__fromList(inputData)
        else:                       return PersonReference.__fromDict(inputData)
    
    @staticmethod
    def __fromList(inputList):
        return [PersonReference.__fromDict(inputDict) for inputDict in inputList]
    
    @staticmethod
    def __fromDict(inputDict):
        personReference = PersonReference()
        personReference.__setFromDict(inputDict)
        return personReference  
    
    def __init__(self):
        self.__inputDict = {}
    
    def __setFromDict(self,inputDict):
        self.__inputDict = inputDict
        
    def get(self,nameOfAttribute):
        if nameOfAttribute in self.__inputDict: 
            return self.__inputDict[nameOfAttribute]
        else: return ''