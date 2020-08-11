import os

from source.spy_object import SpyObject

class MockFolder(SpyObject):
    def __init__(self):
        super().__init__()
        self._filesInFolder = {}
    
    def open(self,fileName,permission):
        self._logCall([fileName,permission],'O')
        if permission == 'r':
            return self.__createFileForReading(fileName)
        else: 
            return self._createFileForWriting(fileName)
        
    def _createFileForWriting(self,fileName):
        fileObject = MockFile()
        self._filesInFolder[fileName]=fileObject
        return fileObject    
        
    def __createFileForReading(self,fileName):
        self.__assertFileExistsWithName(fileName)
        return self._filesInFolder[fileName]
    
    def __assertFileExistsWithName(self,fileName):
        if not fileName in self._filesInFolder: raise FileNotFoundError
    
    
class MockFolderAdapter(MockFolder):    
    def createFileForWriting(self,fileName):
        return self._createFileForWriting(fileName)
    
    def getSuitableInputFiles(self):
        return [self._filesInFolder[fileName] for fileName in self.__getFilesInInputDirectory()
                if self.__isCSVFileExtension(fileName)]
    
    def readContentFromFileWithName(self,fileName):
        with self.open(fileName,'r') as fileObject:
            content = fileObject.read()
        return content
    
    def writeContentToFileWithName(self,content,fileName):
        with self.open(fileName,'w') as fileObject:
            fileObject.write(content)
    
    def _createFileForWriting(self,fileName):
        fileObject = MockFileAdapter(fileName)
        self._filesInFolder[fileName]=fileObject
        return fileObject      
    
    def __getFilesInInputDirectory(self):
        return sorted(self._filesInFolder.keys())
    
    @staticmethod
    def __isCSVFileExtension(fileName):
        root,ext = os.path.splitext(fileName)
        return (ext == '.csv')
    
        
class MockFile(SpyObject):    
    def __init__(self):
        super().__init__()
        self._logCall(None,'I')
        self.__buffer = ''
        self._content = ''
    
    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        self.close()
    
    def read(self):
        self._logCall(None,'R')
        return self._content
    
    def write(self,content):
        self._logCall(content,'W')
        self.__buffer = content
        
    def close(self):
        self._logCall(None,'C')
        self._content = self.__buffer
    
class MockFileAdapter(MockFile):
    def __init__(self,name):
        super().__init__()
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def getContent(self):
        return self._content