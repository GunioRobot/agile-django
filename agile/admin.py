from django.contrib import admin
import agile.models

for k, v in agile.models.__dict__.items():
    try:
        if agile.models.models.Model in v.__bases__:
            admin.site.register(v)
    except:
        pass
