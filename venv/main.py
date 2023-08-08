import sys
from psnawp_api import PSNAWP
import psnawp_api
from enum import Enum
from psnawp_api.core import authenticator

try:
    # psnawp = input("Enter valid npsso code: ")        #TODO: input powinien być w pętli wykonującej się dopóki użytkownik poda prawidłowy npsso
    with open(
            "npssoSave.txt") as npssoSave:  # TODO: będzie ogarnięty frontend to zrobić jakąś instrukcję dla użytkownika, odnośniki do odpowiednich stron
        npsso = npssoSave.readline()
    npssoSave.close()
    psnawp = PSNAWP(npsso)
except psnawp_api.core.psnawp_exceptions.PSNAWPAuthenticationError as errorMessage:
    print(errorMessage)
    sys.exit()

client = psnawp.me()
print("Your nick is: " + client.online_id + "\n")
choice = int(input("1 - Show my games\n" +
                   "2 -  Show trophies for specific game\n"))


def show_library_data(choice):
    match choice:
        case 1:
            show_my_games()
        case 2:
            raise NotImplementedError("Option like that doesn't exist yet!")
        case _:
            print("There is no such option.")


def show_my_games():
    for trophy_title in client.trophy_titles(limit=None):
        print(trophy_title.title_name)
        print(str(trophy_title.progress) + "%\t" +
              sum_trophies(trophy_title, True) + '/' + sum_trophies(trophy_title, False) + "\n")


def sum_trophies(title, is_earned: bool):
    if is_earned:
        trophy_status = title.earned_trophies
    else:
        trophy_status = title.defined_trophies
    return str(trophy_status.bronze +
               trophy_status.silver +
               trophy_status.gold +
               trophy_status.platinum)


def list_games():
    data = []
    titles = []
    for trophy_title in client.trophy_titles(limit=None):
        titles.append(trophy_title.title_name)
        data.append(trophy_title)
    return data, titles


def trophies_for_game(title: str, data: list, titles: list):
    if title in titles:
        index = titles.index(title)
        game = data[index]
        get_trophy_summary_for_title()
    else:
        print("Game not found!")
        exit()


games_data = list_games()[0]  # TODO optimization
games_titles = list_games()[1]
show_library_data(choice)
# trophies_for_game("Assassin's Creed® IV Black Flag", games_data, games_titles)

authenticator = psnawp_api.core.authenticator.Authenticator(npsso)                  # TODO refactor
requestBuilder = psnawp_api.utils.request_builder.RequestBuilder(authenticator)
trophyTitles = psnawp_api.models.trophies.trophy_titles.TrophyTitles(requestBuilder, client.account_id)
np_communication_id = trophyTitles.get_np_communication_id(requestBuilder, "CUSA13323_00", client.account_id)

print(np_communication_id)
trophy_titles_generator = client.trophy_summary()
print(trophy_titles_generator)
