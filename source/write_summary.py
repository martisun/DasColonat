import os

INPUT_DIR = './input'

class SummaryWriter(object):
    @staticmethod
    def usingGUI(theGUI):
        aSummaryWriter = SummaryWriter()
        aSummaryWriter.__setGUITo(theGUI)
        return aSummaryWriter
    
    def __init__(self):
        self.loadedFiles = []
    
    def execute(self): 
        self.__loadFiles() 
        
    
    def __loadFiles(self):
        csvFilesInInputDirectory = self.__getCSVFilesInInputDirectory()
        for fileName in csvFilesInInputDirectory: 
            if self.__GUI.askToLoadFile(fileName): self.loadedFiles += fileName
        if not self.loadedFiles: NoInputError.raiseError()
    
    def __setGUITo(self,theGUI):
        self.__GUI = theGUI        
    
    @staticmethod
    def __getCSVFilesInInputDirectory():
        allFileNamesInInputDirectory = os.listdir(INPUT_DIR)
        return [fileName for fileName in allFileNamesInInputDirectory
                if SummaryWriter.__isCSVFileExtension(fileName)]            
    
    @staticmethod
    def __isCSVFileExtension(fileName):
        root,ext = os.path.splitext(fileName)
        return (ext == '.csv')
    
class NoInputError(OSError):
    @staticmethod
    def raiseError():
        msg = 'No input-files were found in %s, no records can be loaded!'
        raise NoInputError(msg%INPUT_DIR)
        