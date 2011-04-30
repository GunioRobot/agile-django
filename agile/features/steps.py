# -*- coding: utf-8 -*-
from lettuce import step, world
from sure import that

# authentication.feature
@step(u'I am in the login page')
def i_am_in_the_login_page(step):
    step.given('click on the link "Login"')

@step(u'see the login form')
def see_the_login_form(step):
    step.then('see the form field "username"')
    step.then('see the form field "password"')

@step(u'see the logged in homepage')
def see_the_logged_in_homepage(step):
    step.then('see the link "Home"')
    step.then('see the link "Projects"')
    step.then('see the link "Profile"')
    step.then('see the link "Logout"')

@step(u'I am logged in')
def i_am_logged_in(step):
    step.given('I am in the login page')
    step.behave_as('''
    And I fill the form with the next info:
      | name     | value |
      | username | admin |
      | password | admin |
    ''')
    step.then('submit the form')
    step.then('see the logged in homepage')

# Common
@step(u'see the form field "(.+)"')
def see_the_form_field(step, field_name):
    found = world.wait_for_many_elements('select[name=%(field_name)s], input[name=%(field_name)s]'.format(field_name=field_name))
    assert found, 'no form fields named "%s" were found' % field_name

@step('see the link "(.+)"')
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
    
    
########################
import re
import time

from lxml import html
#from lettuce import world
from django.template.defaultfilters import slugify
from selenium.common.exceptions import WebDriverException

@world.absorb
def wait_for_condition(finished, timeout=5, interval=0.5, dont_fail=False):
    """polls a callable until it returns True.
    arguments:

      finished - a callable that takes no parameters
      timeout - the timeout in seconds, [defaults to five seconds]
      interval - the interval in seconds, [defaults to half second]
    """

    started = time.time()
    doc = finished.__doc__

    if doc:
        msg = 'timed out waiting for the "{0}"'.format(doc)
    else:
        msg = 'timed out waiting for the condition {0}'.format(finished)

    while not finished():
        time.sleep(interval)
        now = time.time()
        if (now - started) >= timeout:
            if dont_fail:
                break
            else:
                raise AssertionError(msg)

@world.absorb
def wait_for_element(selector, timeout=5, interval=0.5, dont_fail=False):
    try:
        found = world.wait_for_many_elements(selector, timeout, interval)
    except AssertionError:
        if dont_fail:
            return
        raise

    return found[0]

@world.absorb
class wait_for_ajax_to_finish(object):
    def __init__(self, on):
        self.url = slugify(on)
        self.sid = 'selenium-ajax-to-{0}'.format(self.url)

    def __enter__(self):
        div = '<div id="{0}" class="waiting" style="display:none;width:0px;height:0px"></div>'.format(self.sid)
        script = ur'''window.selenium_requests = {};
            jQuery("body").append('%(id)s');
            jQuery.ajaxSetup({
                beforeSend:function(jqXHR, settings){window.selenium_requests[settings.url] = jqXHR;},
                complete:function(jqXHR){
                    jQuery.each(window.selenium_requests, function(index, item){
                        if (item == jqXHR) {
                            jQuery("#%(url)s").removeClass("waiting");
                            jQuery("#%(url)s").addClass("ready");
                        }
                    });
                }
            });''' % dict(id=self.sid, url=self.url)

        world.jquery(script)

    def __exit__(self, type, value, traceback):
        def ajax_ready():
            jscript = 'jQuery("#{0}.ready").length'.format(self.sid)
            evaluated = world.browser.evaluate_script(jscript)
            return int(evaluated) > 0

        world.wait_for_condition(ajax_ready, 10)

@world.absorb
def wait_until_visible(selector, timeout=5, interval=0.5):
    found = world.wait_for_many_elements(selector, timeout, interval)
    def element_become_visible():
        sel = 'jQuery("{0}:visible").length'.format(selector)
        return int(world.browser.evaluate_script(sel)) > 0

    world.wait_for_condition(element_become_visible)

@world.absorb
def wait_until_hidden(selector, timeout=5, interval=0.5):
    found = world.wait_for_many_elements(selector, timeout, interval)
    def element_become_hidden():
        sel = 'jQuery("{0}:visible").length'.format(selector)
        return int(world.browser.evaluate_script(sel)) == 0

    world.wait_for_condition(element_become_hidden)

@world.absorb
def wait_for_many_elements(selector, timeout=5, interval=0.5, for_at_least=1):
    if selector.startswith("//"):
        find_function = lambda x: world.dom.xpath(x)
        selector_type = 'xpath'
    else:
        find_function = lambda x: world.dom.cssselect(x)
        selector_type = 'css'

    def element_is_there():
        raw = world.browser.html.strip()
        if raw.startswith('<?xml'):
            raw = unicode(re.sub(r'[<][?]xml[^>]+[>]', '', raw))

        try:
            world.dom = html.fromstring(raw)
        except WebDriverException:
            return False

        return find_function(selector)

    element_is_there.__doc__ = \
        "element %s to be in the DOM (not necessarily visible)" % selector

    world.wait_for_condition(element_is_there)
    found = find_function(selector)
    assert len(found) >= for_at_least, \
        'could not find {2} occurrence(s) of the {3} selector "{0}" not found within {1} seconds'.format(selector, timeout, for_at_least, selector_type)

    if selector_type == 'xpath':
        return world.browser.find_by_xpath(selector)

    return world.browser.find_by_css_selector(selector)
