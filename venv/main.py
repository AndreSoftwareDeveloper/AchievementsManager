import sys
from psnawp_api import PSNAWP
import psnawp_api
from enum import Enum

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


def show_games_data(choice):
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


# for dupa in client.trophies():
#      print(dupa)
# dupa = psnawp.game_title
#
show_games_data(choice)
