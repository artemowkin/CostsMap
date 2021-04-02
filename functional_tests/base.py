import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.urls import reverse


class FunctionalTest(LiveServerTestCase):
    """Base class for functional tests"""

    def setUp(self):
        self.browser = webdriver.Firefox()

        # Sign Up
        self.browser.get(self.live_server_url + reverse('account_signup'))
        form_email = self.browser.find_element_by_name('email')
        form_password = self.browser.find_element_by_name('password1')
        form_email.send_keys('testuser@gmail.com')
        form_password.send_keys('testpass123')
        form_password.send_keys(Keys.ENTER)
        time.sleep(2)

    def tearDown(self):
        self.browser.close()
