from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import unittest


class TwitterTest(unittest.TestCase):


    def setUp(self):
        global driver
        driver = webdriver.Firefox()
        driver.get("https://twitter.com/")


    def login_helper(self):
        emailField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.username.field > #signin-email")))
        passField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.password.flex-table-form > #signin-password")))
        enterButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='submit btn primary-btn flex-table-btn js-submit']")))
        emailField.send_keys("ghdfghdfgbdfgh")
        passField.send_keys("qazwsxedc")
        enterButton.click()


    def test_login(self):
        TwitterTest.login_helper(self)
        self.assertTrue(driver.find_element(By.XPATH, "//a[@id='user-dropdown-toggle']"))


    def test_sendTwit(self):
        TwitterTest.login_helper(self)
        twitTextBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='tweet-box-home-timeline']")))
        twitmessage = time.ctime()
        twitTextBox.send_keys(twitmessage)

        sendTwitButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='btn primary-btn tweet-action tweet-btn js-tweet-btn']")))
        sendTwitButton.click()

        time.sleep(5)
        self.assertEqual(driver.find_element_by_xpath(".//*[contains(@id, 'stream-item-tweet')][1]/div/div[2]/p").text, str(twitmessage))


    def test_follow(self):
        TwitterTest.login_helper(self)
        followButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='small-follow-btn follow-btn btn small follow-button js-recommended-item']")))
        initialFollowCount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='page-container']/div[1]/div[1]/div/div[3]/ul/li[2]/a/span[2]"))).text
        followButton.click()
        driver.refresh()
        newFollowCount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='page-container']/div[1]/div[1]/div/div[3]/ul/li[2]/a/span[2]"))).text
        self.assertEqual(str(int(initialFollowCount) + 1), newFollowCount)

    def test_login_neg(self):
        enterButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='submit btn primary-btn flex-table-btn js-submit']")))
        enterButton.click()

        error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='message-drawer']/div/div/span")))
        self.assertTrue(error_message)



    def tearDown(self):
        driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TwitterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
