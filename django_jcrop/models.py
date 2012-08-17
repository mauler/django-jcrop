#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""Definition of JCropImageField with associated widget"""

from PIL import Image
from StringIO import StringIO
try:
    from json import loads
except ImportError:
    from simplejson import loads

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django import forms


class ClearableFileInput(forms.ClearableFileInput):

    def value_from_datadict(self, data, files, name):
        if forms.CheckboxInput().value_from_datadict(data, files,
                                                     "%s-crop" % name):
            forig = default_storage.open(data['%s-original' % name])
            im = Image.open(forig)
            width, height = im.size
            cdata = loads(data['%s-crop-data' % name])
            x_ratio = 1. * width / int(cdata['image_width'])
            y_ratio = 1. * height / int(cdata['image_height'])
            box = (cdata['x'] * x_ratio, cdata['y'] * y_ratio,
                   cdata['x2'] * x_ratio, cdata['y2'] * y_ratio)
            box = map(int, box)
            crop = im.crop(box)
            sio = StringIO()
            crop.save(sio, im.format)
            sio.seek(0)
            size = len(sio.read())
            sio.seek(0)
            f = InMemoryUploadedFile(
                sio, name, forig.name,
                "image/%s" % im.format.lower(), size, "utf-8"
            )
            files[name] = f

        upload = super(ClearableFileInput, self).value_from_datadict(data,
                                                                     files,
                                                                     name)
        if not self.is_required and forms.CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return forms.FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value,
            # as opposed to just None
            return False
        return upload


class JCropAdminImageWidget(ClearableFileInput):
    template_with_initial = (u'<p class="file-upload">%s</p>'
                            % ClearableFileInput.template_with_initial)
    template_with_clear = (u'<span class="clearable-file-input">%s</span>'
                           % ClearableFileInput.template_with_clear)

    class Media:
        js = (settings.STATIC_URL + "django_jcrop/js/jquery.Jcrop.min.js",)
        css = {"all": (
            settings.STATIC_URL + "django_jcrop/css/jquery.Jcrop.css",
        )}

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(forms.ClearableFileInput, self).render(
            name, value, attrs
        )

        print value

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['input_name'] = name
            substitutions['image_value'] = value
            substitutions['image_url'] = value.url
            substitutions['initial'] = (u'<a href="%s">%s</a>'
                                        % (escape(value.url),
                                           escape(force_unicode(value))))
            #if not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = conditional_escape(
                checkbox_name
            )
            substitutions['clear_checkbox_id'] = conditional_escape(
                checkbox_id
            )
            substitutions['clear'] = forms.CheckboxInput().render(
                checkbox_name, False, attrs={'id': checkbox_id}
            )
            substitutions['clear_template'] = self.template_with_clear % \
                    substitutions
        else:
            return mark_safe(template % substitutions)

        t = get_template("jcrop/jcrop_image_widget.html")
        substitutions.update({
            "JCROP_IMAGE_THUMBNAIL_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_THUMBNAIL_DIMENSIONS", "62x62"
            ),
            "JCROP_IMAGE_WIDGET_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_WIDGET_DIMENSIONS", "320x320"
            ),
        })
        c = Context(substitutions)
        return t.render(c)


class JCropImageField(models.ImageField):

    def formfield(self, **kwargs):
        defaults = kwargs
        defaults.update({'form_class': forms.ImageField,
                         'widget': JCropAdminImageWidget})
        return super(JCropImageField, self).formfield(**defaults)
