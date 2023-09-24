#Walker Bove, Sindhu Buggana, Sri Laya Nalmelwar, Hindu Kotha
#Assignment 3: GEDCOM Reader

import os
from datetime import date
from prettytable import PrettyTable

from GEDCOM_Classes import GEDCOMUnit, Individual, Family, GEDCOMReadException

#Storage for all of the individual records
# IDs are the keys, Individual objects are the values
indi_map: dict[str, Individual] = {}

#Storage for all of the family records
# IDs are the keys, Family objects are the values
fam_map: dict[str, Family] = {}

#The current object that's being read. Can be either an Individual or a Family
current_obj: GEDCOMUnit = None

#Used to add the current object to either the Individual or Family maps
def addToMap(unit: GEDCOMUnit) -> None:
    if(unit is None):
        pass
    elif(isinstance(unit, Individual)):
        indi_map.update({unit.id: unit})
    elif(isinstance(unit, Family)):
        fam_map.update({unit.id: unit})
    else:
        raise GEDCOMReadException("Attempting to add non-GEDCOMUnit object to either the Individual or Family maps")

#The last seen date tag. Used to determine what field to fill in
readingDateOf: str = None

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
def stringToDate(string: str) -> date:
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
        raise GEDCOMReadException("<month> of date (" + dateParts[1] + ") is not a valid string")
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



filePath = input("Give the location of the GEDCOM file you'd like to read: ")
try:
    with open(filePath, "r") as file:
        for line in file:
            try: 
                fixedLine: str = line.replace("\n", "") #Remove any newline characters
                fields: list[str] = fixedLine.split(" ", 2) #Split the line into at most three seperate parts
                numFields: int = len(fields)
                if(numFields <= 1):
                    raise GEDCOMReadException("Not enough arguments on the line")
                secondField: str = fields[1]
                match(fields[0]) : #The number of the line
                    case "0":
                        if(secondField == "HEAD" or secondField == "TRLR" or secondField == "NOTE"):
                            pass #These tags are simply for annotation, you don't need to record any data for them
                        elif(numFields == 3):
                            thirdField: str = fields[2]
                            if(fields[2] == "INDI"):
                                addToMap(current_obj) #Add current object to the map before you start with the new Individual
                                current_obj = Individual(secondField)
                            elif(fields[2] == "FAM"):
                                addToMap(current_obj) #Add current object to the map before you start with the new Family
                                current_obj = Family(secondField)
                            else:
                                raise GEDCOMReadException("Invalid tag for 0-numbered line")
                        else:
                            raise GEDCOMReadException("Invalid tag for 0-numbered line")
                    case "1":
                        #Check to make sure object exists, then check if line is specifying a type of date or just a standard field
                        if(current_obj is None):
                            raise GEDCOMReadException("No GEDCOM Unit (Individual or Family) to give field")
                        elif(secondField == "BIRT" or secondField == "DEAT" or secondField == "MARR" or secondField == "DIV"):
                            readingDateOf = secondField
                        else:
                            current_obj.readDataFromFields(fields) #TODO: Change from taking in fields to taking in tag and argument?
                    case "2":
                        #Check for errors, then set date to appropriate field
                        if(fields[1] != "DATE"):
                            raise GEDCOMReadException("Invalid tags for 2-numbered line")
                        if(numFields == 2):
                            raise GEDCOMReadException("Not enough fields for DATE")
                        if(current_obj is None):
                            raise GEDCOMReadException("No GEDCOM Unit (Individual or Family) to give field")
                        if(readingDateOf is None):
                            raise GEDCOMReadException("Type of date has not been specified")
                        dateObj: date = stringToDate(fields[2])
                        current_obj.setDate(dateObj, readingDateOf)
                        readingDateOf = None
                        pass
                    case _: #Since all lines are assumed to be syntatically correct, this technically isn't needed
                        raise GEDCOMReadException("Line number is not valid (0, 1, 2)")
            except Exception as e:
                print("Error reading line: " + e.message)

        addToMap(current_obj) #Add the latest object into the maps
        print("Done reading in data")
except OSError as e:
    print("OS Error encountered: " + os.strerror(e.errno))
except Exception as e:
    print("Error encountered: " + os.strerror(e.errno))

indiTable = PrettyTable(Individual.createRowHeader())
for indi in indi_map.values():
    indiTable.add_row(indi.createRowData())

famTable = PrettyTable(Family.createRowHeader())
for fam in fam_map.values():
    famTable.add_row(fam.createRowData(indi_map)) #Need to pass in the map of individuals so the names can be printed

print("Individuals")
print(indiTable)
print()

print("Families")
print(famTable)