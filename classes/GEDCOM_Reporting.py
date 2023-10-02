from abc import ABC, abstractmethod
from datetime import date
from prettytable import PrettyTable
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family, GEDCOMReadException

#Contains the report class used to contain all of the report data, as well as a couple of utility functions to help out

#Maps months to their integer value
monthToInt = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

#Converts GEDCOM date string into a Python date
def stringDateConversion(string: str) -> date:
    if(string == None or string == ""):
        raise GEDCOMReadException("Date is not provided")
    dateParts = string.split(" ", 2)
    if(len(dateParts) != 3):
        raise GEDCOMReadException("Date is malformed. Should consist <day> <month> <year>, where <day> and <year> are numerical values, while <month> is the first three letters of the month capitalized")
    day: int
    #Parse day
    try:
        day = int(dateParts[0])
    except ValueError:
        raise GEDCOMReadException("<day> of date (" + dateParts[0] + ") is not a valid numerical value")
    #Parse month
    month: int = monthToInt.get(dateParts[1])
    if(month is None):
        raise GEDCOMReadException("<month> of date (" + dateParts[1] + ") is not a valid month string")
    #Parse year
    year: int
    try:
        year = int(dateParts[2])
    except ValueError:
        raise GEDCOMReadException("<year> of date (" + dateParts[2] + ") is not a valid numerical value")
    #Create final date and return it
    finalDate: date
    try:
        finalDate = date(year, month, day)
    except ValueError:
        raise GEDCOMReadException(string + " is not a valid date (the day is probably too large for the current month)")
    return finalDate

