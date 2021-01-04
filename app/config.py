import os


CHROME_PATH = os.getenv('CHROME_PATH', 'chromedriver')
USE_CHROME_HEADLESS = os.getenv('USE_CHROME_HEADLESS', '1') == '1'
MZ_LOGIN_USERNAME = os.getenv('MZ_LOGIN_USERNAME', '')
MZ_LOGIN_PASSWORD = os.getenv('MZ_LOGIN_PASSWORD', '')

MZ_DOMAIN = 'https://www.managerzone.com'