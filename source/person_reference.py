class PersonReferenceX(object):
    def setFromDict(self,inputDict):
        self.isPersonRef = True
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
    
    def __len__(self):
        return 0
    
    def __repr__(self):
        return 'PersonReference[%s]'%(str(self.__inputDict))
    