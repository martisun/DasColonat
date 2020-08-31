class FileParser(object):
    __lineSeperator = '\n'
    __cellSeperator = ';'
    
    @staticmethod
    def withFileToParseSetTo(fileToParse):
        fileParser = FileParser()
        fileParser.__setFileToParseTo(fileToParse)
        return fileParser
        
    def parse(self):
        if self.__isContentParseable():
            self.__splitContentIntoCells()
            self.__parseColumnSelectionsIntoDict()
        return self.__dict
    
    def __parseColumnSelectionsIntoDict(self):
        for columnSelection in self.__getColumnSelections():
            self.__parseToDictRoleFromSelection(columnSelection)
    
    def __getColumnSelections(self):
        startSelection = [column for column in range(len(self.__rolesInHeader))\
                           if self.__rolesInHeader[column] != '']
        nextSelection  = startSelection[1:]+[len(self.__rolesInHeader)]
        return [(startSelection[i],nextSelection[i]) for i in range(len(startSelection))]
    
    def __parseToDictRoleFromSelection(self,columnSelection):
        updateForDict = self.__buildDictWithHeaderAndRecord(columnSelection)
        self.__addToDictRoleWithData(columnSelection[0],updateForDict)
    
    def __setFileToParseTo(self,fileToParse):
        self.__stringContent = fileToParse.getContent()
        self.__dict          = {}
            
    def __splitContentIntoCells(self):
        rowsOfContent =   self.__stringContent.split(FileParser.__lineSeperator)
        cellsOfContent = [self.__splitIntoCells(line) for line in rowsOfContent]
        self.__rolesInHeader      = cellsOfContent[0]
        self.__nameFieldsInHeader = cellsOfContent[1]
        self.__recordValues       = cellsOfContent[2]
                
    def __isContentParseable(self):
        return self.__stringContent != ''
    
    @staticmethod
    def __splitIntoCells(string):
        return string.split(FileParser.__cellSeperator)    
    
    def __buildDictWithHeaderAndRecord(self,columnSelection):
        headerCells  = self.__getSelectionOfList(columnSelection,self.__nameFieldsInHeader)
        recordValues = self.__getSelectionOfList(columnSelection,self.__recordValues)
        return dict(zip(headerCells,recordValues))
    
    @staticmethod
    def __getSelectionOfList(selection,listValues):
        startOfSelection,endOfSelection = selection[0],selection[1]
        return listValues[startOfSelection:endOfSelection]
    
    def __addToDictRoleWithData(self,roleColumn,updateForDict):
        role = self.__rolesInHeader[roleColumn]
        self.__dict[role]=updateForDict