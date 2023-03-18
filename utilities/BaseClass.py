import inspect
import logging
import time
import pyautogui
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup")
class BaseClass:

    # Scrolls page down incrementally so that we can view all inputs
    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, 300);")

    # Allows a screenshot to be taken at any point in the booking process to help troubleshoot what is going wrong
    def takeScreenshot(self):
        self.driver.save_screenshot('screenshot.png')

    # Creates a log of testing events
    def getLog(self):
        loggerName = inspect.stack()[1][3]  # Gets the name of the class / method from where this method is called
        logger = logging.getLogger(loggerName)
        # formatter will produce...201-19-02-17 12:40:14,798 : ERROR: <testcasename>: Fatal error in submitting credit card payment on step 4. Cannot continue...using for formatting error logs
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler = logging.FileHandler('logfile.log')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)  # filehandler object
        logger.setLevel(logging.DEBUG)
        return logger


