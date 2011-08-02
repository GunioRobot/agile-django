# -*- coding: utf-8 -*-

from lettuce import step, world
from sure import that
from agile.models import Tag
import time

@step(u'opened a story')
def opened_a_story(step):
    step.then('I am logged in')
    step.then('see the logged in home page')
    step.then('click on the link "Projects"')
    step.then('click on a project')
    stories = world.wait_for_many_elements('.story a', 5, 0.5)
    world.browser.visit('http://localhost:8000/project/1/story/4')
    tags = world.wait_for_many_elements('#tags', 5, 0.5)
    assert tags, 'This is not the story details'

@step(u'add a new tag with the name "(.+)"')
def add_a_new_tag(step, tag_name):
    selector = '#new-tag'
    input = world.wait_for_element(selector, 5, 0.5)
    assert input, 'The input for a new tag is not present.'
    input.value = tag_name
    world.browser.execute_script('$("%s").focusout();' % selector)

@step(u'see the tag named "(.+)"')
def see_a_tag_with_name(step, tag_name):
    selector = '//span[@class="tag-name" and contains(., "%s")]' % tag_name
    tag = world.wait_for_element(selector, 5, 0.5)
    assert tag, 'The tag was not created'

@step(u'double click on the name of the tag "(.+)"')
def double_click_a_tag(step, tag_name):
    selector = '//span[@class="tag-name" and contains(., "%s")]' % tag_name
    tag = world.wait_for_element(selector, 5, 0.5)
    assert tag, 'Such tag does not exist'
    world.browser.execute_script('$(".tag-name:contains(%s)").dblclick()' % tag_name)

@step(u'see a text box with the text "(.+)"')
def see_text_box_with_tag_name(step, tag_name):
    selector = 'input.new-tag-name'
    input = world.wait_for_element(selector, 5, 0.5)
    assert input, 'Such input does not exist'

@step(u'replace it with "(.+)"')
def replace_tag_name(step, new_name):
    selector = '//input[@class="new-tag-name"]'
    input = world.wait_for_element(selector, 5, 0.5)
    input.click()
    input.value = new_name

@step(u'click elsewhere')
def click_elsewhere(step):
    selector = '#story-number'
    elsewhere = world.wait_for_element("#story-number", 5, 0.5)
    elsewhere.click()

@step(u'click the close button of the tag named "(.+)"')
def click_the_close_button_of_a_tag(step, tag_name):
    selector = '//span[@class="tag-delete ui-icon ui-icon-close" and ' \
        'preceding-sibling::span[@class="tag-name" and ' \
        'contains(., "%s")]]' % tag_name
    button = world.wait_for_element(selector, 5, 0.5)
    assert button, 'The tag "%s" was not found' % tag_name
    button.click()

@step(u'I do not see the tag named "(.+)"')
def do_not_see_some_tag(step, tag_name):
    def tag_was_deleted():
        selector = '//span[@class="tag-name" and contains(., "%s")]' % tag_name
        try:
            tag = world.wait_for_element(selector, 5, 0.5)
        except AssertionError:
            tag = None
        return tag is None
    world.wait_for_condition(tag_was_deleted)
