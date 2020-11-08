import re 

class WriterTemplate(object): 
    blankArgument = '+blank'
    
    def __init__(self,text):
        self.__text = text
    
    def getText(self):
        return self.__text
    
    def getData(self):
        return self._selected
    
    def replaceBlankBy(self,replacementText):
        self.replace(self.blankArgument,replacementText)
    
    def replaceByBlank(self,textToReplace):
        self.replace(textToReplace,self.blankArgument)
    
    def replace(self,textToReplace,replacementText):
        self.__text = self.__text.replace(textToReplace,str(replacementText))
    
    def setDataTo(self,data):
        self._selected = data