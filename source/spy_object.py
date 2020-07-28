class SpyObject(object):
    def __init__(self):
        self.__actions = ''
        self.__arguments = []
    
    def wereActionsCalled(self,actions):
        return self.__doReply('actions',actions,self.__actions)
    
    def wereArgumentsCalled(self,arguments):
        if type(arguments) == str: arguments=  [arguments]
        arguments = [el for el in arguments if el != '']
        return self.__doReply('arguments',arguments,self.__arguments)
    
    def dumpActionsAndArguments(self):
        print('\nactions:   %s'%self.__actions)
        print('arguments: %s'%self.__arguments)
    
    def _logCall(self,argument,actionId):
        self.__arguments.append(argument)
        self.__actions += actionId
    
    @staticmethod
    def __doReply(nameOfReportedObject,actual,observed):
        reply = (observed == actual)
        if not reply:
            print('\nExpected %s: %s \n'%(nameOfReportedObject,actual)+\
                  'Observed %s: %s'%(nameOfReportedObject,observed))
        return reply