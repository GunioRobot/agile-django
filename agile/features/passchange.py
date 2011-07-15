# -*- coding: utf-8 -*-

from lettuce import step, world
from sure import that

@step(u'see the password form')
def see_the_password_form(step):
    old = step.given(u'see the form field "old_password"')
    new1 = step.given(u'see the form field "new_password1"')
    new2 = step.given(u'see the form field "new_password2"')
    assert old and new1 and new2, 'This is not the password change form'

@step(u'see the "(.+)" page')
def see_the_requested_page(step, page):
    assert that(world.browser.title).equals('%s - AgileDjango' % page), \
        'This is not the %s page' % page

@step(u'submit the "(.+)" form')
def submit_the_password_form(step, parent_id):
    form = world.browser.find_by_css_selector("#%s form input[type=submit]" % \
                                              parent_id)
    assert form, "no submit inputs for %s form does not exist in this page" % \
        parent_id
    form[0].click()