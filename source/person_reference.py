class PersonReference(object):
    @staticmethod
    def fromDict(inputData):
        personReference = PersonReference()
        personReference.setFromDict(inputData)
        return personReference
    
    def __init__(self):
        self.__inputDict = {}
    
    def setFromDict(self,inputDict):
        self.__inputDict = inputDict
        
    def get(self,nameOfAttribute):
        if nameOfAttribute in self.__inputDict: 
            return self.__inputDict[nameOfAttribute]
        else: return ''