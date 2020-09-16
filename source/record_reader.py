from source.record_interpreter import RecordInterpreter
from source.role_interpreter import RoleInterpreter

class RecordReader(object):    
    def __init__(self,roleOfMain):
        self.__roleOfMain = roleOfMain
        self.__peopleCollected = {}
        
    def readPeopleFrom(self,parsedRecords):     
        for record in parsedRecords:
            peopleData = self.__collectPeopleDataFrom(record)
            self.__addPeople(peopleData)
        return self.__peopleCollected
    
    def __addPeople(self,peopleData):
        for role in peopleData: self.__addRoleWithData(role,peopleData[role])
        
    def __addRoleWithData(self,role,inputData):
        if not self.__isRoleRecorded(role):
            self.__addUniqueRoleWithData(role,inputData)
        elif role == RoleInterpreter.nonUniqueRole:
            self.__addNonUniqueRoleWithData(role,inputData)
        
    def __addUniqueRoleWithData(self,role,inputData):
        self.__peopleCollected[role] = inputData
        
    def __addNonUniqueRoleWithData(self,role,inputData):
        self.__peopleCollected[role] += inputData
    
    def __collectPeopleDataFrom(self,parsedRecord):
        recordInterpreter = RecordInterpreter()
        recordInterpreter.setParsedRecordTo(parsedRecord)
        recordInterpreter.setRoleOfMainTo(self.__roleOfMain)
        return recordInterpreter.interpret()
    
    def __isRoleRecorded(self,role):
        return (role in self.__peopleCollected)