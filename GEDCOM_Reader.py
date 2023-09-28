#Walker Bove, Sindhu Buggana, Sri Laya Nalmelwar, Hindu Kotha
#Assignment 3: GEDCOM Reader

import os
from datetime import date

from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family, GEDCOMReadException
from classes.GEDCOM_Reporting import Report

report: Report = Report()
#Storage for all of the individual records
# IDs are the keys, Individual objects are the values
#indi_map: dict[str, Individual] = {}

#Storage for all of the family records
# IDs are the keys, Family objects are the values
#fam_map: dict[str, Family] = {}



#Used to add the current object to either the Individual or Family maps
#def addToMap(unit: GEDCOMUnit) -> None:
#    if(unit is None):
#        pass
#    elif(isinstance(unit, Individual)):
#        indi_map.update({unit.id: unit})
#    elif(isinstance(unit, Family)):
#        fam_map.update({unit.id: unit})
#    else:
#        raise GEDCOMReadException("Attempting to add non-GEDCOMUnit object to either the Individual or Family maps")

#The current object that's being read. Can be either an Individual or a Family
current_obj: GEDCOMUnit = None

#The last seen date tag. Used to determine what field to fill in
readingDateOf: str = None



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
                                report.addToMap(current_obj) #Add current object to the map before you start with the new Individual
                                fixedId: str = report.generateId(secondField) #Checks for duplicate IDs
                                current_obj = Individual(fixedId)
                            elif(fields[2] == "FAM"):
                                report.addToMap(current_obj) #Add current object to the map before you start with the new Family
                                fixedId: str = report.generateId(secondField)
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
                        dateObj: date = report.getDateFromString(fields[2])
                        current_obj.setDate(dateObj, readingDateOf)
                        readingDateOf = None
                        pass
                    case _: #Since all lines are assumed to be syntatically correct, this technically isn't needed
                        raise GEDCOMReadException("Line number is not valid (0, 1, 2)")
            except Exception as e:
                print("Error reading line: " + e.message)

        report.addToMap(current_obj) #Add the latest object into the maps
        print("Done reading in data")
except OSError as e:
    print("OS Error encountered: " + os.strerror(e.errno))
except Exception as e:
    print("Error encountered: " + os.strerror(e.errno))

report.printReport()