from abc import ABC, abstractmethod
from datetime import date

class GEDCOMUnit(ABC):
    def __init__(self, id: str):
        self.id = id

    #Used for altering data based on a line (or the line split up into its respective fields)
    #NOTE: This is not used for dates, since those go onto two lines
    @abstractmethod
    def readDataFromFields(self, fields: list[str]) -> None:
        pass

    #Used for setting date values based on the provided label
    @abstractmethod
    def setDate(self, date: date, label: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def createRowHeader() -> list[str]:
        pass

    @abstractmethod
    def getRowData(self) -> list[str]:
        pass


class Individual(GEDCOMUnit):
    def __init__(self, id: str, name: str = None, sex: str = None, birthDate: date = None, deathDate: date = None, childIn: str = None, spouseIn: list[str] = None):
        super().__init__(id)
        self.name = name
        self.sex = sex
        self.birthDate = birthDate
        self.deathDate = deathDate
        self.childIn = childIn
        self.spouseIn = [] if spouseIn is None else spouseIn #Need to do this because using the empty list as a default parameter leads to weird stuff (values become duplicated across multiple instances)

    def readDataFromFields(self, fields: list[str]) -> None:
        if(len(fields) <= 2):
            raise GEDCOMReadException("Not enough arguments for line")
        match(fields[1]):
            case "NAME":
                self.name = fields[2]
            case "SEX":
                self.sex = fields[2]
            case "FAMC":
                self.childIn = fields[2]
            case "FAMS":
                self.spouseIn.append(fields[2])
            case _:
                raise GEDCOMReadException("Specified field (" + fields[2] + ") is invalid for an Individual")
            
    def setDate(self, date: date, label: str) -> None:
        match(label):
            case "BIRT":
                self.birthDate = date
            case "DEAT":
                self.deathDate = date
            case _:
                raise GEDCOMReadException("No date field corresponding to label (" + label + ") for Individual")
            
    def calculateAge(self) -> int:
        if(self.birthDate is None):
            raise ValueError
        today: date = date.today()
        age: int = today.year - self.birthDate.year
        if(self.birthDate.month > today.month or (self.birthDate.month == today.month and self.birthDate.day > today.day)): #Subtract one if birthday month hasn't come up yet, or if birthday is this month, but day hasn't passed yet
            age = age - 1
        return age

    @staticmethod     
    def createRowHeader() -> list[str]:
        return ["ID", "Name", "Sex", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    
    def getRowData(self) -> list[str]:
        rowData: list[str] = [self.id]
        #Making sure name exists
        if(self.name is None):
            rowData.append("NA")
        else:
            rowData.append(self.name)
        #Making sure sex exists
        if(self.sex is None):
            rowData.append("NA")
        else:
            rowData.append(self.sex)
        #Making sure birthday exists and formatting it appropriately
        if(self.birthDate is None):
            rowData.append("NA") #Birth date
            rowData.append("NA") #Age
        else:
            rowData.append(str(self.birthDate.year) + "-" + str(self.birthDate.month) + "-" + str(self.birthDate.day))
            rowData.append(self.calculateAge())
        #Checking to see if death date exists, and formatting it appropriately if it does
        if(self.deathDate is None):
            rowData.append("True") #Alive
            rowData.append("NA") #Death date
        else:
            rowData.append("False")
            rowData.append(str(self.deathDate.year) + "-" + str(self.deathDate.month) + "-" + str(self.deathDate.day))
        #Making sure id of family where individual is a child exists
        if(self.childIn is None):
            rowData.append("NA")
        else:
            rowData.append(self.childIn)
        #Getting string data of all spouse IDs
        spouseStr: str = "["
        for i in range(len(self.spouseIn)):
            spouseStr = spouseStr + self.spouseIn[i]
            if(i < len(self.spouseIn) - 1):
                spouseStr = spouseStr + ", "
        spouseStr = spouseStr + "]"
        rowData.append(spouseStr)
        return rowData



class Family(GEDCOMUnit):
    def __init__(self, id: str, husbandId: str = None, wifeId: str = None, childIds: list[str] = None, marriageDate: date = None, divorceDate: date = None):
        super().__init__(id)
        self.husbandId = husbandId
        self.wifeId = wifeId
        self.childIds = [] if childIds is None else childIds #Done for the same reason this is done in the Individual class
        self.marriageDate = marriageDate
        self.divorceDate = divorceDate

    def readDataFromFields(self, fields: list[str]) -> None:
        if(len(fields) <= 2):
            raise GEDCOMReadException("Not enough arguments for line")
        match(fields[1]):
            case "HUSB":
                self.husbandId = fields[2]
            case "WIFE":
                self.wifeId = fields[2]
            case "CHIL":
                self.childIds.append(fields[2])
            case _:
                raise GEDCOMReadException("Specified field is invalid for a Family")
            
    def setDate(self, date: date, label: str) -> None:
        match(label):
            case "MARR":
                self.marriageDate = date
            case "DIV":
                self.divorceDate = date
            case _:
                raise GEDCOMReadException("No date field corresponding to label (" + label + ") for Family")
            
    @staticmethod     
    def createRowHeader() -> list[str]:
        return ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    
    #This function takes a dictionary that maps ids to individuals, as the Family object doesn't store this directly
    def getRowData(self, indiLookup: dict[str, Individual] = None) -> list[str]:
        rowData: list[str] = [self.id]
        #Checking to see if marriage date exists, and formatting it appropriately if it does
        if(self.marriageDate is None):
            rowData.append("NA")
        else:
            rowData.append(str(self.marriageDate.year) + "-" + str(self.marriageDate.month) + "-" + str(self.marriageDate.day))
        #Checking to see if divorce date exists, and formatting it appropriately if it does
        if(self.divorceDate is None):
            rowData.append("NA")
        else:
            rowData.append(str(self.divorceDate.year) + "-" + str(self.divorceDate.month) + "-" + str(self.divorceDate.day))
        #Making sure husband ID exists (and name)
        if(self.husbandId is None):
            rowData.append("NA") #Husband ID
            rowData.append("NA") #Husband Name
        else:
            rowData.append(self.husbandId)
            if(indiLookup is None):
                rowData.append("NA")
            else:
                husbandData: Individual = indiLookup.get(self.husbandId, None)
                rowData.append("NA" if (husbandData is None or husbandData.name is None) else husbandData.name)
        #Making sure wife ID exists (and name)
        if(self.wifeId is None):
            rowData.append("NA") #Wife ID
            rowData.append("NA") #Wife Name
        else:
            rowData.append(self.wifeId)
            if(indiLookup is None):
                rowData.append("NA")
            else:
                wifeData: Individual = indiLookup.get(self.wifeId, None)
                rowData.append("NA" if (wifeData is None or wifeData.name is None) else wifeData.name)
        #Getting string data of all child IDs
        childStr: str = "["
        for i in range(len(self.childIds)):
            childStr = childStr + self.childIds[i]
            if(i < len(self.childIds) - 1):
                childStr = childStr + ", "
        childStr = childStr + "]"
        rowData.append(childStr)
        return rowData
    

class GEDCOMReadException(Exception):
    def __init__(self, message="Error while reading GEDCOM file"):
        self.message = message
        super().__init__(self.message)