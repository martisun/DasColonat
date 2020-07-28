class Settings(object):
    def __init__(self,inputDict):
        self.INPUT_DIR = './input'
        self.filesToLoadFrom = inputDict['filesToLoadFrom']
        
    def isFileInFilesToLoadFrom(self,fileName):
        return (fileName in self.filesToLoadFrom)
        
    def removeFileFromFilesToLoadFrom(self,fileName):
        self.filesToLoadFrom.remove(fileName)