from source.record_interpreter import RecordInterpreterMaker
from source.role_interpreter import RoleInterpreter

class RecordReader(object):    
    def __init__(self,roleOfMain):
        self.__interpreter = RecordInterpreterMaker.forRoleOfMain(roleOfMain)
        self.__peopleCollected = {}
        
    def readPeopleFrom(self,parsedRecords):
        for record in parsedRecords:
            peopleData = self.__collectPeopleDataFrom(record)
            self.__addPeople(peopleData)   
        return self.__peopleCollected
    
    def __collectPeopleDataFrom(self,parsedRecord):
        self.__interpreter.setParsedRecordTo(parsedRecord)
        return self.__interpreter.interpret()    
    
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
        candidate      = inputData[0]
        pidOfCandidate = candidate['PID']
        alreadyPIDs = [person for person in self.__peopleCollected[role]
                       if pidOfCandidate == person['PID']]
        if not alreadyPIDs:
            self.__peopleCollected[role].append(candidate)
        else:
            personToAddTo = alreadyPIDs[0]
            personToAddTo['denom'] = [(personToAddTo['denom'][count]+candidate['denom'][count])
                                      for count in range(2)]
            personToAddTo['date'] = [personToAddTo['date'],candidate['date']]
    
    def __isRoleRecorded(self,role):
        return (role in self.__peopleCollected)