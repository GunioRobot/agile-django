AgileDjango
===========

Translation scripts
-------------------
`django-admin.py makemessages -l es`  
`django-admin.py makemessages -l de`  
`django-admin.py makemessages -l fr`  
`django-admin.py makemessages -l pt`  
`django-admin.py makemessages -l ru`  
`django-admin.py makemessages -l it`

`$('.suggest').click();$(':checked').click()`


Dump database to fixture
------------------------
`python manage.py dumpdata --indent=1 -e sessions -e admin -e contenttypes > agile/fixtures/initial_data.json`


Graph models in PNG format
------------
`python manage.py graph_models -a -g -o models.png`
