# django-jcrop
This a prototype, the code is working but not ideally (black magic present).

Installation
------------
```
pip install django-jcrop
```

Configuration
-------------
Put 'easy_thumbnails' and 'sorl.thumbnail' on your INSTALLED_APPS settings.
```python
INSTALLED_APPS = [
    '...',
    'sorl.thumbnail',
    'django_jcrop',
    '...',
]


```

Models
-----
```python
from django_jcrop.models import JCropImageField

class MyModel(models.Model):
    image = JCropImageField(blank=True)
```

Admin usage
-----------
Go to model edit view and see the crop feature, select an area:

![First step][1]

And save:

![Second step][2]

  [1]: https://dl.dropboxusercontent.com/u/3341989/django-jcrop-step1.png
  [2]: https://dl.dropboxusercontent.com/u/3341989/django-jcrop-step2.png
