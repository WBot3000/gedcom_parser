from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
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
                newId: str = self.check_unique_id_and_fix(unit.id)
                unit.id = newId
            self.indi_map.update({unit.id: unit})
        elif(isinstance(unit, Family)):
            dup_check: Family = self.fam_map.get(unit.id, None)
            if(dup_check is not None):
                newId: str = self.check_unique_id_and_fix(unit.id)
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

    
    #US04 - Marriage before divorce
    #Marriage should occur before divorce of spouses, and divorce can only occur after marriage
    def marriage_before_divorce(self):
        for fam in self.fam_map.values():
            if fam.marriageDate and fam.divorceDate and fam.divorceDate < fam.marriageDate:
                    self.errors.append(ReportDetail("Divorce Before Marriage", "Divorce of " + fam.id + " (" + str(fam.divorceDate) + ") occurs before their marriage (" + str(fam.marriageDate) + ")"))
            elif fam.divorceDate and not fam.marriageDate:
                    self.errors.append(ReportDetail("Divorce Without Marriage", "Divorce of " + fam.id + " (" + str(fam.divorceDate) + ") occurs without a recorded marriage date."))


    # US05 - Marriage before death  
    # Marriage should occur before death of either spouse
    def marriage_before_death(self):
        for fam in self.fam_map.values():
            self.check_marriage_before_death(fam.husbandId, fam)
            self.check_marriage_before_death(fam.wifeId, fam)

    def check_marriage_before_death(self, spouse_id, family):
        spouse = self.indi_map.get(spouse_id)
        
        if spouse and spouse.deathDate and spouse.deathDate < family.marriageDate:
            error_message = f"Marriage of {family.id} ({family.marriageDate}) occurs after the death of {spouse.name} ({spouse.deathDate})"
            self.errors.append(ReportDetail("Marriage After Death", error_message))


    #US06 - Divorce before death
    # Divorce can only occur before death of both spouses
    def divorce_before_death(self):
        for fam in self.fam_map.values():
            if fam.divorceDate:
                husband = self.indi_map.get(fam.husbandId, None)
                wife = self.indi_map.get(fam.wifeId, None)
                if (husband and husband.deathDate and fam.divorceDate > husband.deathDate):
                    self.errors.append(ReportDetail("Divorce After Death", f"Divorce for family {fam.id} ({fam.divorceDate}) occurs after the death of the husband ({husband.deathDate})"))
                if (wife and wife.deathDate and fam.divorceDate > wife.deathDate):
                    self.errors.append(ReportDetail("Divorce Afte Death", f"Divorce for family {fam.id} ({fam.divorceDate}) occurs after the death of the wife ({wife.deathDate})"))


    #US07 - Less than 150 years old
    # Make sure all individuals are less than 150 years old
    def check_max_age(self):
        for indi in self.indi_map.values():
            if(indi.birthDate):
                age: int = indi.calculateAge()
                if(age > 150):
                    self.errors.append(ReportDetail("Over 150 Years Old", f"{indi.id} is over 150 years old ({age} years old)"))

        
    #US10 - Marriage after 14
    # Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    def marriage_after_14(self):
        for fam in self.fam_map.values():
            husband = self.indi_map.get(fam.husbandId, None)
            if(husband and husband.birthDate and fam.marriageDate):
                if (fam.marriageDate.month < husband.birthDate.month or fam.marriageDate.month == husband.birthDate.month and fam.marriageDate.day < husband.birthDate.day):
                    if (fam.marriageDate.year - husband.birthDate.year - 1 < 14):
                        self.anomalies.append(ReportDetail("Marriage Before 14", "Marriage for " + husband.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(husband.birthDate) + ")"))
                else:
                    if (fam.marriageDate.year - husband.birthDate.year < 14):
                        self.anomalies.append(ReportDetail("Marriage Before 14", "Marriage for " + husband.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(husband.birthDate) + ")"))
            wife = self.indi_map.get(fam.wifeId, None)
            if(wife and wife.birthDate and fam.marriageDate):
                if (fam.marriageDate.month < wife.birthDate.month or fam.marriageDate.month == wife.birthDate.month and fam.marriageDate.day < wife.birthDate.day):
                    if (fam.marriageDate.year - wife.birthDate.year - 1 < 14):
                        self.anomalies.append(ReportDetail("Marriage Before 14", "Marriage for " + wife.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(wife.birthDate) + ")"))
                else:
                    if (fam.marriageDate.year - wife.birthDate.year < 14):
                        self.anomalies.append(ReportDetail("Marriage Before 14", "Marriage for " + wife.id + " (" +  str(fam.marriageDate) + ") occurs before 14 (" + str(wife.birthDate) + ")"))

    #Calculate divorce date
    def get_divorceDate (self, family):
        husband = self.indi_map.get(family.husbandId, None)
        wife = self.indi_map.get(family.wifeId, None)
        if family.divorceDate:
            divorceDate = family.divorceDate
        elif husband and wife and husband.deathDate and wife.deathDate and husband.deathDate > wife.deathDate:
            divorceDate = wife.deathDate
        elif husband and wife and husband.deathDate and wife.deathDate and wife.deathDate > husband.deathDate:
            divorceDate = husband.deathDate
        elif husband and wife and husband.deathDate and wife.deathDate == None:
            divorceDate = husband.deathDate
        elif husband and wife and wife.deathDate and husband.deathDate == None:
            divorceDate = wife.deathDate
        else:
            divorceDate = None
        return divorceDate

    #US11 - No bigamy
    # Marriage should not occur during marriage to another spouse
    def check_bigamy(self):
        bigamy_true = []
        for fam in self.fam_map.values():
            if fam.id in bigamy_true:
                continue
            husband = self.indi_map.get(fam.husbandId, None)
            wife = self.indi_map.get(fam.wifeId, None)
            marriageDate = fam.marriageDate
            divorceDate = self.get_divorceDate(fam)
            if husband and len(husband.spouseIn) > 1:
                for famId in husband.spouseIn:
                    if famId != fam.id:
                        family = self.fam_map.get(famId, None)
                        if family is None:
                            continue
                        marriageDateNew = family.marriageDate
                        divorceDateNew = self.get_divorceDate(family)
                        if divorceDate is not None and divorceDateNew is not None:
                            if marriageDate and marriageDateNew and marriageDate < marriageDateNew and divorceDate > marriageDateNew:
                                bigamy_true.append(famId)
                                self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + husband.id + " and families are " + fam.id + " and " + famId))
                            elif marriageDate and marriageDateNew and marriageDate > marriageDateNew and divorceDateNew > marriageDate:
                                bigamy_true.append(famId)
                                self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + husband.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDate and marriageDateNew and divorceDateNew is None and divorceDate > marriageDateNew:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + husband.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDateNew and marriageDate and divorceDate is None and marriageDate < divorceDateNew:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + husband.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDate is None and divorceDateNew is None:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + husband.id + " and families are " + fam.id + " and " + famId))
            if wife and len(wife.spouseIn) > 1:
                for famId in wife.spouseIn:
                    if famId != fam.id:
                        family = self.fam_map.get(famId, None)
                        if family is None:
                            continue
                        marriageDateNew = family.marriageDate
                        divorceDateNew = self.get_divorceDate(family)
                        if divorceDate is not None and divorceDateNew is not None:
                            if marriageDate and marriageDateNew and marriageDate < marriageDateNew and divorceDate > marriageDateNew:
                                bigamy_true.append(famId)
                                self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + wife.id + " and families are " + fam.id + " and " + famId))
                            elif marriageDate and marriageDateNew and marriageDate > marriageDateNew and divorceDateNew > marriageDate:
                                bigamy_true.append(famId)
                                self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + wife.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDate and marriageDateNew and divorceDateNew is None and divorceDate > marriageDateNew:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + wife.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDateNew and marriageDate and divorceDate is None and marriageDate < divorceDateNew:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + wife.id + " and families are " + fam.id + " and " + famId))
                        elif divorceDate is None and divorceDateNew is None:
                            bigamy_true.append(famId)
                            self.anomalies.append(ReportDetail("Bigamy", "Spouse details are: " + wife.id + " and families are " + fam.id + " and " + famId))


    #US12 - Parents not too old
    # This checks all of the families and compares the ages of both parents to their 
    def check_parent_child_age_difference(self):
        for fam in self.fam_map.values():
            #Store the information and age for the kids in the array so all that doesn't have to be fetched twice (once for father, once for mother)
            kidsInfo: list[str] = []
            kidsAges: list[int] = []
            if(len(fam.childIds) == 0 or (fam.husbandId is None and fam.wifeId is None)): #Don't bother if there's no children or no parents
                continue
            else:
                kidsInfo = list(filter(lambda kid: kid.birthDate is not None, map(lambda kidId: self.indi_map.get(kidId, None), fam.childIds))) #Get the information of all the kids, and remove the ones without birthdays
                kidsAges = list(map(lambda kid: kid.calculateAge(), kidsInfo)) #Get all fo their ages
            dadInfo: Individual = self.indi_map.get(fam.husbandId, None)
            if(dadInfo and dadInfo.birthDate):
                dadTooOldFor: list[str] = [] #The ids of all the kids that the dad is more than 80 years older than
                dadAge: int = dadInfo.calculateAge()
                for i in range(len(kidsInfo)):
                    if dadAge - kidsAges[i] > 80: #Father is over 80 years older than this child
                        dadTooOldFor.append(kidsInfo[i].id)
                if(len(dadTooOldFor) > 0):
                    self.anomalies.append(ReportDetail("Parent Too Old", f"Father in family {fam.id} is over 80 years older than one or more of his children {dadTooOldFor}"))
            momInfo: Individual = self.indi_map.get(fam.wifeId, None)
            if(momInfo and momInfo.birthDate):
                momTooOldFor: list[str] = [] #The ids of all the kids that the mom is more than 60 years older than
                momAge: int = momInfo.calculateAge()
                for i in range(len(kidsInfo)):
                    if momAge - kidsAges[i] > 60: #Mom is over 60 years older than this child
                        momTooOldFor.append(kidsInfo[i].id)
                if(len(momTooOldFor) > 0):
                    self.anomalies.append(ReportDetail("Parent Too Old", f"Mother in family {fam.id} is over 60 years older than one or more of her children {momTooOldFor}"))
            
            


    #US14 - Multiple births <= 5
    # No more than five siblings born at the same time
    def check_multiple_births(self):
        for fam in self.fam_map.values():
            birth_dates = {}  # Dictionary to store birth dates and their counts
            for child_id in fam.childIds:
                child = self.indi_map.get(child_id, None)
                if child and child.birthDate:
                    birth_date = child.birthDate
                    if birth_date in birth_dates:
                        birth_dates[birth_date] += 1
                    else:
                        birth_dates[birth_date] = 1
            for date, count in birth_dates.items():
                if count > 5:
                    self.anomalies.append(ReportDetail("Multiple Births", f"More than five siblings were born on {date} in family {fam.id}."))


    # US15 - Fewer than 15 siblings
    def fewer_than_15_siblings(self):
    # Iterate through all families in the GEDCOM file
        for fam in self.fam_map.values():
        # Check the number of children (siblings) in the family
            if len(fam.childIds) >= 15:
            # If there are 15 or more children, add an error to the report
            # This means that the family has too many siblings
                error_message = f"Family {fam.id} has 15 or more children"
                self.anomalies.append(ReportDetail("Too Many Siblings", error_message))

    
    #US16 - Male last names
    #Makes sure that all male members of a family share the same last name
    def get_surname(self, name: str):
        surnameStartPos: int = name.find("/")
        if(surnameStartPos == -1): #No slashes present, so no surname. Just return the empty string.
            return ""
        surnameEndPos: int = name.find("/", surnameStartPos+1) #Find the next slash after the previous one
        if(surnameEndPos == -1): #If that's the only slash present, then just assume that the last name is until the end of the name
            surnameEndPos = len(name)
        if(surnameStartPos+1 == surnameEndPos): #Have encountered two slashes next to each other, this name is empty
            return ""
        else: #Assumes that there's at least one character in the name, which is why the previous check is needed
            return name[surnameStartPos+1:surnameEndPos]


    def check_family_male_surnames(self):
        for fam in self.fam_map.values():
            male_surnames: list[str] = []
            #First, check the husband of the family
            husband: Individual = self.indi_map.get(fam.husbandId, None)
            if(husband and husband.name):
                #Since the husband is always the first person checked, just put their last name in automatically
                male_surnames = [self.get_surname(husband.name)]
            for id in fam.childIds:
                child: Individual = self.indi_map.get(id, None)
                if(child and child.name and child.sex == "M"):
                    child_surname: str = self.get_surname(child.name)
                    if(child_surname not in male_surnames):
                        male_surnames.append(child_surname)
            if(len(male_surnames) > 1):
                self.anomalies.append(ReportDetail("Differing Male Surnames", f"Males in family {fam.id} have several different surnames {male_surnames}")) 


    # US17: No Marriage to Descendants
    # Marriage between ancestors and descendants is not allowed.

    # Helper function to get descendants of an individual.
    def get_descendants(self, individual_id):
        descendants = set()
        for family in self.fam_map.values():
            if family.husbandId == individual_id or family.wifeId == individual_id:
                for child_id in family.childIds:
                    descendants.add(child_id)
                    if(child_id != individual_id): #To prevent infinite recursion when a child is marked as their own parent
                        descendants.update(self.get_descendants(child_id))
        return descendants

    def no_marriage_to_descendants(self):
        # Iterate through individuals.
        for ind in self.indi_map.values():
            # Get descendants of the current individual.
            descendants = self.get_descendants(ind.id)
            if descendants:
                # Iterate through families associated with the current individual.
                for fam_id in ind.spouseIn:
                    family = self.fam_map.get(fam_id, None)
                    if family is not None:
                        husband_id = family.husbandId
                        wife_id = family.wifeId

                        # Check if either the husband or wife is a descendant of the current individual.
                        if husband_id in descendants or wife_id in descendants:
                            if ind.id == husband_id and husband_id not in family.childIds: #Second check is to prevent incorrect recursive descendants
                                otherIndi = self.indi_map.get(wife_id, None)
                                otherIndiId = "NA" if otherIndi is None else otherIndi.id
                                # Add a note about the marriage if the current individual is the husband.
                                self.anomalies.append(ReportDetail("Marriage to Descendant",
                                    f"{ind.id} is married to descendant, {otherIndiId}."))
                            elif wife_id not in family.childIds:
                                otherIndi = self.indi_map.get(husband_id, None)
                                otherIndiId = "NA" if otherIndi is None else otherIndi.id
                                # Add a note about the marriage if the current individual is the wife.
                                self.anomalies.append(ReportDetail("Marriage to Descendant",
                                    f"{ind.id} is married to descendant, {otherIndiId}."))
                      

    #US19
    def first_cousins_should_not_marry(self):
        # Create a dictionary to store the families of the grandparents of each individual
        grandparents = {}

        # Iterate through all families in the GEDCOM file
        for fam in self.fam_map.values():
            # Check if the family has children (individuals)
            if fam.childIds:
                # Get the grandparents (parents of the parents)
                father = self.indi_map.get(fam.husbandId, None)
                mother = self.indi_map.get(fam.wifeId, None)

                patGrandpa = None
                patGrandma = None
                matGrandpa = None
                matGrandma = None

                if(father and father.childIn):
                    fatherFamily = self.fam_map.get(father.childIn, None)
                    if(fatherFamily):
                        patGrandpa = fatherFamily.husbandId
                        patGrandma = fatherFamily.wifeId

                if(mother and mother.childIn):
                    motherFamily = self.fam_map.get(mother.childIn, None)
                    if(motherFamily):
                        matGrandpa = motherFamily.husbandId
                        matGrandma = motherFamily.wifeId

                grandparentsSet = {patGrandpa, patGrandma, matGrandpa, matGrandma}
                grandparentsSet.discard(None) #Get rid of None value if it's in the set

                #if father or mother:
                for child_id in fam.childIds:
                    child = self.indi_map.get(child_id, None)
                    if child:
                        grandparents[child.id] = grandparentsSet

        # Iterate through the families to check if any have common grandparents (first cousins)
        for fam in self.fam_map.values():
            husband_parents = grandparents.get(fam.husbandId, set())
            wife_parents = grandparents.get(fam.wifeId, set())

            # Find common grandparents (first cousins)
            common_grandparents = husband_parents.intersection(wife_parents)

            # If there are common grandparents, it means first cousins are getting married
            if common_grandparents:
                error_message = f"First cousins are getting married in Family {fam.id}"
                self.anomalies.append(ReportDetail("First Cousins Marrying", error_message))


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
    #This takes a passed in ID, checks if it's a duplicate, and if it is, then note it as an error and change it to make it unique
    #Right now, if the shared ID is used in a family, it will automatically assume it's meant for the first person. I don't think there's a way to account for this given the limitations of GEDCOM files
    def check_unique_id_and_fix(self, id) -> str:
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

    # US35 - List recent births
    def list_recent_births(self, days_threshold=30):
        self.recent_births = []  # Clear the previous list
        current_date = datetime.now()
        threshold_date = current_date - timedelta(days=days_threshold)

        for individual_id, individual in self.individuals.items():
            if individual.birth_date is not None and individual.birth_date >= threshold_date:
                self.recent_births.append(individual)

        # Sort recent_births by birth date
        self.recent_births.sort(key=lambda x: x.birth_date)

    # US36 - List recent deaths
    def list_recent_deaths(self, days_threshold=30):
        self.recent_deaths = []  # Clear the previous list
        current_date = datetime.now()
        threshold_date = current_date - timedelta(days=days_threshold)

        for individual_id, individual in self.individuals.items():
            if individual.death_date is not None and individual.death_date >= threshold_date:
                self.recent_deaths.append(individual)

        # Sort recent_deaths by death date
        self.recent_deaths.sort(key=lambda x: x.death_date)


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
