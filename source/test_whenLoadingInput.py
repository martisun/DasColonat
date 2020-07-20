import unittest
from mock import patch
from source.mocks import AnsweringTrueMockGUI, AnsweringFalseMockGUI

from source.write_summary import *

filesToLoadFrom = None

class whenLoadingInput(unittest.TestCase):
    @patch('os.listdir',return_value=[])
    def test_whenInputDirectoryEmptyThenRaiseError(self,patched_os_listdir):
        aSummaryWriter = SummaryWriter()
        self.assertRaises(NoInputError,aSummaryWriter.execute)
        
    @patch('os.listdir',return_value=['a.dat'])
    def test_whenInputDirectoryWithOneFileNoCSVFileThenRaiseError(self,patched_os_listdir):
        aSummaryWriter = SummaryWriter()        
        self.assertRaises(NoInputError,aSummaryWriter.execute)
    
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenInputDirectoryHasCSVFileThenAskToLoad(self,patched_os_listdir):
        aMockGUI = self.__getAMockGUIAfterExecuteASummaryWriter()
        self.assertTrue(aMockGUI.wereActionsCalled('A'))
        self.assertTrue(aMockGUI.wereArgumentsDuringLastCall('a.csv'))
        
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenAnswerToAskToLoadIsNoWhenOnlyOneFileInDirectory(self,patched_os_listdir):
        aMockGUI = AnsweringFalseMockGUI()
        aSummaryWriter = SummaryWriter.usingGUI(aMockGUI)
        self.assertRaises(NoInputError,aSummaryWriter.execute)
        self.assertTrue(aMockGUI.wereActionsCalled('A'))
        self.assertTrue(aMockGUI.wereArgumentsDuringLastCall('a.csv'))    
        
    @patch('os.listdir',return_value=['a.dat','b.dat'])
    def test_whenInputDirectoryWithTwoFilesNoCSVFileThenRaiseError(self,patched_os_listdir):
        aSummaryWriter = SummaryWriter()        
        self.assertRaises(NoInputError,aSummaryWriter.execute) 
        
    @patch('os.listdir',return_value=['a.dat','a.csv'])
    def test_whenInputDirectoryWithTwoFilesOneCSVFileThenAskToLoad(self,patched_os_listdir):
        aMockGUI = self.__getAMockGUIAfterExecuteASummaryWriter()
        self.assertTrue(aMockGUI.wereActionsCalled('A'))
        self.assertTrue(aMockGUI.wereArgumentsDuringLastCall('a.csv'))
        
    @patch('os.listdir',return_value=['a.csv','b.csv'])
    def test_whenInputDirectoryWithTwoCSVFilesThenAskToLoadTwice(self,patched_os_listdir):
        aMockGUI = self.__getAMockGUIAfterExecuteASummaryWriter()
        self.assertTrue(aMockGUI.wereActionsCalled('AA'))
        self.assertTrue(aMockGUI.wereArgumentsDuringLastCall('b.csv'))    
        
    def __getAMockGUIAfterExecuteASummaryWriter(self):
        aMockGUI = AnsweringTrueMockGUI()
        aSummaryWriter = SummaryWriter.usingGUI(aMockGUI)
        aSummaryWriter.execute()
        return aMockGUI
        