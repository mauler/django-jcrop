from django import forms
from django_jcrop.forms import JCropImageWidget

from models import ExampleModel


class ExampleForm(forms.ModelForm):
    image = forms.ImageField(widget=JCropImageWidget)


    class Meta:
        model = ExampleModel
