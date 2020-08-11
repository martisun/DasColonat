from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_writer import FileWriter

class TaskManager(FileHandler):  
    def initialize(self):
        self.__initializeFileLoader()
        self.__initializeFileWriter()
    
    def go(self):
        filesToLoad = self.__fileLoader.getFileToLoadFrom()
        textToSave = filesToLoad[0].getContent()
        if self._settings.language == 'en': textToSave = textToSave%ENGLISH_WORDS
        elif self._settings.language == 'nl': textToSave = textToSave%DUTCH_WORDS
        self.__fileWriter.writeTextToFileToSaveTo(textToSave)
    
    def __initializeFileLoader(self):
        self.__fileLoader = self.__getInitializedFileHandler(FileLoader())
        
    def __initializeFileWriter(self):
        self.__fileWriter = self.__getInitializedFileHandler(FileWriter())
        
    def __getInitializedFileHandler(self,fileHandler):
        fileHandler.setGUITo(self._GUI)
        fileHandler.setFolderAdapterTo(self._folderAdapter)
        fileHandler.setSettingsTo(self._settings)
        return fileHandler
    
ENGLISH_WORDS = ('From a relationship between',
                 'and',
                 'was brought forth',
                 'was baptised on the',
                 '\supscr{th} of',
                 'before the catholic church of the',
                 'parish at')  
    
DUTCH_WORDS = ('Uit een relatie tussen',
               'en',
               'is voortgebracht',
               'is gedoopt op de',
               '\supscr{de}',
               'voor de katholieke kerk van de',
               'parochie te')