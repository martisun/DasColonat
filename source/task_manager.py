from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_parser import FileParser
from source.file_writer import FileWriter
from source.record_reader import RecordReader

class TaskManager(FileHandler):
    def run(self):
        self.__initialize()
        self.__go()
    
    def __initialize(self):
        self.__initializeFileLoader()
        self.__initializeFileWriter()
        self.__initializeSummaryWriter()
    
    def __go(self):
        filesToLoad    = self.__fileLoader.getFileToLoadFrom()
        parsedRecords  = self.__parseFile(filesToLoad[0]) 
        allPeopleData  = self.__readPeopleFromRecords(parsedRecords)
        self.__deriveAdditionalInformationFrom(allPeopleData)
        textToSave = self.__summaryWriter.write(allPeopleData)
        self.__fileWriter.writeTextToFileToSaveTo(textToSave)
    
    def __initializeFileLoader(self):
        self.__fileLoader = self.__getInitializedFileHandler(FileLoader())
        
    def __initializeFileWriter(self):
        self.__fileWriter = self.__getInitializedFileHandler(FileWriter())
    
    def __initializeSummaryWriter(self):
        self.__summaryWriter = self._settings.getSummaryWriter()
        
    def __getInitializedFileHandler(self,fileHandler):
        fileHandler.setGUITo(self._GUI)
        fileHandler.setFolderAdapterTo(self._folderAdapter)
        fileHandler.setSettingsTo(self._settings)
        return fileHandler
    
    def __parseFile(self,fileToParse):
        fileParser = FileParser.withFileToParseSetTo(fileToParse)
        return fileParser.parse()
     
    def __readPeopleFromRecords(self,parsedRecords):
        recordReader = RecordReader(self._settings.roleOfMain)
        return recordReader.readPeopleFrom(parsedRecords) 
    
    def __deriveAdditionalInformationFrom(self,peopleData):
        people = PeopleDataDeriver(peopleData)
        people.deriveAdditionalInformation()
    
class PeopleDataDeriver(object):
    def __init__(self,rawInputDict):
        self.__data = rawInputDict
        
    def data(self):
        return self.__data
    
    def deriveAdditionalInformation(self):
        if self.__isLastNameOfMainDerivable(): 
            self.__updateLastNameOfMainWithLastNameOfFather()
    
    def __isLastNameOfMainDerivable(self):
        return (not 'lastName' in self.__data['main'] and 'father' in self.__data['main'])
        
    def __updateLastNameOfMainWithLastNameOfFather(self):
        self.__data['main']['lastName'] = self.__data['main']['father']['lastName']   
        
    