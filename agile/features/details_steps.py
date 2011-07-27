import datetime

from lettuce import step, world
from sure import that
from agile.models import Phase

@step(u'see the "(.+)" project form')
def see_the_project_form(step, form):
    found = world.wait_for_element('#add-project', 5, 0.5)
    assert found, 'The %s Project Form was not found' % form.capitalize()

@step(u'select the admin as a member')
def select_admin_as_member(step):
    admin = world.browser.find_by_tag('option')
    assert admin, 'The admin wasn\'t found'
    admin[0].click()

@step(u'click on a link project')
def click_on_a_link_project(step):
    projects = world.wait_for_element("#projects ul li a", 5, 0.5)
    assert projects, 'There are no projects.'
    world.project = world.wait_for_element("div.portlet-header a", 5, 0.5).value
    projects.click()

@step(u'see the board of stories')
def see_the_board_of_stories(step):
    found = world.wait_for_many_elements('.stories, .ui-sortable', 5, 0.5)
    assert found, 'There is no board of stories'

@step(u'display the hidden phases')
def display_the_hidde_phases(step):
    buttons = world.wait_for_many_elements(".left-shows, .right-shows", 5, 0.5)
    assert buttons, 'There are no buttons.'
    buttons[1].click()
    buttons[0].click()

@step(u'see the "(.+)" story form')
def see_the_story_form(step, form):
    found = world.wait_for_many_elements('#add-story-dialog', 5, 0.5)
    assert found, 'The %s Story Form was not found' % form.capitalize()

@step(u'click the menu phase')
def click_the_menu_phase(step):
    phase = world.browser.find_link_by_text('---------')
    assert phase, 'The select menu phase was not found'
    phase[0].click()

@step(u'select the phase')
def select_the_phase(step):
    backlog = world.browser.find_link_by_text("Backlog")
    assert backlog, 'Backlog phase wasn\'t found'
    backlog[0].click()

@step(u'click on a story')
def click_on_a_story(step):
    story = world.wait_for_element("div.story-header a", 5, 0.5)
    assert story, 'There are no stories.'
    world.story = world.wait_for_element("div.story-header a", 5, 0.5).value
    story.click()

@step(u'see the story page')
def see_the_story_page(step):
    assert that(world.browser.title).equals('Story #%s - %s - AgileDjango' %
           (world.story, world.project)), \
        'This is not the story %s page' % world.story

@step(u'click on the time entry')
def click_on_the_time_entry(step):
    time_entry = world.browser.find_link_by_href('#time-entries')
    assert time_entry, 'Could not clicked on time entries'
    time_entry[0].click()

@step(u'click the start button')
def click_the_star_button(step):
    start = world.wait_for_element("#time-entries-start", 5, 0.5)
    assert start, 'There is not the start button'
    cells = world.browser.find_by_css('#table-container td')
    world.len_table = len(cells)
    start.click()

@step(u'see a new row at the table')
def see_a_new_row_at_the_table(step):
    cells2 = world.browser.find_by_css('#table-container td')
    world.len_table2 = len(cells2)
    equal = world.len_table < world.len_table2
    assert equal, 'The current lenght of the table is not greater'

@step(u'click the stop button')
def click_the_stop_button(step):
    world.rows = world.len_table2 / 4
    stop = world.wait_for_element("#time-entries-stop", 5, 0.5)
    assert stop, 'There is not the stop button'
    stop.click()

@step(u'see the right stop and duration time')
def see_the_right_stop_and_duration_time(step):
    stop_cell = world.wait_for_element('#stop-%s' % world.rows, 5, 0.5)
    assert that(stop_cell.text).equals(datetime.datetime.now().strftime("%B %e, %Y,%l:%M %P")), \
        'The stop time is not current'
    duration_cell = world.wait_for_element('#duration-%s' % world.rows, 5, 0.5)
    assert that(duration_cell.text).equals("00:00:03"), \
        'The duration is incorrect'

@step(u'see the message of incorrect')
def see_the_message_of_incorrect(step):
    message = world.wait_for_many_elements('.story-taken-message', 5, 0.5)
    assert message, 'There is not the story taken message'