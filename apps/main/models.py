from django.db import models


class MainContent(models.Model):
    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Главный контент'
        verbose_name_plural = 'Главный контент'