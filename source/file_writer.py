from source.file_handler import FileHandler

class FileWriter(FileHandler):      
    def writeTextToFileToSaveTo(self,text):
        if self._settings.filesToSaveTo:
            outputFileName = self._settings.filesToSaveTo
        else:
            outputFileName = self._GUI.askToSaveToFile()
        self._folderAdapter.writeContentToFileWithName(text,outputFileName)

            
            