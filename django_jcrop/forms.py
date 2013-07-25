from PIL import Image
from StringIO import StringIO
try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.template import Context
from django.template.loader import get_template
from django import forms


class JCropImageWidget(forms.ClearableFileInput):
    ratio = '0'
    jquery_alias = None

    def __init__(self, *args, **kwargs):
        if 'attrs' in kwargs:
            if 'ratio' in kwargs['attrs']:
                self.ratio = kwargs['attrs'].pop('ratio')
            if 'jquery_alias' in kwargs['attrs']:
                self.jquery_alias = kwargs['attrs'].pop('jquery_alias')

        return super(JCropImageWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (
            settings.STATIC_URL + "django_jcrop/js/jquery.Jcrop.min.js",
        )
        css = {"all": (
            settings.STATIC_URL + "django_jcrop/css/jquery.Jcrop.css",
            settings.STATIC_URL + "django_jcrop/css/jcrop-widget.css"
        )}

    def value_from_datadict(self, data, files, name):
        if data["%s-crop-data" % name]:
            forig = default_storage.open(data['%s-original' % name])
            im = Image.open(forig)
            width, height = im.size
            cdata = json.loads(data['%s-crop-data' % name])
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

        upload = super(JCropImageWidget, self).value_from_datadict(data,
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

    def render(self, name, value, attrs=None):
        t = get_template("jcrop/jcrop_image_widget.html")
        substitutions = {
            "input_name": name,
            "image_value": value,
            "ratio": self.ratio,
            "jquery_alias": self.jquery_alias,
            "MEDIA_URL": settings.MEDIA_URL,
            "JCROP_IMAGE_THUMBNAIL_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_THUMBNAIL_DIMENSIONS", "62x62"
            ),
            "JCROP_IMAGE_WIDGET_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_WIDGET_DIMENSIONS", "320x320"
            ),
        }
        c = Context(substitutions)
        clearable_input_render = super(JCropImageWidget, self).render(
            name, value, attrs
        )
        return clearable_input_render + t.render(c)
