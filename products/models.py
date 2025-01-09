from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()

    def __str__(self):
        return self.title