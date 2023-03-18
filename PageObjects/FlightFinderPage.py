from selenium.webdriver.common.by import By

from PageObjects.SelectFlightPage import SelectFlight


class FlightFinder:

    def __init__(self, driver):
        self.driver = driver

    cookie_warning = (By.XPATH, "//button[@name='closeBannerButton']")
    destination = (By.XPATH, "//input[@id='reservationFlightSearchForm.destinationAirport']")
    depart_date = (By.XPATH, "//input[@id='aa-leavingOn']")
    return_date = (By.XPATH, "//input[@id='aa-returningFrom']")
    search_button = (By.XPATH, "//input[@id='flightSearchForm.button.reSubmit']")

    def cookieWarning(self):
        return self.driver.find_element(*FlightFinder.cookie_warning)

    def getDestination(self):
        return self.driver.find_element(*FlightFinder.destination)

    def departDate(self):
        return self.driver.find_element(*FlightFinder.depart_date)

    def returnDate(self):
        return self.driver.find_element(*FlightFinder.return_date)

    def selectFlight(self):
        self.driver.find_element(*FlightFinder.search_button).click()
        selectFlightPage = SelectFlight(self.driver)
        return selectFlightPage

