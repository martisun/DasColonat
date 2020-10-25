from source.writer_maker import WriterMaker
from source.writer_adapter import WriterAdapter

class Settings(object):
    __summaryWriterTemplatePattern = '$summary(all)'
    
    @staticmethod
    def setTo(inputDict):
        theSettings = Settings()
        theSettings.updateWith(inputDict)
        return theSettings
    
    def __init__(self):
        emptySettings = {'filesToLoadFrom':[],'filesToSaveTo':None,'language':'en',
                           'roleOfMain':''}
        self.updateWith(emptySettings)
    
    def getSummaryWriter(self):
        writerMaker = self.getWriterMaker()
        summaryWriter = WriterAdapter.forTemplatePattern(self.__summaryWriterTemplatePattern)
        summaryWriter.setMakerTo(writerMaker)
        return summaryWriter
    
    def getWriterMaker(self):
        return WriterMaker.inLanguage(self.language)
    
    def setGUITo(self,theGUI):
        self.__GUI = theGUI 
    
    def removeUnloadedFileName(self,fileNameInSetting):
        removeFromSettings = self.__GUI.askToRemoveFileFromSetting(fileNameInSetting)
        if removeFromSettings: self.filesToLoadFrom.remove(fileNameInSetting)  
        
    def isFileInFilesToLoadFrom(self,fileName):
        return (fileName in self.filesToLoadFrom)
    
    def updateWith(self,inputDict):
        for setting in inputDict:
            setattr(self,setting,inputDict[setting])