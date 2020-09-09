from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_parser import FileParser
from source.file_writer import FileWriter
from source.record_interpreter import RecordInterpreter
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
        filesToLoad  = self.__fileLoader.getFileToLoadFrom()
        parsedRecord      = self.__parseFile(filesToLoad[0])
        interpretedRecord = self.__interpretRecord(parsedRecord)
        peopleData        = self.__collectPeopleFrom(interpretedRecord)
        self.__summaryWriter.setPeopleTo(peopleData)
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
    
    def __parseFile(self,fileToParse):
        fileParser = FileParser.withFileToParseSetTo(fileToParse)
        return fileParser.parse()      
    
    def __interpretRecord(self,parsedRecord):
        recordInterpreter = RecordInterpreter.withRecordToInterpretSetTo(parsedRecord)
        return recordInterpreter.interpret()
    
    def __collectPeopleFrom(self,interpretedRecord):
        # getMain     : _settings.roleOfMain
        # getSpouse  :  father -> mother / mother -> father
        # getChildren : father/mother -> child 
        returnDict = {}
        for role in interpretedRecord:
            if role in ['father','mother']:
                summaryRole = self.__getRoleInSummaryFor(role)
                returnDict[summaryRole] = interpretedRecord[role]
            elif role == 'child':
                returnDict['children'] = [interpretedRecord[role]] 
        return returnDict
    
    def __getRoleInSummaryFor(self,role):
        if self._settings.roleOfMain == role:   return 'main'
        else:                                   return 'spouse'
    