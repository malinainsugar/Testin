from django.db import models

class Profession(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

class Years(models.Model):
    year = models.IntegerField('Год')
    salaryYear = models.IntegerField('Средняя зарплата')
    numberVacancies = models.IntegerField('Количество вакансий')
    selectedSalaryYear = models.IntegerField('Средняя зарплата для выбранной профессии')
    selectedNumberVacancies = models.IntegerField('Количество вакансий для выбранной профессии')
    skills = models.TextField('Навыки')

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Год'
        verbose_name_plural = 'Года'

class salaryCities(models.Model):
    city = models.CharField('Город', max_length=50)
    salary = models.IntegerField('Средняя зарплата')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города по зарплатам'


class vacanciesCities(models.Model):
    city = models.CharField('Город', max_length=50)
    vacancies = models.FloatField('Доля вакансий')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города по кол-ву вакансий'
    