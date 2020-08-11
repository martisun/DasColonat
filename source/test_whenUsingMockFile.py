import builtins
from mock import patch

from source.extended_testcase import ExtendedTestCase
from source.mock_file import MockFile, MockFolder

class whenUsingMockFile(ExtendedTestCase):
    def _writeContentToFileWithName(self,content,fileName):
        with self.folderAdapter.open(fileName,'w') as fileObject:
            fileObject.write(content)
        
    def _readContentFromFileWithName(self,fileName):
        with self.folderAdapter.open(fileName,'r') as fileObject:
            content = fileObject.read()
        return content
    
    def _assertThatFileContentEquals(self,content):
        self._assertActualEqualsExpected(self.fileObject.read(),content)
        
    def _assertFileWasRunWithActionsAndArguments(self,actions,arguments=[]):
        self.assertTrue(self.fileObject.wasObjectRunWithActionsAndArguments(actions,arguments))

    def _assertFolderWasRunWithActionsAndArguments(self,actions,arguments=[]):
        self.assertTrue(self.folderAdapter.wasObjectRunWithActionsAndArguments(actions,arguments))
        
class whenFileOpenedForWriting(whenUsingMockFile): 
    def setUp(self):
        self.folderAdapter = MockFolder()
        self.fileObject = self.folderAdapter.open('a.txt','w')
    
    def test_outputEqualsEmptyInput(self):
        self._assertThatFileContentEquals('')
           
    def test_whenWriteThenOpenedWithPermission(self):
        self.fileObject.write('b')
        self._assertFolderWasRunWithActionsAndArguments('O',[['a.txt','w']])
        
    def test_whenDoneWritingThenCloseFile(self):
        self.fileObject.write('c')
        self.fileObject.close()
        self._assertFolderWasRunWithActionsAndArguments('O',[['a.txt','w']])
        self._assertFileWasRunWithActionsAndArguments('IWC',['c']) 
        
    def test_whenFileNotClosedThenContentNotAvailable(self):
        self.fileObject.write('a')
        self._assertThatFileContentEquals('')
        self.fileObject.close()
        self._assertThatFileContentEquals('a')
        
class whenOpeningWithWith(whenUsingMockFile):    
    def test_whenOpeningWithWithThenProperFile(self):
        self.folderAdapter = MockFolder()
        with self.folderAdapter.open('a.txt','w') as fileObject: fileObject.write('d')        
        self.fileObject = fileObject
        self._assertFolderWasRunWithActionsAndArguments('O',[['a.txt','w']]) 
        self._assertFileWasRunWithActionsAndArguments('IWC',['d']) 
        
class whenReadingFile(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolder()
    
    def test_whenNotWrittenRaisesFileNotFoundError(self):
        with self.assertRaises(FileNotFoundError): self.folderAdapter.open('a.txt','r')
    
    def test_whenOtherWrittenThenRaisesFileNotFoundError(self):
        with self.folderAdapter.open('a.txt','w') as fileObject: 
            fileObject.write('d')
        with self.assertRaises(FileNotFoundError): self.folderAdapter.open('b.txt','r')
        
class whenFileWasCreated(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolder()
        with self.folderAdapter.open('a.txt','w') as fileObject: 
            fileObject.write('d')
        self.fileObject = fileObject
        
    def test_whenWrittenThenNoError(self):   
        self.fileObject = self.folderAdapter.open('a.txt','r')
        content = self.fileObject.read()
        self._assertActualEqualsExpected(content,'d') 
        
    def test_whenReadingWithWith(self):
        with self.folderAdapter.open('a.txt','r') as fileObject:
            content = fileObject.read()
        self._assertActualEqualsExpected(content,'d') 
        
        