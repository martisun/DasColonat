from source.record_interpreter import RecordInterpreterMaker
from source.role_interpreter import RoleInterpreter

class RecordReader(object):    
    def __init__(self,pidOfMain):
        self.__pidOfMain = pidOfMain
        
    def readPeopleFrom(self,parsedRecords):
        print('l.14 record_reader.py refactoring')
        peopleCollected = self.__readPersonWithPIDFrom(self.__pidOfMain,parsedRecords)
        return self.__addDataForSpouseIntoCollectedFromRecords(peopleCollected,parsedRecords)   
    
    def __addDataForSpouseIntoCollectedFromRecords(self,peopleCollected,parsedRecords):
        spouseEntry = self.__determineFullSpouseEntryFromRecords(peopleCollected,parsedRecords)
        self.__addUniqueRoleWithData('spouse',spouseEntry,peopleCollected)
        return peopleCollected
    
    def __determineFullSpouseEntryFromRecords(self,peopleCollected,parsedRecords):
        spousePID = peopleCollected['spouse']['PID']
        addSpouseCollected = self.__readPersonWithPIDFrom(spousePID,parsedRecords)
        return {**peopleCollected['spouse'],**addSpouseCollected['main']}
    
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
    
    def __addRelativeRolesToData(self,data):
        dataWithRelativeRoles = {'main':data['main']}
        for key in data:
            if key in ['father','mother']:
                dataWithRelativeRoles['main'][key] = data[key]
            elif key != 'main':
                dataWithRelativeRoles[key] = data[key]
        return dataWithRelativeRoles    
    
    def __collectPeopleDataFrom(self,parsedRecord):
        self.__interpreter.setParsedRecordTo(parsedRecord)
        return self.__interpreter.interpret()    
    
    def __addPeople(self,peopleData,peopleCollected):
        for role in peopleData:
            if self.__isRoleRecorded(role,peopleCollected):
                self.__addDataForRole(role,peopleCollected[role],peopleData[role])
            else: self.__addUniqueRoleWithData(role,peopleData[role],peopleCollected)
    
    def __addUniqueRoleWithData(self,role,candidate,peopleCollected):
        peopleCollected[role] = candidate
    
    def __addDataForRole(self,role,currentEntry,inputData):            
        if self.__isRoleNonUnique(role):
            self.__addNonUniqueRoleWithData(currentEntry,inputData)
        else:
            self.__mergeCandidateWithExistingEntry(currentEntry,inputData)
        
    def __addNonUniqueRoleWithData(self,currentEntry,inputData):
        candidate      = inputData[0]
        pidOfCandidate = candidate['PID']
        alreadyPIDs = [person for person in currentEntry
                       if pidOfCandidate == person['PID']]
        print('l.48 record_reader.py refactoring!')
        if not alreadyPIDs:
            currentEntry.append(candidate)
        else:
            self.__mergeCandidateWithExistingEntry(alreadyPIDs[0],candidate)
    
    def __mergeCandidateWithExistingEntry(self,currentEntry,candidate):
        if 'date' in currentEntry and 'date' in candidate\
        and not isinstance(currentEntry['date'],list): 
            currentEntry['denom'] = [(currentEntry['denom'][count]+candidate['denom'][count])
                                      for count in range(2)]
            currentEntry['date'] = [currentEntry['date'],candidate['date']]          
    
    def __isRoleNonUnique(self,role):
        return role == RoleInterpreter.nonUniqueRole
    
    def __isRoleRecorded(self,role,peopleCollected):
        return (role in peopleCollected)