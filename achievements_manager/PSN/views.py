from django.http import HttpResponse
from django.template import loader
from .playstation import PlayStation
from .forms import PsnSignInForm
import json


psn = PlayStation()

def serialize_trophies(trophy):
    return {
        'trophy_name': trophy.trophy_name,
        'trophy_type': trophy.trophy_type,
        'trophy_detail': trophy.trophy_detail,
        'trophy_icon_url': trophy.trophy_icon_url,
        'earned_date_time': trophy.earned_date_time,
        'trophy_rarity': trophy.trophy_rarity,
    }


def platforms(request):
    global psn
    template = loader.get_template('platforms.html')
    psn_form = PsnSignInForm(request.POST)
    psn_form.fields['npsso'].error_messages = {'required': ''}
    saved_npsso = psn.obtain_npsso()

    if saved_npsso != "NO SAVE":
        psn.login(saved_npsso)

    if psn_form.is_valid():
        npsso = psn_form.cleaned_data['npsso']
        psn.login(npsso)
    else:
        npsso = ''

    context = {
        'psn': psn,
        'psn_form': psn_form,
        'npsso': npsso,
        'saved_npsso': saved_npsso
    }

    return HttpResponse(template.render(context, request))


def PSN(request):
    global psn
    template = loader.get_template('PSN.html')
    games = psn.show_my_games()
    context = {
        'games': games
    }
    return HttpResponse(template.render(context, request))


def game(request):
    template = loader.get_template('game.html')
    selected_game = str( request.session.get('selected_game') )

    session_values = request.session.items()
    for key, value in session_values:
        print(f'Klucz: {key}, Wartość: {value}')

    trophies_for_game = psn.trophies_for_game("Horizon Zero Dawn", psn.request_builder, psn.account_id)
    trophies_data = [[] for _ in range(len(trophies_for_game))]
    for i in range(0, len(trophies_for_game)):
        trophies_data[i].append(str(trophies_for_game[i].trophy_name))
        trophies_data[i].append(str(trophies_for_game[i].trophy_type))
        trophies_data[i].append(str(trophies_for_game[i].trophy_detail))
        trophies_data[i].append(str(trophies_for_game[i].trophy_icon_url))
        trophies_data[i].append(str(trophies_for_game[i].earned_date_time))
        trophies_data[i].append(str(trophies_for_game[i].trophy_rarity))

    context = {
        'trophies_data': trophies_data,
        'dupa': selected_game
    }
    return HttpResponse(template.render(context, request))
