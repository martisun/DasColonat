INPUT_DIR = './input'

def createSummary():
    raise NoInputError('No input-files were found in %s, no records can be loaded!'%INPUT_DIR)
    
class NoInputError(OSError):
    '''Use when required input is lacking.'''    