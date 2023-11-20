import unittest

#Unit Test Classes
from tests.US01_Tests import US01_Tests as us01
from tests.US02_Tests import US02_Tests as us02
from tests.US03_Tests import US03_Tests as us03
from tests.US04_Tests import US04_Tests as us04
from tests.US05_Tests import US05_Tests as us05 
from tests.US06_Tests import US06_Tests as us06
from tests.US07_Tests import US07_Tests as us07
from tests.US08_Tests import US08_Tests as us08
from tests.US09_Tests import US09_Tests as us09
from tests.US10_Tests import US10_Tests as us10
from tests.US11_Tests import US11_Tests as us11
from tests.US12_Tests import US12_Tests as us12
from tests.US14_Tests import US14_Tests as us14
from tests.US15_Tests import TestFewerThan15Siblings as us15
from tests.US16_Tests import US16_Tests as us16
from tests.US17_Tests import TestNoMarriageToDescendants as us17
from tests.US18_Tests import TestNoSiblingMarriage as us18
from tests.US19_Tests import US19_Tests as us19
from tests.US21_Tests import TestCheckCorrectGenderForRoles as us21
from tests.US22_Tests import US22_Tests as us22
from tests.US23_Tests import TestCheckUniqueNamesAndBirthDates as us23
from tests.US25_Tests import US25_Tests as us25
from tests.US26_Tests import US26_Tests as us26
from tests.US28_Tests import US28_Tests as us28
from tests.US30_Tests import US30_Tests as us30
from tests.US31_Tests import US31_Tests as us31
from tests.US35_Tests import TestRecentBirths as us35
from tests.US36_Tests import TestRecentDeaths as us36
from tests.US38_Tests import TestUpcomingBirthdaysSorting as us38
from tests.US42_Tests import US42_Tests as us42

#Index of the array is the number of the corresponding user story minus 1
#Fill this out as test case files are written
testCaseClassArray = [us01, us02, us03, us04, us05, us06, us07, us08, us09, us10, 
                      us11, us12, None, us14, us15, us16, us17, us18, us19, None, 
                      us21, us22, us23, None, us25, us26, None, us28, None, us30,
                      us31, None, None, None, us35, us36, None, us38, None, None,
                      None, us42]

def printTestCases(usNum: int):
    if(usNum < 1 or usNum > 42):
        raise ValueError("Number provided not between 1 and 42")
    testCaseClass = testCaseClassArray[usNum - 1]
    if(testCaseClass is None):
        raise Exception("Test cases for US" + str(usNum) + " yet to be implemented.")
    cases = unittest.TestLoader().loadTestsFromTestCase(testCaseClass)
    print("\n[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]")
    unittest.TextTestRunner(verbosity=2).run(cases)
    print("[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]\n")

while(True):
    testCaseVal: str = input("Which set of test cases do you want to run (Provide a number from 1-42, write ALL to run all 42 test suites, write EXIT to exit the program)? ")
    try:
        fixedVal: str = testCaseVal.strip().upper()
        if(fixedVal == "EXIT"):
            print("Goodbye")
            break
        elif(fixedVal == "ALL"):
            for num in range(len(testCaseClassArray)):
                try:
                    printTestCases(num+1)
                except Exception as e:
                    print(e)
            print()
        else:
            testCaseNum = int(testCaseVal)
            printTestCases(testCaseNum)
    except Exception as e:
        print(e)
