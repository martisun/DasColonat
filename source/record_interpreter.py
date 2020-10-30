from source.role_interpreter import RoleInterpreter

class RecordInterpreter(object):
    __rolesForSummary          = ['main','spouse','children','father','mother'] 
    __roleSpecificImplicitData = {'father':{'gender':'m'},
                                  'mother':{'gender':'f'}}
    
    @staticmethod
    def forRoleOfMain(roleOfMain):
        mainRoleInterpreter = RoleInterpreter.forRole(roleOfMain)
        return RecordInterpreter(mainRoleInterpreter)
    
    def __init__(self,roleInterpreter):
        self.__pidOfMain       = ''
        self.__roleInterpreter = roleInterpreter
        
    def interpret(self):        
        self.__interpretRoleSpecificImplicitData()
        pidOfMainInRecord = self.__roleInterpreter.getPIDOfMainRoleInRecord()
        self.__setPIDofMainIfUnset(pidOfMainInRecord)
        return self.__collectRolesForSummary(pidOfMainInRecord)
    
    def setParsedRecordTo(self,parsedRecord):
        self.__record = parsedRecord
        self.__roleInterpreter.setRecordTo(self.__record)
    
    def __setPIDofMainIfUnset(self,pidOfMainInRecord):
        if not self.__pidOfMain: self.__pidOfMain = pidOfMainInRecord        
    
    def __collectRolesForSummary(self,pid):
        if self.__pidOfPersonMatchesPIDofMainRole(pid):
            return self.__collectRolesFromMatchingRecordForSummary() 
        elif self.__pidOfPersonMatchesPIDofAnyRole():
            roleOfMain = [role for role in self.__record\
                          if self.__record[role]['PID']==self.__pidOfMain][0]
            self.__roleInterpreter = RoleInterpreter.forRole(roleOfMain)
            self.__roleInterpreter.setRecordTo(self.__record)
            print('l.38 awful (working) mess!!! record_interpreter')
            return self.__collectRolesFromMatchingRecordForSummary()   
        else: return {}    
    
    def __pidOfPersonMatchesPIDofAnyRole(self):
        return any([self.__record[role]['PID']==self.__pidOfMain for role in self.__record])
        
    def __pidOfPersonMatchesPIDofMainRole(self,pid):    
        return self.__pidOfMain == pid
    
    def __collectRolesFromMatchingRecordForSummary(self):
        return self.__roleInterpreter.getRelativeRolesInRecord(self.__rolesForSummary)     
        
    def __interpretRoleSpecificImplicitData(self):
        for role in self.__record: 
            self.__updateRecordForRole(role)
    
    def __updateRecordForRole(self,role):
        if role in self.__roleSpecificImplicitData:
            self.__record[role].update(self.__roleSpecificImplicitData[role])      