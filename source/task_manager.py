from source.file_handler import FileHandler
from source.file_loader import FileLoader
from source.file_parser import FileParser
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
        parsedFile  = self.__parseFile(filesToLoad[0])
        people      = self.__collectPeopleFrom(parsedFile)
        self.__summaryWriter.setPeopleTo(people)
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
    
    def __collectPeopleFrom(self,parsedFile):
        returnDict = {}
        for role in parsedFile:
            if role in ['father','mother']:
                summaryRole = self.__getRoleInSummaryFor(role)
                returnDict[summaryRole] = parsedFile[role]
                if role == 'father': returnDict[summaryRole]['gender']='m'
                else:                returnDict[summaryRole]['gender']='v'
            elif role == 'child':
                returnDict['children'] = [parsedFile[role]]
            else: returnDict[role]=parsedFile[role]    
        return returnDict
    
    def __getRoleInSummaryFor(self,role):
        if self._settings.roleOfMain == role:   return 'main'
        else:                                   return 'spouse'
    