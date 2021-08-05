# pytest-bdd-101
pytest-bdd basics

## Preparation

### Prepare Environment

```bash
$ py -m venv .venv
$ source .venv/Scripts/activate
$ pip install pytest pytest-bdd
...
Successfully installed Mako-1.1.4 MarkupSafe-2.0.1 atomicwrites-1.4.0 attrs-21.2.0 colorama-0.4.4 glob2-0.7 iniconfig-1.1.1 packaging-21.0 parse-1.19.0 parse-type-0.5.2 pluggy-0.13.1 py-1.10.0 pyparsing-2.4.7 pytest-6.2.4 pytest-bdd-4.1.0 six-1.16.0 toml-0.10.2
```

### Project Structure

```
[project root directory]
|‐‐ src
|   `-- [product code packages]
|-- tests
|   |-- features
|   |   `-- *.feature
|   |-- step_defs
|   |   |-- __init__.py
|   |   |-- conftest.py
|   |   `-- test_*.py
|   `-- webdriver
|       |-- chromedriver.92
|           `-- chromedriver.exe
`-- [pytest.ini|tox.ini|setup.cfg]
```



### Install Selenium 

```bash
$ pip install -U selenium
...
```

#### Windows

Download Chromedriver package (find the binding link at https://pypi.org/project/selenium/)

Extract under `<project-root-dir>/tests/webdriver/chromedriver.92` directory.

See also:

* [How to install Selenium in Python](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/) - Geckodriver
* [Selenium with Python: Tutorial on Test Automation](https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test) - Chrome

#### Verify Selenium Installation

Start Python from the project root directory:

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./tests/webdriver/chromedriver.92/chromedriver.exe')
driver.get("https://www.python.org")
print(driver.title)
driver.close()
```

## Create Tests

### Create feature file

 `tests/features/web.feature`:

```gherkin
@web @duckduckgo
Feature: DuckDuckGo Web Browsing
  As a web surfer,
  I want to find information online,
  So I can learn new things and get tasks done.

  # The "@" annotations are tags
  # One feature can have multiple scenarios
  # The lines immediately after the feature title are just comments

  Scenario: Basic DuckDuckGo Search
    Given the DuckDuckGo home page is displayed
    When the user searches for "panda"
    Then results are shown for "panda"
```

### Create `tests/conftest.py`

Add the fixture(s):

```python
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

```



### Create steps file

 `tests/step_defs/test_unit_web.py`:

```python
from .conftest import BASE_DIR, DUCKDUCKGO_HOME
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.keys import Keys


# Scenarios
 
scenarios(BASE_DIR / 'features/web.feature')
 
# Given Steps
 
@given('the DuckDuckGo home page is displayed')
def ddg_home(browser):
    browser.get(DUCKDUCKGO_HOME)

# When Steps
 
@when(parsers.parse('the user searches for "{phrase}"'))
def search_phrase(browser, phrase):
    search_input = browser.find_element_by_id('search_form_input_homepage')
    search_input.send_keys(phrase + Keys.RETURN)
 
# Then Steps
 
@then(parsers.parse('results are shown for "{phrase}"'))
def search_results(browser, phrase):
    # Check search result list
    # (A more comprehensive test would check results for matching phrases)
    # (Check the list before the search phrase for correct implicit waiting)
    links_div = browser.find_element_by_id('links')
    assert len(links_div.find_elements_by_xpath('//div')) > 0
    # Check search phrase
    search_input = browser.find_element_by_id('search_form_input')
    assert search_input.get_attribute('value') == phrase

```

### Update `pytest.ini`

```ini
[pytest]
markers =
    duckduckgo
    web
```

### Run tests

```bash
$ pytest -vv
========================= test session starts ==========================
platform win32 -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- c:\sandbox\learn\python\pytest-bdd\.venv39\scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Sandbox\Learn\Python\pytest-bdd\pytest-bdd-101, configfile: pytest.ini
plugins: bdd-4.1.0
collected 1 item

tests/step_defs/test_duckduckgo.py::test_basic_duckduckgo_search <- ..\.venv39\lib\site-packages\pytest_bdd\scenario.py
DevTools listening on ws://127.0.0.1:49679/devtools/browser/f96798f3-e989-4b2b-ae6f-0a340f77ee5f
PASSED [100%]

========================== 1 passed in 5.71s =========================== 

```



## Visual Studio Code Plugins

* https://marketplace.visualstudio.com/items?itemName=alexkrechik.cucumberautocomplete
  * Snippets in `.feature` files





## See Also

* [Python Testing 101: Pytest-bdd](https://automationpanda.com/2018/10/22/python-testing-101-pytest-bdd/)
* [Python Testing 101: Behave](https://automationpanda.com/2018/05/11/python-testing-101-behave/)
* Automation Panda BDD: https://automationpanda.com/bdd/

