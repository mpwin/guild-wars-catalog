from django.shortcuts import render
from .models import Skin


def skin_list(request):
    context = {
        'skins': Skin.objects.all(),
    }
    return render(request, 'skins/skin_list.html', context)
