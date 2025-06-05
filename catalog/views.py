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
    weapon = Skin.objects.filter(
        category='Weapon',
        collection__isnull=True,
    ).order_by('name')
    armor = Skin.objects.filter(
        category='Armor',
        collection__isnull=True,
    ).order_by('name')
    back = Skin.objects.filter(category='Back').order_by('name')
    gathering = Skin.objects.filter(category='Gathering').order_by('name')

    context = {
        'weapon_skins': weapon,
        'armor_skins': armor,
        'back_skins': back,
        'gathering_skins': gathering,
    }
    return render(request, 'catalog/skin_list.html', context)
