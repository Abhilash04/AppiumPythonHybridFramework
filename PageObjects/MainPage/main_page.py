"""This module is used for main page objects."""

import logging
from SupportLibraries.base_helpers import BaseHelpers
import FrameworkUtilities.logger_utility as log_utils


class MainPage(BaseHelpers):
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    team_A_super_tackle = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_STackle']"
    team_B_super_tackle = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_STackle_b']"
    team_A_do_or_die_raid = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_DRaid']"
    team_B_do_or_die_raid = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_DRaid']"
    team_A_touch = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Touch']"
    team_B_touch = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Touch_b']"
    team_A_all_out = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_AllOut']"
    team_B_all_out = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_AllOut_b']"
    team_A_bonus = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Bonus']"
    team_B_bonus = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Bonus_b']"
    team_A_tackle = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Tackle']"
    team_B_tackle = "//android.widget.Button[@resource-id='com.example.android.prokabaddi:id/button_Tackle_b']"
    reset_button = "//android.widget.Button[@text='RESET']"
    team_A_score_view = "//android.widget.TextView[@resource-id='com.example.android.prokabaddi:id/team_a_score']"
    team_B_score_view = "//android.widget.TextView[@resource-id='com.example.android.prokabaddi:id/team_b_score']"

    def verify_main_screen_elements(self):
        """
        This function is used to verify all the elements present on the main screen
        :return: this function returns boolean status of element located
        """
        result = False
        _xpath_prop = "xpath"

        locator_dict = {
            self.team_A_super_tackle: _xpath_prop,
            self.team_B_super_tackle: _xpath_prop,
            self.team_A_do_or_die_raid: _xpath_prop,
            self.team_B_do_or_die_raid: _xpath_prop,
            self.team_A_touch: _xpath_prop,
            self.team_B_touch: _xpath_prop,
            self.team_A_all_out: _xpath_prop,
            self.team_B_all_out: _xpath_prop,
            self.team_A_bonus: _xpath_prop,
            self.team_B_bonus: _xpath_prop,
            self.team_A_tackle: _xpath_prop,
            self.team_B_tackle: _xpath_prop,
            self.reset_button: _xpath_prop,
            self.team_A_score_view: _xpath_prop,
            self.team_B_score_view: _xpath_prop
        }

        result = self.verify_elements_located(locator_dict)

        if not result:
            self.log.error("Main screen element verification failed.")

        return result

    def verify_super_tackle_functionality(self, move_point):
        """
        This function is used to verify super tackle functionality.
        :return: this function returns boolean status for super tackle functionality.
        """
        result = True

        self.mouse_click_action(self.team_A_super_tackle)
        self.wait_for_sync(1)
        actual_point = self.get_text_from_element(self.team_A_score_view)

        if not self.verify_text_match(actual_point, str(move_point)):
            self.log.error("Super tackle move point is not correct.")
            result = False

        return result

    def verify_reset_button_functionality(self):
        """
        This function is used to verify reset functionality.
        :return: this function returns boolean status for reset functionality.
        """
        result = True

        self.mouse_click_action(self.reset_button)
        self.wait_for_sync(1)
        actual_score_value = self.get_text_from_element(self.team_A_score_view)

        if not self.verify_text_match(actual_score_value, "0"):
            self.log.error("Reset button functionality is not working.")
            result = False

        return result
