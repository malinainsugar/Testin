from django.shortcuts import render
from testin.models import Profession, Years, salaryCities, vacanciesCities
from testin.hhApi import hhApi

def index_page(reqest):
    data = {
        'profession_title': Profession.objects.get(id=1).title,
        'profession_description': Profession.objects.get(id=1).description.split('&&&')
    }
    return render(reqest, 'index.html', context=data)

def demand_page(reqest):
    data = {
        'profession': Profession.objects.get(id=1),
        'years' : [Years.objects.get(id=i) for i in range(1, 21)],
    }
    return render(reqest, 'demand.html', context=data)

def geography_page(reqest):
    data = {
        'salaryCities' : [salaryCities.objects.get(id=i) for i in range(1, 11)],
        'vacanciesCities' : [vacanciesCities.objects.get(id=i) for i in range(1, 11)],
    }
    return render(reqest, 'geography.html', context=data)

def skills_page(reqest):
    skills = []

    for i in range(0, 10):
        skills.append([Years.objects.get(year=year).skills.split(', ')[i] for year in range(2015, 2023)])

    data = {
        'profession': Profession.objects.get(id=1),
        'skills': skills,
    }
    return render(reqest, 'skills.html', context=data)

def vacancies_page(reqest):
    data = {
        'vacancies': hhApi.loadingVacancies(20, 12, 2022)
    }
    return render(reqest, 'recent-vacancies.html', context=data)
