from django.db import models


class ExampleModel(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')

    def __unicode__(self):
        return self.title
