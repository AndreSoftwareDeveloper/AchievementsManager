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


def log_in(request):
    nick = request.POST.get('nick', '')
    password = request.POST.get('password', '')
    try:
        logged_user = User.objects.get(Q(nick=nick) | Q(email=nick))
        if bcrypt.checkpw(password.encode('utf-8'), logged_user.encrypted_password.encode('utf-8')):
            login(request, logged_user)
            return 0  # logged successfully
    except User.DoesNotExist:
        return 1
    return 1


def list_users():
    users = User.objects.all()
    for user in users:
        print(user.nick, user.email, user.encrypted_password)


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

    list_users()  # for debugging purpose

    if request.method == 'POST':
        register_form = request.POST.get('register', '')
        login_form = request.POST.get('login', '')

        if register_form == 'Submit' and sign_up(request) == 1:  # registration
            error_message = "Passwords are not the same."

        if login_form == 'Submit' and log_in(request) == 1:  # login
            error_message = "Incorrect nickname or password."

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
    selected_game = request.POST.get('selected_game', None)
    trophies_for_game = psn.trophies_for_game(selected_game, psn.request_builder, psn.account_id)

    trophies_data = [
        [
            str(t.trophy_name),
            str(t.trophy_type),
            str(t.trophy_detail),
            str(t.earned_date_time),
            str(t.trophy_rarity),
        ] for t in trophies_for_game
    ]

    trophies_icons = [str(t.trophy_icon_url) for t in trophies_for_game]

    context = {
        'trophies_data': trophies_data,
        'trophies_icons': trophies_icons,
        'selected_game': selected_game
    }

    return HttpResponse(loader.get_template('game.html').render(context, request))
