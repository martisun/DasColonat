import os
import source.settings as ss

class SummaryWriter(object):
    @staticmethod
    def startUpWithGUI(theGUI):
        aSummaryWriter = SummaryWriter()
        aSummaryWriter.__setGUITo(theGUI)
        aSummaryWriter.startUp()
    
    def startUp(self):
        FileLoader(self.__GUI)
    
    def __setGUITo(self,theGUI):
        self.__GUI = theGUI 

class FileLoader(object):
    def __init__(self,theGUI):
        self.__GUI = theGUI
        self.__loadFiles()         
        
    def __loadFiles(self):
        self.filesToLoad = self.__getFilesToLoad()
        self.__checkIfFilesToLoadNonEmpty()
            
    def __getFilesToLoad(self):
        csvFilesInInputDirectory = self.__getCSVFilesInInputDirectory()
        return [fileName for fileName in csvFilesInInputDirectory
                if self.__isFileToBeLoaded(fileName)]
            
    def __checkIfFilesToLoadNonEmpty(self):
        if not self.filesToLoad: 
            self.__GUI.raiseError('NoInputError')
            self.__askToRemoveFileFromSetting()
    
    def __askToRemoveFileFromSetting(self):
        if not ss.FilesToLoadFrom is None:
            removeFromSettings = self.__GUI.askToRemoveFileFromSetting(ss.FilesToLoadFrom)
            if removeFromSettings: ss.FilesToLoadFrom = None
    
    def __isFileToBeLoaded(self,fileName):
        return (fileName == ss.FilesToLoadFrom or self.__GUI.askToLoadFile(fileName)) 
    
    @staticmethod
    def __getCSVFilesInInputDirectory():
        allFileNamesInInputDirectory = os.listdir(ss.INPUT_DIR)
        return [fileName for fileName in allFileNamesInInputDirectory
                if FileLoader.__isCSVFileExtension(fileName)]            
    
    @staticmethod
    def __isCSVFileExtension(fileName):
        root,ext = os.path.splitext(fileName)
        return (ext == '.csv')
        