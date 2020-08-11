from source.spy_object import SpyObject

class MockGUI(SpyObject): 
    def __init__(self):
        super().__init__()
        self.__script = None
    
    def askToLoadFile(self,fileName):
        self._logCall(fileName,'Al')
        return self.__script
    
    def askToSaveToFile(self):
        self._logCall(None,'As')
        return self.__script
    
    def askToRemoveFileFromSetting(self,fileName):
        self._logCall(fileName,'R')
        return self.__script
    
    def raiseError(self,errorCode):
        self._logCall(errorCode,'E')
    
    def setScript(self,script):
        self.__script = script
        
class MockGUIInspector(object):
    def _initializeMockGUI(self):
        self.theGUI = MockGUI()
    
    def _assertGUIWasRunWithActionsAndArguments(self,actions,arguments=[]):
        self.assertTrue(self.theGUI.wasObjectRunWithActionsAndArguments(actions,arguments)) 