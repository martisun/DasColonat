from source.test_whenUsingMockFile import whenUsingMockFile

from source.settings import Settings
from source.task_manager import TaskManager
from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter

from source.default_settings import getDefaultTestSettings,PrimalTestInput

class whenUsingTaskManager(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
        self._testInput = PrimalTestInput()
        defaultTestSettings = getDefaultTestSettings()
        self.defaultTestFileToLoadFrom = defaultTestSettings['filesToLoadFrom'][0]
        
    def _writeContentToDefaultFile(self,desiredFileContent):
        desiredFileName    = self.defaultTestFileToLoadFrom
        self._writeContentToFileWithName(desiredFileContent,desiredFileName) 
        
    def _setupAndRunTaskManagerThenGetOutputAsText(self,pidOfMain):
        settings    = self.__setupGoldSettingsWithMain(pidOfMain)
        taskManager = self.__setupTaskManagerWithSettings(settings) 
        taskManager.run()
        return self.__readContentFromDefaultFile()
    
    def __setupGoldSettingsWithMain(self,pidOfMain):
        defaultTestSettings = getDefaultTestSettings()
        settings = Settings.setTo(defaultTestSettings)
        settings.updateWith({'pidOfMain':pidOfMain})
        return settings
    
    def __setupTaskManagerWithSettings(self,settings):
        taskManager = TaskManager()
        taskManager.setGUITo(MockGUI())
        taskManager.setFolderAdapterTo(self.folderAdapter)
        taskManager.setSettingsTo(settings)
        return taskManager
    
    def __readContentFromDefaultFile(self):
        defaultTestSettings = getDefaultTestSettings()
        fileNameWithSavedData = defaultTestSettings['filesToSaveTo']
        return self._readContentFromFileWithName(fileNameWithSavedData)         