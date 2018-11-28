import unittest
from TestScripts.RegressionTests.main_page_tests import MainPageTests

# Get all tests from classes
mainPageTests = unittest.TestLoader().loadTestsFromTestCase(MainPageTests)

# Create a test suite combining all test cases
regressionSuite = unittest.TestSuite()
regressionSuite.addTest(mainPageTests)

smokeSuite = unittest.TestSuite()
smokeSuite.addTest(mainPageTests)

# Test runner
unittest.TextTestRunner(verbosity=2).run(smokeSuite)
