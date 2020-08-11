from source.file_handler import FileHandler

class FileLoader(FileHandler):        
    def getFileToLoadFrom(self):    
        self.__loadFiles()
        self.__checkIfFilesToLoadNonEmpty()
        self.__askToRemoveUnloadedFilesFromSetting()
        return self.__filesToLoad
        
    def __loadFiles(self):
        self.__filesToLoad = self.__getFilesToLoad()
            
    def __getFilesToLoad(self):
        inputFiles = self._folderAdapter.getSuitableInputFiles()
        return [fileObject for fileObject in inputFiles
                if self.__isFileToBeLoaded(fileObject)]
    
    def __getFileNamesInSettingButNotFound(self):
        return [fileName for fileName in self._settings.filesToLoadFrom
                if self.__isFileWithNameNotInFilesToLoad(fileName)]
            
    def __checkIfFilesToLoadNonEmpty(self):
        if not self.__filesToLoad: self._GUI.raiseError('NoInputError')
    
    def __askToRemoveUnloadedFilesFromSetting(self):
        fileNamesInSettingButNotFound = self.__getFileNamesInSettingButNotFound()
        for fileNameInSettingButNotFound in fileNamesInSettingButNotFound:
            self._settings.removeUnloadedFileName(fileNameInSettingButNotFound)
    
    def __isFileToBeLoaded(self,fileObject):
        fileName = fileObject.getName()
        return (self._settings.isFileInFilesToLoadFrom(fileName) or
                self._GUI.askToLoadFile(fileName)) 
    
    def __isFileWithNameNotInFilesToLoad(self,fileName):
        fileNamesToLoad = [fileObject for fileObject in self.__filesToLoad\
                           if fileObject.getName() == fileName]
        return (not fileNamesToLoad)
