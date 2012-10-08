from django.contrib import admin

import models
import forms


class ExampleAdmin(admin.ModelAdmin):
    class Media:
        js = ('jquery-1.8.2.js', )

    form = forms.ExampleForm

admin.site.register(models.ExampleModel, ExampleAdmin)
