#Walker Bove, Sindhu Buggana, Sri Laya Nalmelwar, Hindu Kotha
#Assignment 3: GEDCOM Reader

import os
from datetime import date

from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family, GEDCOMReadException
from classes.GEDCOM_Reporting import Report

#Tags that indicate annotation. They exist to aid the reader of the file, not to add new content, so they can be skipped over
annotationTags: list[str] = ["HEAD", "TRLR", "NOTE"]

#Tags that indicate types of date values. Indicate what the date that's about to be read is meant for
dateTags: list[str] = ["BIRT", "DEAT", "MARR", "DIV"]

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
                        if(secondField in annotationTags):
                            pass #These tags are simply for annotation, you don't need to record any data for them
                        elif(numFields == 3):
                            if(fields[2] == "INDI"):
                                report.addToReport(current_obj) #Add current object to the map before you start with the new Individual
                                fixedId: str = report.check_unique_id_and_fix(secondField) #Checks for duplicate IDs, #US22
                                current_obj = Individual(fixedId)
                            elif(fields[2] == "FAM"):
                                report.addToReport(current_obj) #Add current object to the map before you start with the new Family
                                fixedId: str = report.check_unique_id_and_fix(secondField)
                                current_obj = Family(fixedId)
                            else:
                                raise GEDCOMReadException("Invalid tag for 0-numbered line")
                        else:
                            raise GEDCOMReadException("Invalid tag for 0-numbered line")
                    case "1":
                        #Check to make sure object exists, then check if line is specifying a type of date or just a standard field
                        if(current_obj is None):
                            raise GEDCOMReadException("No GEDCOM Unit (Individual or Family) to give field")
                        elif(secondField in dateTags):
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
else:
    #Checks
    report.check_corresponding_entries() #US26, felt like it fit more at the beginning despite being the 26th story
    report.birth_before_marriage() #US02
    report.birth_before_death() #US03
    report.marriage_before_divorce() #US04
    report.marriage_before_death() #US05
    report.divorce_before_death() #US06
    report.check_max_age() #US07
    report.check_birth_after_parents_marriage() #US08
    report.check_birth_before_death_parents() #US09
    report.marriage_after_14() #US10
    report.check_bigamy() #US11
    report.check_parent_child_age_difference() #US12
    report.check_multiple_births() #US14
    report.fewer_than_15_siblings() #US15
    report.check_family_male_surnames() #US16
    report.no_marriage_to_descendants() #US17
    report.no_sibling_marriage() #US18
    report.first_cousins_should_not_marry() #US19
    report.check_correct_gender_for_roles() #US21
    report.check_unique_name_and_birth_date() #US23
    report.check_sibling_same_name() #US25
    report.sort_children_by_age() #US28
    report.list_couples_with_large_age_difference() #US34
    report.list_recent_births() #US35 
    report.list_recent_deaths() #US36
    report.list_upcoming_birthdays() #US38
    report.list_upcoming_anniversaries() #US39
    report.printReport()

