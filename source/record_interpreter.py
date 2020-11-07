from source.role_interpreter import RoleInterpreter

class RecordInterpreterMaker(object):    
    @staticmethod
    def forRoleOfMain(roleOfMain):
        return RecordInterpreterMaker(roleOfMain)
    
    def __init__(self,roleOfMain):
        self.__recordInterpreter = ''
        self.__roleOfMain        = roleOfMain
        
    def interpret(self):
        return self.__recordInterpreter.interpret(self.__record)
        
    def setParsedRecordTo(self,parsedRecord):
        self.__record = self.__interpretRoleSpecificallyTheRecord(parsedRecord)
        self.__setPIDofMainIfUnset()        
    
    def __getPIDOfRoleOfMain(self):
        return self.__record[self.__roleOfMain]['PID']
    
    def __interpretRoleSpecificallyTheRecord(self,record):
        interpreter = RoleSpecificImplicitInterpreter()
        return interpreter.interpret(record)
    
    def __setPIDofMainIfUnset(self):
        pidOfMainInRecord = self.__getPIDOfRoleOfMain()
        if not self.__recordInterpreter: 
            self.__recordInterpreter = RecordInterpreter(pidOfMainInRecord)           

            
class RoleSpecificImplicitInterpreter(object):
    __roleSpecificImplicitData = {'father':{'gender':'m'},
                                  'mother':{'gender':'f'}}
    
    def interpret(self,record):
        for role in record:
            self.__updateRecordForRole(record,role)
        return record
        
    def __updateRecordForRole(self,record,role):
        if role in self.__roleSpecificImplicitData:
            record[role].update(self.__roleSpecificImplicitData[role])  
            

class RecordInterpreter(object):
    __rolesForSummary          = ['main','spouse','children','father','mother'] 
    
    def __init__(self,pidOfMain):
        self.__pidOfMain = pidOfMain
        
    def interpret(self,record):
        self.__record = record 
        if self.__pidOfPersonMatchesPIDofAnyRole():
            self.__setupRoleInterpreterForMainPID()
            return self.__collectRolesFromMatchingRecordForSummary()   
        else: return {} 
    
    def __setupRoleInterpreterForMainPID(self):
        roleOfMain = self.__getRoleOfMainPID()
        self.__setupRoleInterpreterForRole(roleOfMain)                 
    
    def __getRoleOfMainPID(self):
        return [role for role in self.__record if self.__record[role]['PID']==self.__pidOfMain][0]
    
    def __setupRoleInterpreterForRole(self,role):
        self.__roleInterpreter = RoleInterpreter.forRole(role)
        self.__roleInterpreter.setRecordTo(self.__record)
    
    def __pidOfPersonMatchesPIDofAnyRole(self):
        return any([self.__record[role]['PID']==self.__pidOfMain for role in self.__record])
    
    def __collectRolesFromMatchingRecordForSummary(self):
        return self.__roleInterpreter.getRelativeRolesInRecord(self.__rolesForSummary)          