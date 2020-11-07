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
        self.data = inputDict
        
    def get(self,namesOfAttributes):
        if isinstance(namesOfAttributes,list):
            return self.__getMultipleAttributes(namesOfAttributes)
        else:
            return self.__getSingleAttribute(namesOfAttributes)
    
    def __getMultipleAttributes(self,namesOfAttributes):
        return [self.__getSingleAttribute(nameOfAttribute) for nameOfAttribute in namesOfAttributes]
        
    def __getSingleAttribute(self,nameOfAttribute):    
        if nameOfAttribute in self.__inputDict: 
            return self.__inputDict[nameOfAttribute]
        else: return ''
        
    def isMoreThanReference(self):
        return 'year' in self.__inputDict
    
    def isSuitableGivenTag(self,tag):
        return (tag == '*' and self.isMoreThanReference()) or tag != '*'
    