from django.shortcuts import render
from .models import Collection, Skin


def collection_list(request):
    weapon = Collection.objects.filter(category='Weapon').order_by('name')
    armor = Collection.objects.filter(category='Armor').order_by('name')

    context = {
        'weapon_collections': weapon,
        'armor_collections': armor,
    }
    return render(request, 'catalog/collection_list.html', context)


def skin_list(request):
    context = {
        'skins': Skin.objects.all(),
    }
    return render(request, 'catalog/skin_list.html', context)
