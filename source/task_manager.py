from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_writer import FileWriter
from source.phrases_factory import PhrasesFactory

class TaskManager(FileHandler):
    def run(self):
        self.__initialize()
        self.__go()
    
    def __initialize(self):
        self.__initializeFileLoader()
        self.__initializeFileWriter()
    
    def __go(self):
        filesToLoad = self.__fileLoader.getFileToLoadFrom()
        textToFill = filesToLoad[0].getContent()
        textToSave = self.__fillTemplate(textToFill)
        self.__fileWriter.writeTextToFileToSaveTo(textToSave)
    
    def __fillTemplate(self,textToFill):
        phrases = PhrasesFactory.inLanguage(self._settings.language)
        return textToFill%phrases
    
    def __initializeFileLoader(self):
        self.__fileLoader = self.__getInitializedFileHandler(FileLoader())
        
    def __initializeFileWriter(self):
        self.__fileWriter = self.__getInitializedFileHandler(FileWriter())
        
    def __getInitializedFileHandler(self,fileHandler):
        fileHandler.setGUITo(self._GUI)
        fileHandler.setFolderAdapterTo(self._folderAdapter)
        fileHandler.setSettingsTo(self._settings)
        return fileHandler    