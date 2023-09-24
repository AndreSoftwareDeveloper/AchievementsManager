import bcrypt
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .forms import PsnSignInForm
from .models import User
from .playstation import PlayStation

psn = PlayStation()


def sign_up(request):
    nick = request.POST.get('nick', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    repeat_password = request.POST.get('repeat_password', '')
    if password == repeat_password:
        user = User(nick=nick, email=email, encrypted_password=password)
        user.encrypted_password = User.encrypt_password(password)
        user.save()
        return 0
    return 1


def log_in(request):  # TODO: refactor
    nick = request.POST.get('nick', '')
    password = request.POST.get('password', '')
    try:
        logged_user = User.objects.get(Q(nick=nick) | Q(email=nick))
        if bcrypt.checkpw(password.encode('utf-8'), logged_user.encrypted_password.encode('utf-8')):
            login(request, logged_user)  # logged successfully
        else:
            raise User.DoesNotExist
    except User.DoesNotExist:  # user does not exist
        return 1  # error_message = "Incorrect nickname or password."


def platforms(request):
    global psn
    template = loader.get_template('platforms.html')
    psn_form = PsnSignInForm(request.POST)
    psn_form.fields['npsso'].error_messages = {'required': ''}
    saved_npsso = psn.obtain_npsso()
    error_message = ""

    if saved_npsso != "NO SAVE":
        psn.login(saved_npsso)

    if psn_form.is_valid():
        npsso = psn_form.cleaned_data['npsso']
        psn.login(npsso)
    else:
        npsso = ''

    users = User.objects.all()  # listing of created User objects, just for debugging purpose
    for user in users:
        print(user.nick, user.email, user.encrypted_password)

    if request.method == 'POST':
        register_form = request.POST.get('register', '')
        login_form = request.POST.get('login', '')

        if register_form == 'Submit' and sign_up(request) == 1:  # registration
            error_message = "Passwords are not the same."
        if login_form == 'Submit':                               # login
            log_in(request)

    context = {
        'psn': psn,
        'psn_form': psn_form,
        'npsso': npsso,
        'saved_npsso': saved_npsso,
        'error_message': error_message
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
        'selected_game': selected_game
    }
    return HttpResponse(template.render(context, request))
