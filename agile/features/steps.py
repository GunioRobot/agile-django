# -*- coding: utf-8 -*-
from lettuce import step, world
from sure import that

@step(u'I am in the login page')
def i_am_in_the_login_page(step):
    step.given('click on the link "Login"')

@step(u'see the logged in homepage')
def see_the_logged_in_homepage(step):
    step.behave_as('''
    I see the link "Home"
    I see the link "Projects"
    I see the link "Profile"
    I see the link "Logout"
    ''')

@step(u'I am logged in')
def i_am_logged_in(step):
    step.behave_as('''
    Given I am in the login page
    And I fill the form with the next info:
      | name     | value |
      | username | admin |
      | password | admin |
    Then I submit the form
    ''')

@step('I see the link "(.+)"')
def see_the_link(step, text):
    found = world.browser.find_link_by_text(text)
    assert found, 'no links with the text "%s" were found' % text
    
@step('I don\'t see the link "(.+)"')
def dont_see_the_link(step, text):
    found = world.browser.find_link_by_text(text)
    assert not found, 'links with the text "%s" were found' % text

@step(u'see the page for (.+) seconds')
def see_the_page_for_n_seconds(step, n):
    import time
    time.sleep(float(n))
    
@step(u'fill the form with the next info:')
def fill_the_form_with_the_next_info(step):
    form_data = step.hashes
    for data in form_data:
        name = data['name']
        value = data['value']
        is_input = world.browser.find_by_css_selector('input[name=%s]' % name)
        if is_input:
            if value:
                is_input.first.value = value
            continue
        
        is_select = world.browser.find_by_css_selector('select[name=%s]' % name)
        if is_select:
            world.browser.select(name, value)
            continue

@step(u'click on the link "(.*)"')
def click_on_the_link(step, text):
    found = world.browser.find_link_by_text(text)
    assert found, 'no links with the text "%s" were found' % text
    found.first.click()

@step(u'submit the form')
def submit_the_form(step):
    submitter = world.browser.find_by_css_selector("form input[type='submit']")
    assert submitter, 'no form submit inputs were found'
    submitter[0].click()