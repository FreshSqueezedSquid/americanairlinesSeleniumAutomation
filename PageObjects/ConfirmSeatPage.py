from selenium.webdriver.common.by import By

class ConfirmSeat:

    def __init__(self, driver):
        self.driver = driver

    skip_seating = (By.CSS_SELECTOR, "#continueWithoutSeatsLink")

    def skipSeating(self):
        return self.driver.find_element(*ConfirmSeat.skip_seating)