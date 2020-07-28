from source.spy_object import SpyObject

class MockGUI(SpyObject):     
    def askToLoadFile(self,fileName):
        self._logCall(fileName,'A')
        return self.__script
    
    def askToRemoveFileFromSetting(self,fileName):
        self._logCall(fileName,'R')
        return self.__script
    
    def raiseError(self,errorCode):
        self._logCall(errorCode,'E')
    
    def setScript(self,script):
        self.__script = script