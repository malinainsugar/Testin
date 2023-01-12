from django.db import models

class Profession(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
