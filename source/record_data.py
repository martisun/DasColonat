import re

class WriterData(object):
    @staticmethod
    def makeFrom(data):
        if isinstance(data,list): return WriterDataList(data)
        else:                     return WriterDataDict(data)
    
    def __init__(self,data):
        self._data = data
        self.__index = 0
    
    def toDict(self):
        return self._data
    
    def setTagOrder(self,tagOrder):
        self.__tagOrder = tagOrder
    
    def selectData(self,keyedDataList):
        for keyedData in keyedDataList: 
            self.__addKeyedDataElement(keyedData)

    def get(self,namesOfAttributes):
        if isinstance(namesOfAttributes,list):
            return self.__getMultipleAttributes(namesOfAttributes)
        else: return self.__getSingleAttribute(namesOfAttributes)
    
    def hasDateReference(self):
        return ('date' in self._data)
      
    def __addKeyedDataElement(self,keyedData):
        if keyedData.isNextSuitable():
            newElement = keyedData.getWriterData()
            self._data.update(newElement)
    
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
    
    def __contains__(self,tag):
        return tag in self._data
    
    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self._data)
    
    def __next__(self):
        if self.__index == len(self):
            self.__index = 0
            raise StopIteration
        self.__index += 1
        selectedData = self._data[self.__index-1]
        return self.makeFrom(selectedData)
            
    def isEmpty(self):
        return (not self._data)
    
    def isMainNonTrivial(self):
        return False
    
    def isPrimitive(self):
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
    
    def __repr__(self):
        return 'WriterDataList[%s]'%(str(self._data))

class WriterDataDict(WriterData):
    def getMainData(self):
        if len(self) == 1:  
            primalTag = list(self._data)[0]  
            return self.selectTag(primalTag)
        else: 
            return self.makeFrom({'main':self._data})      
        
    def isMainNonTrivial(self):
        return len(self) != 1
    
    def isPrimitive(self):
        return False
    
    def __repr__(self):
        return 'WriterDataDict[%s]'%(str(self._data))    
    
class KeySpecification(object):
    __pattern = '(\w+)(.?)'
    
    @staticmethod
    def setupFrom(templateSpecification):
        return [KeySpecification(parsableText,templateSpecification)
                for parsableText in templateSpecification.getRequiredKeys()]
    
    @staticmethod
    def parse(parsableText):
        return re.findall(KeySpecification.__pattern,parsableText)[0]
    
    def __init__(self,parsableText,templateSpecification):
        self.key, self.tag = self.parse(parsableText)
        self.__setDesiredLength(templateSpecification)
    
    def __setDesiredLength(self,templateSpecification):
        if templateSpecification.hasNonTrivialLength() : 
            self.__desiredLength = templateSpecification.getLength()
        else: self.__desiredLength = None
    
    def setWriterData(self,writerData):
        self.__data = writerData
    
    def getWriterData(self):
        return {self.key:self.__data.getData()}
    
    def isNextSuitable(self):
        if not self.__data.isEmpty():
            if not self.__data.isPrimitive(): 
                self.__data = self.__data.pop()
            return self.__dataMatches() and self.__tagMatches()
        else: return False
    
    def __tagMatches(self):
        return self.tag == '' or self.__data.hasDateReference()                
    
    def __dataMatches(self):
        return self.__data.isPrimitive() or self.__lengthMatches()
                
    def __lengthMatches(self):
        return self.__desiredLength is None or len(self.__data) == self.__desiredLength
    
    def __repr__(self):
        if self.tag == '': tagRepr = 'EMPTY'
        else:              tagRepr = self.tag
        return 'KeySpecification[key=%s,tag=%s]'%(self.key,tagRepr)    