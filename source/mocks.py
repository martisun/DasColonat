class MockGUI(object):
    def __init__(self):
        self.__actions = ''
        self.__input   = ''
    
    def askToLoadFile(self,fileName):
        self.__mostRecentInput = fileName
        self.__actions += 'A'
        
    def wereActionsCalled(self,actions):
        return (self.__actions == actions)
    
    def wereArgumentsDuringLastCall(self,arguments):
        return (self.__mostRecentInput == arguments)
    
class AnsweringTrueMockGUI(MockGUI):
    def askToLoadFile(self,fileName):
        super().askToLoadFile(fileName)
        return True
    
class AnsweringFalseMockGUI(MockGUI):
    def askToLoadFile(self,fileName):
        super().askToLoadFile(fileName)
        return False   