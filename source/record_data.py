class WriterData(object):
    def __init__(self,data):
        self.__data = data
        self.__index = 0
    
    def toDict(self):
        return self.__data             
    
    def setTagOrder(self,tagOrder):
        self.__tagOrder = tagOrder
        
    def __getMainTag(self):
        if len(self) > 0: return list(self.__data)[0]     
        else:             return 'main'

    def get(self,namesOfAttributes):
        if isinstance(namesOfAttributes,list):
            return self.__getMultipleAttributes(namesOfAttributes)
        else:
            return self.__getSingleAttribute(namesOfAttributes)
    
    def __getMultipleAttributes(self,namesOfAttributes):
        return [self.__getSingleAttribute(nameOfAttribute) for nameOfAttribute in namesOfAttributes]
        
    def __getSingleAttribute(self,nameOfAttribute):    
        if nameOfAttribute in self.__data: 
            return self.__data[nameOfAttribute]
        else: return ''
        
    def getMainData(self):
        tag = self.__getMainTag()
        mainData = self.__determineMainData(tag)
        return WriterData(mainData)
    
    def __determineMainData(self,tag):
        if isinstance(self.__data,dict):
            print('record_data l.37 refactoring')
            if isinstance(self.__data[tag],list):
                return self.__data[tag][0].data
            else: return self.__data[tag].data
        else: return {tag:self.__data}
    
    def selectTag(self,desiredTag):
        return WriterData(self.__data[desiredTag])
    
    def selectTags(self,desiredTags):
        data = self.__selectTags(desiredTags)
        return WriterData(data)
    
    def isEmpty(self):
        return (not self.__data)
    
    def __selectTags(self,desiredTags):
        return [self.__data[tag] for tag in desiredTags if tag in self.__data]
    
    def __len__(self):
        return len(self.__data)
    
    def __contains__(self,tag):
        return tag in self.__data
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__index == len(self):
            self.__index = 0
            raise StopIteration
        self.__index += 1
        return WriterData(self.__data[self.__index-1])

class RecordData(object):
    def __init__(self,data):
        self._data = data
    
    def isEmptyList(self):
        return isinstance(self._data,list) and not self._data
    
    def isPrimitive(self):
        return self._isPrimitive(self._data)
    
    def pop(self):
        poppedData = self._data.pop(0)
        return RecordData(poppedData)
    
    def getData(self):
        if self.isPrimitive(): return self._data[0]
        else: return self._data
    
    @staticmethod
    def _isPrimitive(data):
        return isinstance(data,list) and (isinstance(data[0],int) or isinstance(data[0],str))
    
    def isSuitableGivenKeySpecification(self,keySpecification):
        return isinstance(self._data,list) or self._data.isSuitableGivenTag(keySpecification.tag)
    
class CompositeRecordData(RecordData):
    def __init__(self,data):
        self._data = self.__getCopyOfData(data)
        
    def __getCopyOfData(self,data):
        if self._isPrimitive(data): return data         
        else: return data.copy()    