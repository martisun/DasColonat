import re

class FileParser(object):
    __lineSeperator = '\n'
    __cellSeperator = ';'
    
    @staticmethod
    def withFileToParseSetTo(fileToParse):
        stringContent = fileToParse.getContent()
        fileParser = FileParser(stringContent)
        return fileParser
    
    @staticmethod
    def parseString(content):
        fileParser = FileParser(content)
        return fileParser.parse()
    
    def __init__(self,stringContent):
        self.__stringContent = stringContent
    
    def parse(self):
        if self.__isContentParseable():
            cellsOfContent = self.__splitContentIntoCells()
            return self.__readAllRecordsFrom(cellsOfContent)
                    
    def __isContentParseable(self):
        return self.__stringContent != ''    
    
    def __splitContentIntoCells(self):
        rowsOfContent =   self.__stringContent.split(FileParser.__lineSeperator)
        cellsOfContent = [self.__splitIntoCells(line) for line in rowsOfContent]
        return cellsOfContent
    
    @staticmethod
    def __splitIntoCells(string):
        return string.split(FileParser.__cellSeperator)  
    
    @staticmethod 
    def __readAllRecordsFrom(cellsOfContent):
        cellReader = CellReader()
        cellReader.readCellsOfContent(cellsOfContent)
        return cellReader.getAllRecords()

class CellReader(object):
    def __init__(self):
        self.__header    = HeaderNode()
        self.__records   = []
    
    def readCellsOfContent(self,cellsOfContent):
        while not self.__header.areAllColumnsSelected():
            lineOfCells      = cellsOfContent.pop(0)
            self.__readLine(lineOfCells)
        self.__records = cellsOfContent
        
    def getAllRecords(self):
        return [self.__header.buildWith(record) for record in self.__records]
    
    def __readLine(self,lineOfCells):
        self.__selection = Selection.withLengthOf(lineOfCells)
        
        for index,cell in self.__getReversedEnumeratedOf(lineOfCells):
            self.__addCellAtIndexToHeader(cell,index)
    
    def __addCellAtIndexToHeader(self,cell,index):
        if cell != '':
            self.__selection.addBound(index)
            self.__header.addCellWithSelectionAsDescendant(cell,self.__selection)
            
    def __len__(self):      
        return len(self.__records)
        
    @staticmethod
    def __getReversedEnumeratedOf(lineOfCells):
        return reversed(list(enumerate(lineOfCells))) 
        
class HeaderNode(object):
    def __init__(self,name=None):
        self.__children  = []
        self.__selection = Selection() 
        self.name = name
    
    def areAllColumnsSelected(self):
        if self.__children: return self.__areAllChildrensColumnsSelected()
        else:               return self.__isSelectionLengthOne()
    
    def addCellWithSelectionAsDescendant(self,cell,selection):
        if selection.isComplete():
            descendant = HeaderNode(cell)
            descendant.setSelectionTo(selection)
            self.addDescendant(descendant)
    
    def addDescendant(self,descendant):
        nodesToAddTo = self.__children+[self]
        for node in nodesToAddTo:
            if node is self: 
                self.__children.append(descendant)
                break
            if descendant.__isIn(node): 
                node.addDescendant(descendant)
                break
    
    def buildWith(self,record):
        if self.__children:         
            recordBuilder = RecordBuilder()
            for child in self.__children: 
                recordBuilder.addKeyWithValue(child.name,child.buildWith(record))            
            return recordBuilder.makeDictionary()
        else:
            return self.__selection.sliceFrom(record)[0]
    
    def setSelectionTo(self,selection):
        self.__selection = selection.copy()
        
    def __areAllChildrensColumnsSelected(self):
        return all([child.areAllColumnsSelected() for child in self.__children])
        
    def __isIn(self,other):
        return self.__selection.isIn(other.__selection)
    
    def __isSelectionLengthOne(self):
        return self.__selection.isComplete() and len(self.__selection) == 1
        
class RecordBuilder(object):
    def __init__(self):
        self.__outputDict = {}
        self.__listElements = {}
    
    def addKeyWithValue(self,key,value):
        listCriterium = re.findall('(\w+)\_(\d+)',key)
        if listCriterium: self.__setListToValue(listCriterium[0],value)
        else:             self.__setDictKeyToValue(key,value)
    
    def makeDictionary(self):
        self.__addListElementsToOutputDict()
        return self.__outputDict
    
    def __setDictKeyToValue(self,key,value):
        self.__outputDict[key] = value
        
    def __setListToValue(self,listCriterium,value):
        listKey,index = listCriterium
        if not listKey in self.__listElements: self.__listElements[listKey] = {}
        self.__listElements[listKey][index] = value
        
    def __addListElementsToOutputDict(self):
        for listKey in self.__listElements:
            listKeyElements = self.__collectListElementsWithKey(listKey)
            self.__setDictKeyToValue(listKey,listKeyElements) 
    
    def __collectListElementsWithKey(self,listKey):
        indices=sorted(self.__listElements[listKey])
        return [self.__listElements[listKey][index] for index in indices]
        
class Selection(object):
    @staticmethod
    def withLengthOf(inputList):
        return Selection(len(inputList))
    
    def __init__(self,length=None):
        self.__dict = {'start':length,'end':None}
    
    def addBound(self,index):
        self.__dict['end']   = self.get('start')
        self.__dict['start'] = index
    
    def copy(self):
        selection = Selection()
        selection.__dict = self.__dict.copy()
        return selection
    
    def get(self,nameOfAttribute):
        return self.__dict[nameOfAttribute]
    
    def isComplete(self):
        return not (self.get('start') is None)
    
    def isIn(self,other):
        return (self.get('start') >= other.get('start') and self.get('end') <= other.get('end'))
    
    def sliceFrom(self,record):
        return record[self.get('start'):self.get('end')]
    
    def __len__(self):
        return self.get('end')-self.get('start')