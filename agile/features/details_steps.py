import datetime

from lettuce import step, world
from sure import that
from agile.models import Phase

@step(u'click on a link project')
def click_on_a_link_project(step):
    projects = world.browser.find_by_css("#projects ul li a")
    assert projects, 'There are no projects.'
    world.project = world.browser.find_by_css("div.portlet-header a")[0].value
    projects[0].click()

@step(u'see the board of stories')
def see_the_board_of_stories(step):
    found = world.browser.find_by_css('.stories, .ui-sortable')
    assert found, 'There is no board of stories'
    
@step(u'display the hidden phases')
def display_the_hidde_phases(step):
    buttons = world.browser.find_by_css(".left-shows, .right-shows")
    assert buttons, 'There are no buttons.'
    buttons[0].click()
    buttons[1].click()
    
@step(u'click on a story')
def click_on_a_story(step):
    stories = world.browser.find_by_css("div.story-header a")
    assert stories, 'There are no stories.'
    world.story = world.browser.find_by_css("div.story-header a")[0].value
    stories[0].click()
    
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
    start = world.browser.find_by_css("#time-entries-start")
    assert start, 'There is not the start button'
    cells = world.browser.find_by_css('#table-container td')
    world.len_table = len(cells)
    start[0].click()
    
@step(u'see a new row at the table')
def see_a_new_row_at_the_table(step):
    cells2 = world.browser.find_by_css('#table-container td')
    world.len_table2 = len(cells2)
    equal = world.len_table < world.len_table2
    assert equal, 'The current lenght of the table is not greater'

@step(u'click the stop button')
def click_the_stop_button(step):
    world.rows = world.len_table2 / 4
    stop = world.browser.find_by_css("#time-entries-stop")
    assert stop, 'There is not the stop button'
    stop[0].click()
    
@step(u'see the right stop and duration time')
def see_the_right_stop_and_duration_time(step):
    stop_cell = world.browser.find_by_css('#stop-%s' % world.rows)
    assert that(stop_cell.first.text).equals(datetime.datetime.now().strftime("%B %e, %Y,%l:%M %P")), \
        'The stop time is not current'
    duration_cell = world.browser.find_by_css('#duration-%s' % world.rows)
    assert that(duration_cell.first.text).equals("00:00:03"), \
        'The duration is incorrect'
        
@step(u'see the message of incorrect')
def see_the_message_of_incorrect(step):
    message = world.browser.find_by_css('.story-taken-message')
    assert message, 'There is not the story taken message'