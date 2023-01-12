from django.shortcuts import render
from testin.models import Profession

def index_page(reqest):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(reqest, 'index.html', context=data)

def demand_page(reqest):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(reqest, 'demand.html', context=data)

def geography_page(reqest):
    data = {}
    return render(reqest, 'geography.html', context=data)

def skills_page(reqest):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(reqest, 'skills.html', context=data)

def vacancies_page(reqest):
    data = {}
    return render(reqest, 'recent-vacancies.html', context=data)
