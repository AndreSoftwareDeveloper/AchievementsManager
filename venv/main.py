import sys
from psnawp_api import PSNAWP
import psnawp_api
from enum import Enum

try:
    psnawp = input("Enter valid npsso code: ")       #TODO: będzie ogarnięty frontend to zrobić jakąś instrukcję dla użytkownika, odnośniki do odpowiednich stron
    npssoSave = open("npssoSave.txt", 'w')           #TODO: input powinien być w pętli wykonującej się dopóki użytkownik poda prawidłowy npsso
    print(psnawp, file=npssoSave)
    npssoSave.close()
except psnawp_api.core.psnawp_exceptions.PSNAWPAuthenticationError:
    print("Incorrect npsso code. Unable to authenticate.")
    sys.exit()


psnawp = PSNAWP(psnawp)
client = psnawp.me()
print("Your nick is: " + client.online_id + "\n")

choice = int(input("1 - Show my games\n" +
                   "2 -  Show trophies for specific game\n"))

def sum_trophies(title, isEarned : bool):
    if isEarned:
         trophyStatus = title.earned_trophies
    else:
         trophyStatus = title.defined_trophies 
    return str(trophyStatus.bronze + 
               trophyStatus.silver +
               trophyStatus.gold +
               trophyStatus.platinum)

def show_my_games():
            for trophy_title in client.trophy_titles(limit = None):
                print(trophy_title.title_name)
                print(str(trophy_title.progress) + "%\t" + 
                      sum_trophies(trophy_title, True) +'/' + sum_trophies(trophy_title, False) + "\n")
                
def show_games_data(x):
    match x:
        case 1:
              show_my_games()
        case 2:
              raise NotImplementedError("Option like that doesn't exist yet!") 
        case _:
                print("There is no such option.")

for dupa in client.trophies():
     print(dupa)
dupa = psnawp.game_title

show_games_data(choice)
