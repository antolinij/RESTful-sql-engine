# django
from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Director'

    name = models.CharField(max_length=100, verbose_name='Name', default="")


class Movie(models.Model):

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    title = models.CharField(max_length=200, verbose_name='Name', default="", unique=True)
    release_date = models.DateTimeField(verbose_name='release date')
    imdb_ranking = models.FloatField()
    director = models.ForeignKey(Director, verbose_name='Director', related_name='director', on_delete=models.CASCADE, blank=False, null=False, default="")