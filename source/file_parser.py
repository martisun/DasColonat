class FileParser(object):
    __lineSeperator = '\n'
    __itemSeperator = ';'
    
    @staticmethod
    def withFileToParseSetTo(fileToParse):
        fileParser = FileParser()
        fileParser.__setFileToParseTo(fileToParse)
        return fileParser
        
    def parse(self):
        if self.__isContentParseable():
            updateForDict = self.__getUpdateForDict()
            self.__updateDictWith(updateForDict)          
        return self.__dict
    
    def __setFileToParseTo(self,fileToParse):
        stringContent,dictContent = fileToParse.getContent()
        self.__content = stringContent
        self.__dict    = dictContent
            
    def __isContentParseable(self):
        return self.__content != ''
    
    @staticmethod
    def __splitIntoItems(string):
        return string.split(FileParser.__itemSeperator)    
    
    def __updateDictWith(self,updateForDict):
        self.__dict[self.__role]=updateForDict
    
    def __getUpdateForDict(self):
        lines = self.__content.split(FileParser.__lineSeperator)
        self.__role = self.__splitIntoItems(lines[0])[0]
        headerItems = self.__splitIntoItems(lines[1])
        recordItems = self.__splitIntoItems(lines[2])
        return dict(zip(headerItems,recordItems))