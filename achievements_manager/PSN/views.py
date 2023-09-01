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
    trophies_data = [[] for _ in range(len(trophies_for_game))]

        dupa.append(trophy) #.trophy_name trophy_type trophy_detail trophy_icon_url earned_date_time trophy_rarity


    context = {
        'games': games,
        'dupa': dupa
    }
    return HttpResponse(template.render(context, request))
