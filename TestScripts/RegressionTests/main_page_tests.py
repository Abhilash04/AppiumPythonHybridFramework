""" This module contains the all test cases."""
import logging
import unittest
import pytest
import allure
import sys
import string
import random
import FrameworkUtilities.logger_utility as log_utils
from PageObjects.MainPage.main_page import MainPage
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.config_utility import ConfigUtility


@allure.story('[DEMO] - Automate  the  main screen functionality')
@allure.feature('Web App Main Screen Tests')
@pytest.mark.usefixtures("get_driver")
class MainPageTests(unittest.TestCase):
    """
    This class contains the executable test cases.
    """

    data_reader = DataReader()
    config = ConfigUtility()
    log = log_utils.custom_logger(logging.INFO)

    def setUp(self):
        self.main_page = MainPage(self.driver)
        self.exe_status = ExecutionStatus(self.driver)
        self.prop = self.config.load_properties_file()

    def tearDown(self):
        pass
        # self.login_page.logout_from_app()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, request):
        """
        This method is used for one time setup of test execution process.
        :return: it returns nothing
        """

        if self.data_reader.get_data(request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @allure.testcase("Verify Main Screen Elements")
    def test_verify_main_screen_elements(self):
        """
        This test is validating the presence of main screen elements.
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name

        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        with allure.step("Verify Presence of Main Screen Elements Successful"):
            result = self.main_page.verify_main_screen_elements()
            self.exe_status.mark_final(test_step="Verify Presence of Main Screen Elements Successful", result=result)

    def test_verify_supertackle_reset(self):
        """
        This test is validating the presence of main screen elements.
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name

        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        with allure.step("Verify Super Tackle Functionality"):
            result_1 = self.main_page.verify_super_tackle_functionality(
                self.data_reader.get_data(test_name, "MovePoint"))
            self.exe_status.mark(test_step="Verify Super Tackle Functionality", result=result_1)

        with allure.step("Verify Reset Button Functionality"):
            result = self.main_page.verify_reset_button_functionality()
            self.exe_status.mark_final(test_step="Verify Reset Button Functionality", result=result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
