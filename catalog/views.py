from django.shortcuts import render
from .models import Collection, Skin


def collection_list(request):
    context = {
        'collections': Collection.objects.all(),
    }
    return render(request, 'catalog/collection_list.html', context)


def skin_list(request):
    context = {
        'skins': Skin.objects.all(),
    }
    return render(request, 'catalog/skin_list.html', context)
