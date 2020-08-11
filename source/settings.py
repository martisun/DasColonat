class Settings(object):
    @staticmethod
    def setTo(inputDict):
        theSettings = Settings()
        theSettings.__updateWith(inputDict)
        return theSettings
    
    def __init__(self):
        defaultSettings = {'filesToLoadFrom':[],'filesToSaveTo':None,'language':'en'}
        self.__updateWith(defaultSettings)
    
    def setGUITo(self,theGUI):
        self.__GUI = theGUI 
    
    def removeUnloadedFileName(self,fileNameInSetting):
        removeFromSettings = self.__GUI.askToRemoveFileFromSetting(fileNameInSetting)
        if removeFromSettings: self.filesToLoadFrom.remove(fileNameInSetting)  
        
    def isFileInFilesToLoadFrom(self,fileName):
        return (fileName in self.filesToLoadFrom)
    
    def __updateWith(self,inputDict):
        for setting in inputDict:
            setattr(self,setting,inputDict[setting])