#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django import forms

from .forms import JCropAdminImageWidget


class JCropImageField(models.ImageField):

    def formfield(self, **kwargs):
        defaults = kwargs
        defaults.update({
            'form_class': forms.ImageField,
             'widget': JCropAdminImageWidget
        })
        return super(JCropImageField, self).formfield(**defaults)
