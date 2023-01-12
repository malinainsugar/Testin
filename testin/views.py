from django.shortcuts import render
from testin.models import Profession

def index_page(reqest):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(reqest, 'index.html', context=data)
