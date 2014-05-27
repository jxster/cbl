import logging
from bs4 import BeautifulSoup
from selenium import webdriver


def before_all(context):
    selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.WARN)
    context.browser = webdriver.Firefox()
    context.testserver = 'http://localhost:5000'

    def parse_soup():
        """Use BeautifulSoup to parse the current response and return the DOM tree.
        """
        html = context.browser.page_source
        return BeautifulSoup(html)

    context.parse_soup = parse_soup

def after_all(context):
    context.browser.quit()