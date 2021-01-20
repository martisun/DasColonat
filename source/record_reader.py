from source.record_interpreter import RecordInterpreterMaker
from source.role_interpreter import RoleInterpreter

class RecordReader(object):    
    def __init__(self,roleOfMain):
        self.__roleOfMain = roleOfMain
        
    def readPeopleFrom(self,parsedRecords):
        # main run
        print('l.11 record_reader.py REFACTORING!!!')
        mainPID = [record[self.__roleOfMain]['PID'] for record in parsedRecords\
                   if self.__roleOfMain in record][0]
        peopleCollected = self.__readPersonWithPIDFrom(mainPID,parsedRecords)
        # spouse run
        spousePID = peopleCollected['spouse']['PID']
        tmpCollected = self.__readPersonWithPIDFrom(spousePID,parsedRecords)
        spouseEntry = {**peopleCollected['spouse'],**tmpCollected['main']}
        #if 'father' in tmpCollected:
        #    spouseEntry = {**spouseEntry,'father':tmpCollected['father']}
        #if 'mother' in tmpCollected:
        #    spouseEntry = {**spouseEntry,'mother':tmpCollected['mother']}
        self.__addUniqueRoleWithData('spouse',spouseEntry,peopleCollected)
        return peopleCollected
    
    def __addRelativeRolesToData(self,data):
        dataWithRelativeRoles = {'main':data['main']}
        for key in data:
            if key in ['father','mother']:
                dataWithRelativeRoles['main'][key] = data[key]
            elif key != 'main':
                dataWithRelativeRoles[key] = data[key]
        return dataWithRelativeRoles
    
    def __readPersonWithPIDFrom(self,mainPID,parsedRecords):
        peopleCollected = {}
        for record in parsedRecords:
            roleOfMain = [role for role in record if 'PID' in record[role]\
                            and record[role]['PID'] == mainPID]
            if roleOfMain:
                self.__interpreter = RecordInterpreterMaker.forRoleOfMain(roleOfMain[0])
                peopleData = self.__collectPeopleDataFrom(record)
                self.__addPeople(peopleData,peopleCollected)
        peopleCollected = self.__addRelativeRolesToData(peopleCollected)
        return peopleCollected
    
    def __collectPeopleDataFrom(self,parsedRecord):
        self.__interpreter.setParsedRecordTo(parsedRecord)
        return self.__interpreter.interpret()    
    
    def __addPeople(self,peopleData,peopleCollected):
        for role in peopleData: self.__addRoleWithData(role,peopleData[role],peopleCollected)
        
    def __addRoleWithData(self,role,inputData,peopleCollected):
        if not self.__isRoleRecorded(role,peopleCollected):
            self.__addUniqueRoleWithData(role,inputData,peopleCollected)
        elif role == RoleInterpreter.nonUniqueRole:
            self.__addNonUniqueRoleWithData(role,inputData,peopleCollected)
        
    def __addUniqueRoleWithData(self,role,inputData,peopleCollected):
        peopleCollected[role] = inputData
        
    def __addNonUniqueRoleWithData(self,role,inputData,peopleCollected):
        candidate      = inputData[0]
        pidOfCandidate = candidate['PID']
        alreadyPIDs = [person for person in peopleCollected[role]
                       if pidOfCandidate == person['PID']]
        print('l.48 record_reader.py refactoring!')
        if not alreadyPIDs:
            peopleCollected[role].append(candidate)
        else:
            personToAddTo = alreadyPIDs[0]
            if not isinstance(personToAddTo['date'],list): 
                personToAddTo['denom'] = [(personToAddTo['denom'][count]+candidate['denom'][count])
                                          for count in range(2)]
                personToAddTo['date'] = [personToAddTo['date'],candidate['date']]
    
    def __isRoleRecorded(self,role,peopleCollected):
        return (role in peopleCollected)