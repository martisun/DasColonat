from source.record_interpreter import RecordInterpreterMaker
from source.role_interpreter import RoleInterpreter

class RecordReader(object):    
    def __init__(self,roleOfMain):
        self.__interpreter = RecordInterpreterMaker.forRoleOfMain(roleOfMain)
        self.__peopleCollected = {}
        
    def readPeopleFrom(self,parsedRecords):
        # main run
        print('l.11 record_reader.py REFACTORING!!!')
        for record in parsedRecords:
            peopleData = self.__collectPeopleDataFrom(record)
            self.__addPeople(peopleData)   
        # spouse run
        spousePID = self.__peopleCollected['spouse']['PID']
        for record in parsedRecords:
            roleOfSpouse = [role for role in record if 'PID' in record[role]\
                            and record[role]['PID'] == spousePID]
            if roleOfSpouse and roleOfSpouse[0] == 'infant':
                interpreter = RecordInterpreterMaker.forRoleOfMain(roleOfSpouse[0])
                interpreter.setParsedRecordTo(record)
                people = interpreter.interpret()
                self.__peopleCollected['spouse'] = {**self.__peopleCollected['spouse'], **people['main'],'father':people['father'],'mother':people['mother']}
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
        print('l.48 record_reader.py refactoring!')
        if not alreadyPIDs:
            self.__peopleCollected[role].append(candidate)
        else:
            personToAddTo = alreadyPIDs[0]
            personToAddTo['denom'] = [(personToAddTo['denom'][count]+candidate['denom'][count])
                                      for count in range(2)]
            personToAddTo['date'] = [personToAddTo['date'],candidate['date']]
    
    def __isRoleRecorded(self,role):
        return (role in self.__peopleCollected)