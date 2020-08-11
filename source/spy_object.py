class SpyObject(object):
    def __init__(self):
        self.__actions = ''
        self.__arguments = []
    
    def wasObjectRunWithActionsAndArguments(self,actions,arguments):
        assertion = (self.__wereActionsCalled(actions) and\
                     self.__wereArgumentsCalled(arguments))
        if not assertion: self.dumpActionsAndArguments()
        return assertion
    
    def dumpActionsAndArguments(self):
        print('\nactions:   %s'%self.__actions)
        print('arguments: %s'%self.__arguments)
    
    def _logCall(self,argument,actionId):
        if not argument is None: self.__arguments.append(argument)
        self.__actions += actionId
    
    def __wereActionsCalled(self,actions):
        return self.__doReply('actions',actions,self.__actions)
    
    def __wereArgumentsCalled(self,arguments):
        if type(arguments) == str: arguments=  [arguments]
        arguments = [el for el in arguments if el != '']
        return self.__doReply('arguments',arguments,self.__arguments)
    
    def __doReply(self,nameOfReportedObject,actual,observed):
        reply = (observed == actual)
        if not reply:
            print('\nFor %s-type object\n'%type(self)+\
                  'Expected %s: %s \n'%(nameOfReportedObject,actual)+\
                  'Observed %s: %s'%(nameOfReportedObject,observed))
        return reply