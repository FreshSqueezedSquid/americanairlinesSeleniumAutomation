from selenium.webdriver.common.by import By



class SelectFlight:

    def __init__(self, driver):
        self.driver = driver

    lowest_depart_fare = (By.XPATH, "(//button[@id='slice0Flight1MainCabin'])[1]")
    lowest_return_fare = (By.XPATH, "(//button[@id='slice1Flight1MainCabin'])[1]")
    close_popup = (By.CSS_SELECTOR, ".icon-close.icon-medium")
    status_pref = (By.CSS_SELECTOR, "#mainCabinUpsellDialogClose")
    guest_login = (By.CSS_SELECTOR, "#continue-as-guest-btn")

    def lowestDepartPrice(self):
        return self.driver.find_element(*SelectFlight.lowest_depart_fare)

    def lowestReturnPrice(self):
        return self.driver.find_element(*SelectFlight.lowest_return_fare)

    def closePopUp(self):
        return self.driver.find_element(*SelectFlight.close_popup)

    def statusPref(self):
        return self.driver.find_element(*SelectFlight.status_pref)

    def guestLogin(self):
        return self.driver.find_element(*SelectFlight.guest_login)
