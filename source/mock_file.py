from source.spy_object import SpyObject

class MockFile(SpyObject):
    @staticmethod
    def open(fileName,permission):
        mockFile = MockFile()
        mockFile._logCall([fileName,permission],'O')
        return mockFile
    
    def __init__(self):
        super().__init__()
        self.write('')
    
    def write(self,content):
        self.__content = content
    
    def read(self):
        return self.__content