#Will contain all of the data of the report, such as...
# # Errors and anomalies that are caught within the file
# # Upcoming birthdays and anniversaries
class Report():

    def __init__(self):
        #Storage for all of the individual records
        # IDs are the keys, Individual objects are the values
        self.indi_map: dict[str, Individual] = {}
        #Storage for all of the family records
        # IDs are the keys, Family objects are the values
        self.fam_map: dict[str, Family] = {}

        #TODO: Make these maps of some kind?
        #TODO: Create an object for errors/anomalies/birthdays/anniversaries
        self.errors: list[ReportDetail] = [] 
        self.anomalies: list[ReportDetail] = []
        self.upcomingBirthdays: list[ReportDetail] = []
        self.upcomingAnniversaries: list[ReportDetail] = []

        #Used for US22 - Unique IDs. Key is ID that's attempting to be duplicated, int is the amount of times it's duplicated (used to differentiate between IDs)
        self.duplicate_id_map: dict[str, int] = {}


    #Used to add the current object to either the Individual or Family maps
    #TODO: Change this to addToReport, is more clear
    def addToMap(self, unit: GEDCOMUnit) -> None:
        if(unit is None):
            pass
        elif(isinstance(unit, Individual)):
            dup_check: Individual = self.indi_map.get(unit.id, None)
            if(dup_check is not None):
                newId: str = self.generateId(unit.id)
                unit.id = newId
            self.indi_map.update({unit.id: unit})
        elif(isinstance(unit, Family)):
            dup_check: Family = self.fam_map.get(unit.id, None)
            if(dup_check is not None):
                newId: str = self.generateId(unit.id)
                unit.id = newId
            self.fam_map.update({unit.id: unit})
        else:
            raise GEDCOMReadException("Attempting to add non-GEDCOMUnit object to either the Individual or Family maps")

    
    #US05 - Marriage before death  
    # Marriage should occur before death of either spouse
    def marriage_before_death(self):
        for fam in self.fam_map.values():
            husband = self.indi_map.get(fam.husbandId, None)
            if(husband and husband.deathDate and husband.deathDate < fam.marriageDate):
                self.errors.append(ReportDetail("Marriage After Death", "Marriage for " + husband.id + " (" +  str(fam.marriageDate) + ") occurs after their death (" + str(husband.deathDate) + ")"))
            wife = self.indi_map.get(fam.wifeId, None)
            if(wife and wife.deathDate and wife.deathDate < fam.marriageDate):
                self.errors.append(ReportDetail("Marriage After Death", "Marriage for " + wife.id + " (" +  str(fam.marriageDate) + ") occurs after their death (" + str(wife.deathDate) + ")"))


    #US06 - Divorce before death
    # Divorce can only occur before death of both spouses
    def divorce_before_death(self):
        for fam in self.fam_map.values():
            husband = self.indi_map.get(fam.husbandId, None)
            wife = self.indi_map.get(fam.wifeId, None)
            
            if (husband and husband.deathDate) and (wife and wife.deathDate) and fam.divorceDate:
                if fam.divorceDate > husband.deathDate and fam.divorceDate > wife.deathDate:
                    self.errors.append(ReportDetail("Divorce After Death", f"Divorce for family {fam.id} ({(fam.divorceDate)}) occurs after the death of the husband ({str(husband.deathDate)}) and the wife ({str(wife.deathDate)})"))



    #US22 - Unique IDs
    #TODO: Rename to mention checking for multiple IDs
    #This takes a passed in ID, checks if it's a duplicate, and if it is, then note it as an error and change it to make it unique
    #Right now, if the shared ID is used in a family, it will automatically assume it's meant for the first person. I don't think there's a way to account for this given the limitations of GEDCOM files
    def generateId(self, id) -> str:
        if(id in self.indi_map or id in self.fam_map):
            self.errors.append(ReportDetail("Duplicate IDs", id + " is already used"))
            numDuplicates: int = self.duplicate_id_map.get(id, 1) #numDuplicates is 1 less than the amount of total times the ID appears in total (since the original isn't a duplicate)
            self.duplicate_id_map.update({id: numDuplicates + 1})
            #This uses a space, since GEDCOM IDs can't have spaces in them normally (due to how the line is parsed). Therefore, this new ID will definitely be unique
            return id + " (" + str(numDuplicates) + ")"
        return id


    #US42 - Reject invalid dates
    #Wrapper around conversion function. Returns None if an error occurs
    def getDateFromString(self, string: str) -> str:
        dateObj: date = None
        try:
            dateObj = stringDateConversion(string)
        except GEDCOMReadException as e:
            self.errors.append(ReportDetail("Invalid Date", e.message))
        finally:
            return dateObj


    def printReport(self) -> None:
        print("[GEDCOM File Report]")
        indiTable = PrettyTable(Individual.createRowHeader())
        for indi in self.indi_map.values():
            indiTable.add_row(indi.getRowData())

        famTable = PrettyTable(Family.createRowHeader())
        for fam in self.fam_map.values():
            famTable.add_row(fam.getRowData(self.indi_map)) #Need to pass in the map of individuals so the names can be printed

        #Will print out all of the errors stored in the error list
        errorTable = PrettyTable(["Error", "Details"])
        for error in self.errors:
            errorTable.add_row(error.getRowData())

        #Will print out all of the anomalies stored in the anomaly list
        anomalyTable = PrettyTable(["Anomaly", "Details"])
        for anomaly in self.anomalies:
            anomalyTable.add_row(anomaly.getRowData())

        #Will print out all of the upcoming birthdays stored in the birthday list
        bdayTable = PrettyTable(["Individual", "Birthday"])
        for bday in self.upcomingBirthdays:
            bdayTable.add_row(bday.getRowData())

        #Will print out all of the upcoming anniversaries stored in the anniversary list
        anniversaryTable = PrettyTable(["Family", "Anniversary"])
        for anniversary in self.upcomingAnniversaries:
            anniversaryTable.add_row(anniversary.getRowData())

        print("Individuals:")
        print(indiTable)
        print()

        print("Families:")
        print(famTable)
        print()

        print("Errors:")
        print(errorTable)
        print()

        print("Anomalies:")
        print(anomalyTable)
        print()

        print("Upcoming Birthdays:")
        print(bdayTable)
        print()

        print("Upcoming Anniversaries:")
        print(anniversaryTable)
            

#Contains all of the data regarding a certain detail to look out for during a report
#NOTE: Used to store Errors and anomalies inherit from the same class
class ReportDetail():
    def __init__(self, detailType, message):
        self.detailType = detailType
        self.message = message

    def __eq__(self, other: object) -> bool:
        if(isinstance(other, ReportDetail)):
            return self.detailType == other.detailType and self.message == other.message
        return False

    def getRowData(self):
        return [self.detailType, self.message]