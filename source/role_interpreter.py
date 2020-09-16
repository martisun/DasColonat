class RoleInterpreter(object):
    __relativeRoleData = {'father':{'spouse':'mother','children':'child'},
                          'mother':{'spouse':'father','children':'child'}}
    __uniqueRoles  = ['main','spouse']
    nonUniqueRole = 'children'
    __roleInterpreters = {}
    
    @staticmethod
    def initialize():
        for role in RoleInterpreter.__relativeRoleData:
            roleDictionary  = {**RoleInterpreter.__relativeRoleData[role],'main':role}
            roleInterpreter = RoleInterpreter(roleDictionary)
            RoleInterpreter.__roleInterpreters[role] = roleInterpreter
        
    @staticmethod
    def forRole(role):
        return RoleInterpreter.__roleInterpreters[role]
    
    def __init__(self,relativeRoleDict):
        self.__dict = relativeRoleDict   
        
    def setRecordTo(self,record):
        self.__record = record
    
    def getRelativeRoleInRecord(self,name):
        relativeRole = self.__getRelativeRoleWithName(name)
        if name in RoleInterpreter.__uniqueRoles: return self.__record[relativeRole]
        else:                                     return [self.__record[relativeRole]]
        
    def __getRelativeRoleWithName(self,name):
        return self.__dict[name]
    
RoleInterpreter.initialize()    