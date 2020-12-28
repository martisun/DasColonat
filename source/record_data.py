class WriterData(object):
    @staticmethod
    def makeFrom(data):
        if isinstance(data,list): return WriterDataList(data)
        else:                     return WriterDataDict(data)
    
    def __init__(self,data):
        self._data = data
        self.__index = 0
    
    def isSuitableGivenTag(self,tag):
        return (tag == '*' and self._isMoreThanReference()) or tag != '*'
      
    def _isMoreThanReference(self):
        return 'year' in self._data    
    
    def toDict(self):
        return self._data
    
    def setTagOrder(self,tagOrder):
        self.__tagOrder = tagOrder
    
    def update(self,dataElement):
        self._data.update(dataElement)

    def get(self,namesOfAttributes):
        if isinstance(namesOfAttributes,list):
            return self.__getMultipleAttributes(namesOfAttributes)
        else: return self.__getSingleAttribute(namesOfAttributes)
    
    def __getMultipleAttributes(self,namesOfAttributes):
        return [self.__getSingleAttribute(nameOfAttribute)\
                for nameOfAttribute in namesOfAttributes]
        
    def __getSingleAttribute(self,nameOfAttribute):    
        if nameOfAttribute in self._data: 
            return self._data[nameOfAttribute]
        else: return ''
           
    def getMainData(self):
        raise Exception('Calling abstract method!')       
            
    def selectTag(self,desiredTag):
        data = self._data[desiredTag]
        return self.makeFrom(data)
    
    def selectTags(self,desiredTags):
        data = self.__selectTags(desiredTags)
        return self.makeFrom(data)
    
    def isEmpty(self):
        return (not self._data)
    
    def __selectTags(self,desiredTags):
        return [self._data[tag] for tag in desiredTags if tag in self._data]
    
    def __len__(self):
        return len(self._data)
    
    def __contains__(self,tag):
        return tag in self._data
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__index == len(self):
            self.__index = 0
            raise StopIteration
        self.__index += 1
        selectedData = self._data[self.__index-1]
        return self.makeFrom(selectedData)
            
    def isEmpty(self):
        return (not self._data)
    
    def isPrimitive(self):
        raise Exception('Calling abstract method!')
        
    def isSuitableGivenKeySpecification(self,keySpecification):
        raise Exception('Calling abstract method!')    
    
    def pop(self):
        poppedData = self._data.pop(0)
        return self.makeFrom(poppedData)
    
    def getData(self):
        if self.isPrimitive(): return self._data[0]
        else: return self._data
        
    def copy(self):
        if self.isPrimitive(): return self
        else: 
            copiedData = self._data.copy()
            return self.makeFrom(copiedData)
    
class WriterDataList(WriterData):    
    def getMainData(self):
        return self.makeFrom(self._data[0])
    
    def isPrimitive(self):
        return isinstance(self._data[0],int) or isinstance(self._data[0],str)
    
    def isSuitableGivenKeySpecification(self,keySpecification):
        print('l.105 record_data.py refactoring')
        return True
    
    def __repr__(self):
        return 'WriterDataList[%s]'%(str(self._data))

class WriterDataDict(WriterData):
    def getMainData(self):
        if len(self) == 1:  
            primalTag = list(self._data)[0]  
            return self.selectTag(primalTag)
        else: 
            return self.makeFrom({'main':self._data})      
        
    def isPrimitive(self):
        return False
    
    def isSuitableGivenKeySpecification(self,keySpecification):
        return keySpecification.tag == '' or self._isMoreThanReference()
    
    def __repr__(self):
        return 'WriterDataList[%s]'%(str(self._data))        