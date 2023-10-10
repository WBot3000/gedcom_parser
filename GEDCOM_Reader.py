#Walker Bove, Sindhu Buggana, Sri Laya Nalmelwar, Hindu Kotha
#Assignment 3: GEDCOM Reader

import os
from datetime import date

from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family, GEDCOMReadException
from classes.GEDCOM_Reporting import Report

#Stores all report data
report: Report = Report()

#The current object that's being read. Can be either an Individual or a Family
current_obj: GEDCOMUnit = None

#The last seen tag that correpsonds to a date (BIRT, DEAT, MARR, DIV). Used to determine what field to fill in
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
                                report.addToReport(current_obj) #Add current object to the map before you start with the new Individual
                                fixedId: str = report.generate_unique_id(secondField) #Checks for duplicate IDs, #US22
                                current_obj = Individual(fixedId)
                            elif(fields[2] == "FAM"):
                                report.addToReport(current_obj) #Add current object to the map before you start with the new Family
                                fixedId: str = report.generate_unique_id(secondField)
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
                        dateObj: date = report.getDateFromString(fields[2]) #US42
                        report.check_for_future_dates(dateObj) #US01
                        current_obj.setDate(dateObj, readingDateOf)
                        readingDateOf = None
                        pass
                    case _: #Since all lines are assumed to be syntatically correct, this technically isn't needed
                        raise GEDCOMReadException("Line number is not valid (0, 1, 2)")
            except Exception as e:
                print("Error reading line: " + e.message)

        report.addToReport(current_obj) #Add the latest object into the maps
        print("Done reading in data")
except OSError as e:
    print("OS Error encountered: " + os.strerror(e.errno))
except Exception as e:
    print("Error encountered: " + os.strerror(e.errno))

#Checks
report.birth_before_marriage() #US02
report.birth_before_death() #US03
report.marriage_before_divorce() #US04
report.marriage_before_death() #US05
report.divorce_before_death() #US06
report.check_max_age() #US07
report.marriage_after_14() #US10
report.check_multiple_births() #US14
report.fewer_than_15_siblings() #US15
report.check_correct_gender_for_roles() #US21
report.check_unique_name_and_birth_date() #US23
report.sort_children_by_age() #US28

#Printing the report
report.printReport()
