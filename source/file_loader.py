import os

class FileLoader(object):        
    def setGUITo(self,theGUI):
        self.__GUI = theGUI 
        
    def setSettingsTo(self,theSettings):
        self.__settings = theSettings        
        
    def startUp(self):    
        self.__loadFiles()
        self.__checkIfFilesToLoadNonEmpty()
        self.__askToRemoveUnloadedFilesFromSetting()
        
    def __loadFiles(self):
        self.__filesToLoad = self.__getFilesToLoad()
            
    def __getFilesToLoad(self):
        csvFilesInInputDirectory = self.__getCSVFilesInInputDirectory()
        return [fileName for fileName in csvFilesInInputDirectory
                if self.__isFileToBeLoaded(fileName)]
    
    def __getFileInSettingButNotFound(self):
        return [fileName for fileName in self.__settings.filesToLoadFrom
                if self.__isFileNotInFilesToLoad(fileName)]
            
    def __checkIfFilesToLoadNonEmpty(self):
        if not self.__filesToLoad: self.__GUI.raiseError('NoInputError')
    
    def __askToRemoveUnloadedFilesFromSetting(self):
        filesInSettingButNotFound = self.__getFileInSettingButNotFound()
        for fileInSettingButNotFound in filesInSettingButNotFound:
            self.__removeUnloadedFileFromSetting(fileInSettingButNotFound)
            
    def __removeUnloadedFileFromSetting(self,fileInSetting):
        removeFromSettings = self.__GUI.askToRemoveFileFromSetting(fileInSetting)
        if removeFromSettings: self.__settings.removeFileFromFilesToLoadFrom(fileInSetting)
    
    def __isFileToBeLoaded(self,fileName):
        return (self.__settings.isFileInFilesToLoadFrom(fileName) or
                self.__GUI.askToLoadFile(fileName)) 
    
    def __isFileNotInFilesToLoad(self,fileName):
        return (not fileName in self.__filesToLoad)
    
    def __getCSVFilesInInputDirectory(self):
        allFileNamesInInputDirectory = os.listdir(self.__settings.INPUT_DIR)
        return [fileName for fileName in allFileNamesInInputDirectory
                if self.__isCSVFileExtension(fileName)]            
    
    @staticmethod
    def __isCSVFileExtension(fileName):
        root,ext = os.path.splitext(fileName)
        return (ext == '.csv')
        