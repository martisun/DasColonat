import unittest
from mock import patch

from source.create_summary import *

class whenNoInput(unittest.TestCase):
    @patch('os.listdir',return_value=[])
    def test_whenInputDirectoryEmptyThenRaiseError(self,patched_os_listdir):
        self.assertRaises(NoInputError,createSummary)
    