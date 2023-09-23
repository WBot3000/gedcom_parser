#Walker Bove
#Assignment 3: Improved GEDCOM Data

import os
from datetime import date

from GEDCOM_Classes import Individual, Family, GEDCOMReadException

#Valid tags for each level. The index corresponds to the level of the tag
#NOTE: "INDI" and "FAM" are not included in the level 0 tags, since those two tags are special cases that are handled using a different method
validTags = [
    ["HEAD", "TRLR", "NOTE"],
    ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
    ["DATE"]
]

#Storage for all of the individual records
# IDs are the keys, Individual objects are the values
indi_map = {}

#Storage for all of the family records
# IDs are the keys, Family objects are the values
fam_map = {}

#The current object that's being read. Can be either an Individual or a Family
current_obj = None

#The last seen date tag

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
                fixedLine = line.replace("\n", "") #Remove any newline characters
                fields = fixedLine.split(" ", 2) #Split the line into at most three seperate parts
                numFields = len(fields)
                if(numFields <= 1):
                    raise GEDCOMReadException("Not enough arguments on the line")
                match fields[0] : #The number of the line
                    case "0":
                        secondField = fields[1]
                        if(secondField == "HEAD" or secondField == "TRLR" or secondField == "NOTE"):
                            pass #These tags are simply for annotation, you don't need to record any data for them
                        elif(numFields == 2):
                            raise GEDCOMReadException("Not enough fields for valid INDI or FAM")
                        elif(fields[2] == "INDI"):
                            current_obj = Individual(secondField)
                        elif(fields[2] == "FAM"):
                            current_obj = Family(secondField)
                        else:
                            raise GEDCOMReadException("Invalid tags for 0-numbered line")
                    case "1":
                        pass
                    case "2":
                        if(fields[1] != "DATE"):
                            raise GEDCOMReadException("Invalid tags for 2-numbered line")
                        if(numFields == 2):
                            raise GEDCOMReadException("Not enough fields for DATE")
                        lineDate = stringToDate(fields[2])
                        #TODO: Finish this
                        pass
                    case _: #Since all lines are assumed to be syntatically correct, this technically isn't needed
                        raise GEDCOMReadException("Line number is not valid (0, 1, 2)")
            except GEDCOMReadException as e:
                print("Error reading line: " + e.message)
except OSError as e:
    print("OS Error encountered: " + os.strerror(e.errno))
except Exception as e:
    print("Error encountered: " + os.strerror(e.errno))
