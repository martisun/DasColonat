class RoleInterpreter(object):
    __mainRole         = 'main'
    __relativeRoleData = {'father':{'spouse':'mother','children':'infant'},
                          'mother':{'spouse':'father','children':'infant'},
                          'infant':{'father':'father','mother':'mother'}}
    __uniqueRoles  = ['main','spouse','father','mother']
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
    
    def getRelativeRolesInRecord(self,roles):
        peopleData = {}
        for role in roles:
            peopleData.update(self.getRelativeRoleInRecord(role))
        return peopleData 
    
    def getRelativeRoleInRecord(self,name):
        relativeRole = self.__getRelativeRoleWithName(name)
        if self.__isRelativeRoleRecorded(relativeRole): 
            recordOfRelativeRole = self.__record[relativeRole]
            return self.__formatIntoListForNonUniqueRoles(name,recordOfRelativeRole)
        else: return {}
    
    def getPIDOfMainRoleInRecord(self):
        return self.getRelativeRoleInRecord(self.__mainRole)[self.__mainRole]['PID']
    
    def __formatIntoListForNonUniqueRoles(self,name,recordOfRelativeRole):
        if name in RoleInterpreter.__uniqueRoles: return {name:recordOfRelativeRole}
        else:                                     return {name:[recordOfRelativeRole]}
    
    def __getRelativeRoleWithName(self,name):
        if name in self.__dict: return self.__dict[name]
        
    def __isRelativeRoleRecorded(self,relativeRole):
        return relativeRole in self.__record
    
RoleInterpreter.initialize()    