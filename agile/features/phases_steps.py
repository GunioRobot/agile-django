# -*- coding: utf-8 -*-

from lettuce import step, world
from sure import that
from agile.models import Phase

@step(u'click on a project')
def click_on_a_project(step):
    projects = world.browser.find_by_css("#projects ul li a")
    assert projects, 'There are no projects.'
    projects[0].click()

@step(u'wait for the "(.+)" port')
def wait_for_the_requested_port(step, port):
    found = world.wait_for_many_elements('#%s' % port, 5, 0.5)
    assert found, 'This is not the %s port'

@step(u'see the "(.+)" port')
def see_the_requested_port(step, port):
    port = world.browser.find_by_css("#%s" % port)
    assert port, 'The requested port does not exist in this page.'

@step(u'see the "(.+)" phase form')
def see_the_phase_form(step, form):
    found = world.wait_for_many_elements('#add-phase-dialog', 5, 0.5)
    assert found, 'The %s Form was not found' % form.capitalize()
    name = step.given(u'see the form field "name"')
    description = step.given(u'see the form field "description"')
    strories_limit = step.given(u'see the form field "stories_limit"')

@step(u'see the "(.+)" validation error "(.+)"')
def see_the_validation_error_for_field(step, form, value):
    form = form.lower()
    error = world.browser.find_by_xpath(
        '//div[@id="%s-phase-dialog"]//div[contains(., "%s")]' % (form, value))
    assert error, 'No validation errors as expected'

@step(u'check existence of object with the next info')
def check_existence_of_object_with_the_next_info(step):
    form_data = step.hashes
    kwargs = {}
    for data in form_data:
        name = data['name']
        value = data['value']
        kwargs[name] = value
    assert Phase.objects.get(**kwargs), 'The object was not added'

@step(u'click on the "(.+)" button of phase number (.+)')
def click_on_a_button_of_a_phase(step, button_name, number):
    number = int(number)
    if button_name.lower() == u'edit':
        nth = 1
    elif button_name.lower() == u'delete':
        nth = 2
    else:
        assert False, 'Invalid button for phase'
    world.browser.execute_script('$(".phase-controls").css'
                                 '("visibility","visible")')
    button = world.browser.find_by_css('div.phase button')[nth * number - 1]
    assert button, 'There is no %s button for phase %s' % (button_name, number)
    button.click()

@step(u'fill the "(.+)" form with the next info:')
def fill_a_form_with_the_next_info(step, form):
    form_data = step.hashes
    for data in form_data:
        name = data['name']
        value = data['value']
        is_input = world.browser.find_by_css_selector(
                        '#%s-phase-dialog input[name=%s]' % (form, name))
        if is_input:
            is_input.first.value = value
            continue
        
        is_select = world.browser.find_by_css_selector(
                        '#%s-phase-dialog select[name=%s]' % (form, name))
        if is_select:
            world.browser.select(name, value)
            continue

@step(u'check that the phase has the edited info:')
def check_that_the_phase_has_the_edited_info(step):
    form_data = step.hashes
    for data in form_data:
        name = data['name']
        value = data['value']
        is_input = world.browser.find_by_css('div#"edit-phase-dialog" ' +
                                             'input[name=%s]' % name)
        if is_input:
            assert is_input.first.value == value, \
                '%s has not the expected value'
            continue
        
        is_select = world.browser.find_by_css('select[name=%s]' % name)
        if is_select:
            assert is_select.first.value == value, \
                    '%s has not the expected value'
            continue

@step(u'see a dialog')
def see_a_dialog(step):
    dialog = world.browser.find_by_css('div.confirm')
    assert dialog, 'There is no dialog'
    assert dialog.first.visible, 'The dialog exists, but was not shown'

@step(u'click the "(.+)" button of the dialog')
def click_a_button_of_the_dialog(step, button_name):
    buttons = world.browser.find_by_css('div.confirm ~ div '
                                        'div.ui-dialog-buttonset button')
    if buttons[0].text.lower() == button_name.lower():
        button = buttons[0]
    else:
        button = buttons[1]
    assert button, 'There is no %s button in the dialog' % button
    button.click()

@step(u'see that no error is reported')
def see_that_no_error_is_reported(step):
    error_message = world.browser.find_by_css('#agile-message')
    message_is_hidden = not error_message.first.visible
    assert message_is_hidden, 'An unexpected error was shown'

@step(u'see an error message that says "(.+)"')
def see_an_error_message(step, message):
    error_message = world.browser.find_by_css('#agile-message')
    if not error_message.first.visible:
        assert False, 'The message was not shown'
    assert that(error_message.first.text).equals(message), \
        'The message was not the expected'
    

