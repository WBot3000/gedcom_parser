from abc import ABC, abstractmethod
from datetime import date, datetime
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

        #Used for US01 - Dates before current date. Micro-optimization so that this doesn't need to be recalculated for every date checked (since it won't change).
        self.run_date: date = datetime.today().date()
        #Used for US22 - Unique IDs. Key is ID that's attempting to be duplicated, int is the amount of times it's duplicated (used to differentiate between IDs)
        self.duplicate_id_map: dict[str, int] = {}


    #Used to add the current object to either the Individual or Family maps
    def addToReport(self, unit: GEDCOMUnit) -> None:
        if(unit is None):
            pass
        elif(isinstance(unit, Individual)):
            dup_check: Individual = self.indi_map.get(unit.id, None)
            if(dup_check is not None):
                newId: str = self.generate_unique_id(unit.id)
                unit.id = newId
            self.indi_map.update({unit.id: unit})
        elif(isinstance(unit, Family)):
            dup_check: Family = self.fam_map.get(unit.id, None)
            if(dup_check is not None):
                newId: str = self.generate_unique_id(unit.id)
                unit.id = newId
            self.fam_map.update({unit.id: unit})
        else:
            raise GEDCOMReadException("Attempting to add non-GEDCOMUnit object to either the Individual or Family maps")


    #US01 - Dates before current date
    # Make sure all of the dates present in the file occur before the scanning of the file.
    def check_for_future_dates(self, dateVal : date):
        if(dateVal and dateVal > self.run_date):
            self.errors.append(ReportDetail("Future Date", f"Date that has yet to happen ({dateVal}) has been detected"))

    #US02 - Birth before Marriage
    # This is to check if birth occurred before marriage of an individual
    def birth_before_marriage(self):
        for fam in self.fam_map.values():
            husband = self.indi_map.get(fam.husbandId, None)
            if(husband and husband.birthDate and husband.birthDate > fam.marriageDate):
                self.errors.append(ReportDetail("Birth After Marriage", "Birth of " + husband.id + " (" +  str(husband.birthDate) + ") occurred after their marriage (" + str(fam.marriageDate) + ")"))
            wife = self.indi_map.get(fam.wifeId, None)
            if(wife and wife.birthDate and wife.birthDate > fam.marriageDate):
                self.errors.append(ReportDetail("Birth After Marriage", "Birth of " + wife.id + " (" +  str(wife.birthDate) + ") occurred after their marriage (" + str(fam.marriageDate) + ")"))
    
    #US03 - Birth before Death
    # This is to check if birth occurred before death of an individual
    def birth_before_death(self):
        for indi in self.indi_map.values():
            if indi.birthDate and indi.deathDate and indi.deathDate < indi.birthDate:
                self.errors.append(ReportDetail("Birth After Death", "Birth of " + indi.id + " (" + str(indi.birthDate) + ") occurs after their death (" + str(indi.deathDate) + ")" ))

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


    #US07 - Less than 150 years old
    # Make sure all individuals are less than 150 years old
    def check_max_age(self):
        for indi in self.indi_map.values():
            if(indi.birthDate):
                age: int = indi.calculateAge()
                if(age > 150):
                    self.anomalies.append(ReportDetail("Over 150 Years Old", f"{indi.id} is over 150 years old ({age} years old)"))

        
     #US10 - Marriage after 14
    # Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    def marriage_after_14(self):
        for fam in self.fam_map.values():
            husband = self.indi_map.get(fam.husbandId, None)
            if(husband and husband.birthDate and fam.marriageDate):
                if (fam.marriageDate.month < husband.birthDate.month or fam.marriageDate.month == husband.birthDate.month and fam.marriageDate.day < husband.birthDate.day):
                    if (fam.marriageDate.year - husband.birthDate.year - 1 < 14):
                        self.errors.append(ReportDetail("Marriage After 14", "Marriage for " + husband.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(husband.birthDate) + ")"))
                else:
                    if (fam.marriageDate.year - husband.birthDate.year < 14):
                        self.errors.append(ReportDetail("Marriage After 14", "Marriage for " + husband.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(husband.birthDate) + ")"))
            wife = self.indi_map.get(fam.wifeId, None)
            if(wife and wife.birthDate and fam.marriageDate):
                if (fam.marriageDate.month < wife.birthDate.month or fam.marriageDate.month == wife.birthDate.month and fam.marriageDate.day < wife.birthDate.day):
                    if (fam.marriageDate.year - wife.birthDate.year - 1 < 14):
                        self.errors.append(ReportDetail("Marriage After 14", "Marriage for " + wife.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(wife.birthDate) + ")"))
                else:
                    if (fam.marriageDate.year - wife.birthDate.year < 14):
                        self.errors.append(ReportDetail("Marriage After 14", "Marriage for " + wife.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(wife.birthDate) + ")"))

    # US15 - Fewer than 15 siblings
    def fewer_than_15_siblings(self):
    # Iterate through all families in the GEDCOM file
        for fam in self.fam_map.values():
        # Check the number of children (siblings) in the family
            if len(fam.childIds) >= 15:
            # If there are 15 or more children, add an error to the report
            # This means that the family has too many siblings
                error_message = f"Family {fam.id} has 15 or more children"
                self.errors.append(ReportDetail("Too Many Siblings", error_message))

    
    #US21 - Correct Gender of Role
    def check_correct_gender_for_roles(self):
        # Iterate through all families in the GEDCOM file
        for fam in self.fam_map.values():
            husband_id = fam.husbandId
            wife_id = fam.wifeId
            
            # Check the husband's gender
            if husband_id:
                husband = self.indi_map.get(husband_id)
                if husband and husband.sex != "M":
                    # Add the issue to the list
                    self.errors.append(ReportDetail("Incorrect Sex", f"Husband in family {fam.id} is female"))
            
            # Check the wife's gender
            if wife_id:
                wife = self.indi_map.get(wife_id)
                if wife and wife.sex != "F":
                    # Add the issue to the list
                    self.errors.append(ReportDetail("Incorrect Sex", f"Wife in family {fam.id} is male"))


    #US22 - Unique IDs
    #TODO: Rename to mention checking for multiple IDs
    #This takes a passed in ID, checks if it's a duplicate, and if it is, then note it as an error and change it to make it unique
    #Right now, if the shared ID is used in a family, it will automatically assume it's meant for the first person. I don't think there's a way to account for this given the limitations of GEDCOM files
    def generate_unique_id(self, id) -> str:
        if(id in self.indi_map or id in self.fam_map):
            self.errors.append(ReportDetail("Duplicate IDs", id + " is already used"))
            numDuplicates: int = self.duplicate_id_map.get(id, 1) #numDuplicates is 1 less than the amount of total times the ID appears in total (since the original isn't a duplicate)
            self.duplicate_id_map.update({id: numDuplicates + 1})
            #This uses a space, since GEDCOM IDs can't have spaces in them normally (due to how the line is parsed). Therefore, this new ID will definitely be unique
            return id + " (" + str(numDuplicates) + ")"
        return id
    

    #US23 - Unique Name and Birth Date
    def check_unique_name_and_birth_date(self):
        # Dictionary to store individuals based on name and birth date
        name_birth_dict = {}

        # Iterate through all individuals in the GEDCOM file
        for indi in self.indi_map.values():
            # Check if the individual has a name and a birth date
            if indi.name and indi.birthDate:
                # Create a unique key based on name and birth date
                unique_key = f"{indi.name} {indi.birthDate}"
                
                # Check if the unique key already exists in the dictionary
                if unique_key in name_birth_dict:
                    # If the key exists, it means there's already an individual with the same name and birth date
                    # Add the issue to the list of duplicates
                    name_birth_dict[unique_key].append(indi.id)
                else:
                    # If the key doesn't exist, create a list for it and add the individual
                    name_birth_dict[unique_key] = [indi.id]

        # Iterate through the dictionary to find duplicates
        for key, duplicates in name_birth_dict.items():
            if len(duplicates) > 1:
                # If there are duplicates, create a new anomaly detailing all of them
                detailStr = ""
                for i in range(len(duplicates)):
                    #print(f"Multiple individuals with the same name '{issue[0]['name']}' and birth date '{issue[0]['birth_date']}' found:")
                    detailStr += duplicates[i]
                    if i < len(duplicates) - 1:
                        detailStr += ","
                    detailStr += " "
                sharedDetails = key.split(" ")
                sharedBDay = sharedDetails.pop()
                sharedName = ""
                for namePart in sharedDetails: #Need to reassemble the name
                    sharedName += namePart
                detailStr += f"share a name ({sharedName}) and birthday ({sharedBDay})"
                self.anomalies.append(ReportDetail("Duplicate Name and Birthdate", detailStr))

    
    #US28 - Order siblings by age
    def sort_children_by_age(self):
        def age_sorting_fn(indi_id):
            if(indi_id is None):
                return date.max
            indi_data = self.indi_map.get(indi_id, None)
            if(indi_data is None or indi_data.birthDate is None):
                return date.max
            return indi_data.birthDate

        for fam in self.fam_map.values():
            sorted_siblings = sorted(fam.childIds, key=age_sorting_fn)
            fam.childIds = sorted_siblings


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
