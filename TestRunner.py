import unittest

#Unit Test Classes
from tests.US01_Tests import US01_Tests as us01
from tests.US02_Tests import US02_Tests as us02
from tests.US03_Tests import US03_Tests as us03
from tests.US22_Tests import US22_Tests as us22
from tests.US42_Tests import US42_Tests as us42

#Index of the array is the number of the corresponding user story minus 1
#Fill this out as test case files are written
testCaseClassArray = [us01, us02, us03, None, None, None, None, None, None, None, 
                      None, None, None, None, None, None, None, None, None, None, 
                      None, us22, None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None, None, None,
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
