import unittest

class ExtendedTestCase(unittest.TestCase):
    def _assertSpyWasRunWithActionsAndArguments(self,actions,arguments=[]):
        assertion = (self._spyObject.wereActionsCalled(actions) and\
                     self._spyObject.wereArgumentsCalled(arguments))
        self.assertThatIsTrue(assertion)
        
    def assertThatIsTrue(self,assertion):
        if not assertion: self._spyObject.dumpActionsAndArguments()
        super().assertTrue(assertion)  