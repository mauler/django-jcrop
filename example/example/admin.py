from django.contrib import admin

import models
import forms


class ExampleAdmin(admin.ModelAdmin):
    class Media:
        js = ('jquery-1.9.1.min.js', )

    form = forms.ExampleForm

admin.site.register(models.ExampleModel, ExampleAdmin)
