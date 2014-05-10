import logging
from selenium import webdriver


def before_all(context):
    selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.WARN)
    context.browser = webdriver.Firefox()
    context.testserver = 'http://localhost:8000'

def after_all(context):
    context.browser.quit()