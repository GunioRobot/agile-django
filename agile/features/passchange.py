# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2011
@author: orozco
'''
from lettuce import step, world
from sure import that

#passchange.feature

@step(u'see the password form')
def see_the_password_form(step):
    old = step.given(u'see the form field "old_password"')
    new1 = step.given(u'see the form field "new_password1"')
    new2 = step.given(u'see the form field "new_password2"')
    assert old and new1 and new2, 'This is not the password change form'

@step(u'see the "(.+)" page')
def see_the_requested_page(step, page):
    
    assert that(world.browser.title).equals('Profile - AgileDjango'), 'This is not the Profile page'
    step.then('see the form field "first_name"')
    step.then('see the form field "last_name"')
    step.then('see the form field "email"')

@step(u'submit the "(.+)" form')
def submit_the_password_form(step, parent_id):
    form = world.browser.find_by_css_selector("#%s form input[type=submit]" % \
                                              parent_id)
    assert form, "no submit inputs for %s form does not exist in this page" % \
        parent_id
    form[0].click()