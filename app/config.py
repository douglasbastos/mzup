import os


CHROME_PATH = os.getenv('CHROME_PATH', 'chromedriver')
USE_CHROME_HEADLESS = os.getenv('USE_CHROME_HEADLESS', '1') == '1'
MZ_LOGIN_USERNAME = os.getenv('MZ_LOGIN_USERNAME', '')
MZ_LOGIN_PASSWORD = os.getenv('MZ_LOGIN_PASSWORD', '')
MZ_TEAM_ID = os.getenv('MZ_TEAM_ID', '')

MZ_DOMAIN = 'https://www.managerzone.com'
MZ_URL_LIST_PLAYERS = f'{MZ_DOMAIN}/ajax.php?p=players&sub=team_players&tid={MZ_TEAM_ID}&sport=soccer'
MZ_URL_TRAINING_HISTORY = f'{MZ_DOMAIN}/ajax.php?p=trainingGraph&sub=getJsonTrainingHistory&sport=soccer&player_id={{}}'
MZ_URL_SCOUT_REPORT = f'{MZ_DOMAIN}/ajax.php?p=players&sub=scout_report&pid={{}}&sport=soccer'
