from django.http import HttpResponse
from django.template import loader
from .playstation import PlayStation
from .forms import PsnSignInForm


psn = PlayStation()

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

    trophies_for_game = psn.trophies_for_game("Horizon Zero Dawn", psn.request_builder, psn.account_id)
    trophies_data = [ [] for _ in range(len(trophies_for_game)) ]
    for i in range(0, len(trophies_for_game)):
         trophies_data[i].append(trophies_for_game[i].trophy_name)
         trophies_data[i].append(trophies_for_game[i].trophy_type)
         trophies_data[i].append(trophies_for_game[i].trophy_detail)
         trophies_data[i].append(trophies_for_game[i].trophy_icon_url)
         trophies_data[i].append(trophies_for_game[i].earned_date_time)
         trophies_data[i].append(trophies_for_game[i].trophy_rarity)

    context = {
        'games': games,
        'trophies_data': trophies_data
    }
    return HttpResponse(template.render(context, request))


def game(request):
    pass
