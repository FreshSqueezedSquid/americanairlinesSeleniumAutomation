import time
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PageObjects.BookFlightPage import BookFlight
from PageObjects.FlightFinderPage import FlightFinder
from TestData.TripData import TripData
from utilities.BaseClass import BaseClass
from selenium.webdriver.support import expected_conditions as EC


class TestAA(BaseClass):

    def test_flightBooking(self, getData):

        log = self.getLog()
        wait = WebDriverWait(self.driver, 45)

        flightFinderPage = FlightFinder(self.driver)
        time.sleep(3)

        # closes cookie warning banner so as not to block any inputs
        try:
            elem = self.driver.find_element(By.XPATH, "//button[@name='closeBannerButton']")
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("Cookie warning encountered and closed")
        except NoSuchElementException:
            log.info("No warning encountered")

        # Entering trip data from getData to search for available flights
        wait.until(EC.element_to_be_clickable(flightFinderPage.getDestination()))
        flightFinderPage.getDestination().send_keys(getData["destination"])
        wait.until(EC.element_to_be_clickable(flightFinderPage.departDate()))
        time.sleep(2)
        flightFinderPage.departDate().send_keys(getData["depart_date"])
        wait.until(EC.element_to_be_clickable(flightFinderPage.returnDate()))
        flightFinderPage.returnDate().send_keys(getData["return_date"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='flightSearchForm.button.reSubmit']")))
        # Switching driver to flight selection page
        selectFlightPage = flightFinderPage.selectFlight()
        time.sleep(3)

        # checks to see if the page is taking extra time to load
        try:
            elem = self.driver.find_element(By.CSS_SELECTOR, "#sec-text-container")
            if elem.is_displayed():
                log.info("Waiting for page to load")
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#aa-search-field")))

        except NoSuchElementException:
            log.info("Page loading normally")

        # closes tool-tip/info pop-up so as not to block available flights to click
        try:
            elem = self.driver.find_element(By.XPATH, "(//button[@id='closeTooltip'])[1]")
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("Tool-tip encountered and closed")
        except NoSuchElementException:
            log.info("No tool-tip encountered")
        time.sleep(3)

        # AA.com can give 2 different ways of identifying flight choices...this try/except block accounts for that
        try:
            elem = selectFlightPage.lowestDepartPrice()
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("No alt id detected")

        except NoSuchElementException:
            self.driver.find_element(By.CSS_SELECTOR, "#flight0-product1").click()
            log.info("Alt CSS id detected")
        time.sleep(4)

        # scrolls down so cheapest return flight options are visible
        self.scrollDown()

        # AA.com can give 2 different ways of identifying flight choices...this try/except block accounts for that
        try:
            elem = selectFlightPage.lowestReturnPrice()
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("No alt id detected")

        except NoSuchElementException:
            self.driver.find_element(By.CSS_SELECTOR, "#flight0-product0").click()
            log.info("Alt CSS id detected")
        time.sleep(4)

        # closes flight upgrade pop up when it appears after selecting return flight
        try:
            elem = selectFlightPage.statusPref()
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("Closing upgrade offer")

        except NoSuchElementException:
            self.driver.find_element(By.CSS_SELECTOR, ".icon-close").click()
            log.info("Alt close option detected")

        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # checks for alternate tags for the continue button on this page
        try:
            elem = selectFlightPage.guestLogin()
            if elem.is_displayed():
                elem.click()  # this will click the element if it is there
                log.info("Going to guest checkout")

        except NoSuchElementException:
            self.driver.find_element(By.CSS_SELECTOR, "#button_continue_guest").click()
            log.info("Alt guest button detected")

        # Booking flight by entering passenger information
        bookFlight = BookFlight(self.driver)
        self.scrollDown()
        log.info("Entering firstname/lastname")
        bookFlight.firstName().send_keys(getData["firstname"])
        bookFlight.lastName().send_keys(getData["lastname"])
        self.scrollDown()
        log.info("Entering month/day/year")
        bookFlight.monthDropdown().select_by_index(2)  # selects 'February'
        bookFlight.dayDropdown().select_by_index(28)   # selects '28'
        bookFlight.yearDropdown().select_by_index(32)  # selects '1992'
        time.sleep(2)
        log.info("Entering gender")
        bookFlight.genderDropdown().select_by_index(1) # selects 'Male'
        log.info("Entering Country/State")
        bookFlight.regionDropdown().select_by_index(1) # selects 'US'
        wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='passengers0.residencyInfo.state']")))
        time.sleep(2.5)
        bookFlight.stateDropdown().select_by_index(3)  # selects 'Arizona'

        self.scrollDown()
        wait.until(EC.element_to_be_clickable(bookFlight.getEmail()))

        # Entering email/phone number
        bookFlight.getEmail().send_keys(getData["email"])
        bookFlight.confEmail().send_keys(getData["email"])
        bookFlight.codeDropdown().select_by_index(1)  # selects 'United States +1'
        bookFlight.phoneNum().send_keys(getData["phone_num"])

        self.scrollDown()
        time.sleep(1)

        # Changes driver to seat confirmation page
        confirmSeat = bookFlight.passengerButton()

        time.sleep(2)
        wait.until(EC.element_to_be_clickable(confirmSeat.skipSeating()))
        confirmSeat.skipSeating().click()
        self.takeScreenshot()



    @pytest.fixture(params=TripData.test_trip_data)
    def getData(self, request):
        return request.param