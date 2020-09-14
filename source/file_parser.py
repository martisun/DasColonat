class FileParser(object):
    __lineSeperator = '\n'
    __cellSeperator = ';'
    
    @staticmethod
    def withFileToParseSetTo(fileToParse):
        fileParser = FileParser()
        fileParser.__setFileToParseTo(fileToParse)
        return fileParser
    
    def __setFileToParseTo(self,fileToParse):
        self.__stringContent = fileToParse.getContent()
    
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
    
    def __addCellAtIndexToHeader(self,cell,index):
        if cell != '':
            self.__selection.addBound(index)
            self.__header.addCellWithSelectionAsDescendant(cell,self.__selection)
            
    def __len__(self):      
        return len(self.__records)
    
    def __readLine(self,lineOfCells):
        self.__selection = Selection.withLengthOf(lineOfCells)
        for index,cell in self.__getReversedEnumeratedOf(lineOfCells):
            self.__addCellAtIndexToHeader(cell,index)
        
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
            return {child.name:child.buildWith(record) for child in self.__children}
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