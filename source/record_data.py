class WriterData(object):
    def __init__(self,data):
        self.__data = data
    
    def toDict(self):
        return self.__data             
    
    def setTagOrder(self,tagOrder):
        self.__tagOrder = tagOrder
        
    def __getMainTag(self):
        if len(self): return list(self.__data)[0]     
        else:         return 'main'

    def getMainData(self):
        tag = self.__getMainTag()
        return WriterData(self.__data[tag].data)
    
    def selectTags(self,desiredTags):
        data = self.__selectTags(desiredTags)
        return WriterData(data)
    
    def isEmpty(self):
        return (not self.__data)
    
    def __selectTags(self,desiredTags):
        return [self.__data[tag] for tag in desiredTags if tag in self.__data]
    
    def __len__(self):
        return len(self.__data)

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