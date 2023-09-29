import unittest

#Unit Test Classes
from tests.US22_Tests import US22_Tests as us22

#Index of the array is the number of the corresponding user story minus 1
#Fill this out as test case files are written
testCaseClassArray = [None, None, None, None, None, None, None, None, None, None, 
                      None, None, None, None, None, None, None, None, None, None, 
                      None, us22, None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None, None, None,
                      None, None]

while(True):
    testCaseVal: str = input("Which set of test cases do you want to run (Provide a number from 1-42, write EXIT to exit the program)? ")
    try:
        if(testCaseVal.strip().upper() == "EXIT"):
            print("Goodbye")
            break
        testCaseNum = int(testCaseVal)
        if(testCaseNum < 1 or testCaseNum > 42):
            raise ValueError("Number provided not between 1 and 42")
        testCaseClass = testCaseClassArray[testCaseNum - 1]
        if(testCaseClass is None):
            raise Exception("Test cases for US" + str(testCaseNum) + " yet to be implemented.")
        cases = unittest.TestLoader().loadTestsFromTestCase(testCaseClass)
        print("\n[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]")
        unittest.TextTestRunner(verbosity=2).run(cases)
        print("[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]\n")
    except Exception as e:
        print(e)
