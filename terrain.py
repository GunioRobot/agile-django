# terrain.py
from lettuce import before, after, world
from splinter.browser import Browser
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command
from django.db import connection
from django.conf import settings

@before.harvest
def initial_setup(server):
    settings.LANGUAGES = (
        ('en', 'English'),
    )
    settings.DATABASES['default']['NAME'] = 'test.sqlite'
    call_command('syncdb', interactive=False, verbosity=0)
    call_command('flush', interactive=False, verbosity=0)
    #call_command('migrate', interactive=False, verbosity=0)
    call_command('loaddata', 'all', verbosity=0)
    setup_test_environment()
    world.browser = Browser('webdriver.chrome')

@after.harvest
def cleanup(server):
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    teardown_test_environment()

@before.each_scenario
def reset_data(scenario):
    # Clean up django.
    call_command('flush', interactive=False, verbosity=0)
    call_command('loaddata', 'all', verbosity=0)
    world.browser.visit('http://localhost:8000')

@after.all
def teardown_browser(total):
    world.browser.quit()
