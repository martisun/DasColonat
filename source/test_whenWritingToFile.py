from source.extended_testcase import ExtendedTestCase
from source.mock_gui import MockGUIInspector
from source.mock_file import MockFolderAdapter
from source.file_writer import FileWriter
from source.settings import Settings

class whenWritingToFile(ExtendedTestCase,MockGUIInspector):
    def test_whenSettingEmptyThenAskForInput(self):
        self._initializeMockGUI()
        fileWriter = FileWriter()
        fileWriter.setGUITo(self.theGUI)
        fileWriter.setFolderAdapterTo(MockFolderAdapter())
        self.theSettings = Settings() 
        fileWriter.setSettingsTo(self.theSettings)
        fileWriter.writeTextToFileToSaveTo('')
        self._assertGUIWasRunWithActionsAndArguments('As','')   