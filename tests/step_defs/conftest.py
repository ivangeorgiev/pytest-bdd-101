from pathlib import Path
import pytest
from selenium import webdriver

# Constants

BASE_DIR = Path(__file__).parent.parent
DUCKDUCKGO_HOME = 'https://duckduckgo.com/'

# Fixtures

@pytest.fixture
def browser():
    driver_path = BASE_DIR / 'webdriver/chromedriver.92/chromedriver.exe'
    b = webdriver.Chrome(driver_path)
    b.implicitly_wait(10)
    yield b
    b.quit()
 