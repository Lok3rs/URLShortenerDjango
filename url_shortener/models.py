from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=6, allow_unicode=True, primary_key=True)
