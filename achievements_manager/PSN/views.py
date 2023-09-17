from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .forms import PsnSignInForm
from .playstation import PlayStation
from .models import User

psn = PlayStation()


def serialize_trophies(trophy):  # dead code? TODO: check this and eventually delete
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

    if request.method == 'POST':
        register = request.POST.get('register', '')
        if register == 'Submit':
            nick = request.POST.get('nick', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = User(nick=nick, email=email, encrypted_password=password)
            user.encrypted_password = user.set_password(password)
            user.save()

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


@csrf_exempt
def game(request):
    template = loader.get_template('game.html')
    selected_game = request.POST.get('selected_game', None)

    trophies_for_game = psn.trophies_for_game(selected_game, psn.request_builder, psn.account_id)
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
        'dupa': selected_game  # dead code?
    }
    return HttpResponse(template.render(context, request))
