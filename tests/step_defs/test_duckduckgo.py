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
