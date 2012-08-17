from PIL import Image
from StringIO import StringIO
try:
    from json import loads
except ImportError:
    from simplejson import loads

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.template import Context
from django.template.loader import get_template
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
            print files[name]
            print files[name]
            print files[name]
            print files[name]
            print files[name]
            print files[name]

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

    class Media:
        js = (settings.STATIC_URL + "django_jcrop/js/jquery.Jcrop.min.js",)
        css = {"all": (
            settings.STATIC_URL + "django_jcrop/css/jquery.Jcrop.css",
        )}

    def render(self, name, value, attrs=None):
        t = get_template("jcrop/jcrop_image_widget.html")
        substitutions = {
            "input_name": name,
            "image_value": value,
            "JCROP_IMAGE_THUMBNAIL_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_THUMBNAIL_DIMENSIONS", "62x62"
            ),
            "JCROP_IMAGE_WIDGET_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_WIDGET_DIMENSIONS", "320x320"
            ),
        }
        c = Context(substitutions)
        clearable_input_render = super(ClearableFileInput, self).render(
            name, value, attrs
        )
        return clearable_input_render + t.render(c)
