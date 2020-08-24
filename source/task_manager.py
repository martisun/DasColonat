from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_writer import FileWriter
from source.summary_writer import SummaryWriter

class TaskManager(FileHandler):
    def run(self):
        self.__initialize()
        self.__go()
    
    def __initialize(self):
        self.__initializeFileLoader()
        self.__initializeFileWriter()
        self.__initializeSummaryWriter()
    
    def __go(self):
        filesToLoad = self.__fileLoader.getFileToLoadFrom()
        self.__summaryWriter.setPeopleTo(filesToLoad[0].getContent())
        textToSave = self.__summaryWriter.getSummary()
        self.__fileWriter.writeTextToFileToSaveTo(textToSave)
    
    def __initializeFileLoader(self):
        self.__fileLoader = self.__getInitializedFileHandler(FileLoader())
        
    def __initializeFileWriter(self):
        self.__fileWriter = self.__getInitializedFileHandler(FileWriter())
        
    def __initializeSummaryWriter(self):
        self.__summaryWriter = SummaryWriter()
        self.__phraseWriter = self._settings.getPhraseWriter()
        self.__summaryWriter.setPhraseWriterTo(self.__phraseWriter)
        
    def __getInitializedFileHandler(self,fileHandler):
        fileHandler.setGUITo(self._GUI)
        fileHandler.setFolderAdapterTo(self._folderAdapter)
        fileHandler.setSettingsTo(self._settings)
        return fileHandler
    