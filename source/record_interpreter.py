from source.role_interpreter import RoleInterpreter

class RecordInterpreter(object):
    __rolesForSummary          = ['main','spouse','children'] 
    __roleSpecificImplicitData = {'father':{'gender':'m'},
                                  'mother':{'gender':'f'}}
    
    def interpret(self):
        self.__interpretRoleSpecificImplicitData()
        peopleData = self.__collectRolesForSummary()
        return peopleData
    
    def setParsedRecordTo(self,parsedRecord):
        self.__record = parsedRecord  
        
    def setRoleOfMainTo(self,roleOfMain):
        self.__roleInterpreter = RoleInterpreter.forRole(roleOfMain)
        self.__roleInterpreter.setRecordTo(self.__record)
        
    def __collectRolesForSummary(self):
        peopleData = {}
        for role in RecordInterpreter.__rolesForSummary:
            peopleData.update(self.__roleInterpreter.getRelativeRoleInRecord(role))
        return peopleData 
         
    def __interpretRoleSpecificImplicitData(self):
        for role in self.__record: self.__updateRecordForRole(role)
    
    def __updateRecordForRole(self,role):
        if role in self.__roleSpecificImplicitData:
            self.__record[role].update(self.__roleSpecificImplicitData[role])      