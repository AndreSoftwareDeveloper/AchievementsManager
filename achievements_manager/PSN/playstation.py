import sys
from enum import Enum

from django.contrib.staticfiles.storage import staticfiles_storage

import psnawp_api
from psnawp_api import PSNAWP
from psnawp_api.core.authenticator import Authenticator
from psnawp_api.core.psnawp_exceptions import PSNAWPAuthenticationError as errorMessage
from psnawp_api.models.game_title import GameTitle
from psnawp_api.models.trophies.trophy import TrophyBuilder
from psnawp_api.models.trophies.trophy_titles import TrophyTitles
from psnawp_api.utils.request_builder import RequestBuilder
from psnawp_api.models.search import Search


class PlayStation:

    def __init__(self):
        pass


    def obtain_npsso(self):
        with staticfiles_storage.open('PSN/npssoSave.txt') as npssoSave:
            npsso_bytes = npssoSave.readline()
            npsso = npsso_bytes.decode('utf-8')
        npssoSave.close()
        if npsso is "":
            return "ERROR"
        else:
            return npsso

    # try:
    #     psnawp = input("Enter valid npsso code: ")
    #     npsso = "xGhVVqUSyW8Q15f0GrhXqdN6fwbnZ7KWZf54FLeaCFz87edUfaTKtA2KSHdmFLo7"
    #     psnawp = PSNAWP(npsso)
    # except errorMessage:
    #     print(errorMessage)
    #     sys.exit()
    #
    # client = psnawp.me()
    # authenticator = Authenticator(npsso)
    # request_builder = RequestBuilder(authenticator)
    # search = Search(request_builder)
    # trophyTitles = TrophyTitles(request_builder, client.account_id)
    # account_id = client.account_id


    def show_library_data(choice):
        match choice:
            case 1:
                show_my_games()
            case 2:
                trophies_for_game(request_builder, account_id)
            case 3:
                exit()
            case _:
                print("There is no such option!")


    def show_my_games(self):
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


    def list_games(self):
        data = []
        titles = []
        for trophy_title in self.client.trophy_titles(limit=None):
            titles.append(trophy_title.title_name)
            data.append(trophy_title)
        return data, titles


    def trophies_for_game(self, requestBuilder, accountID):
        title = input("Enter game title: ")
        title_id = search.get_title_id(title)[1]
        np_com_id = trophyTitles.get_np_communication_id(requestBuilder, title_id, accountID)
        trophy_builder = TrophyBuilder(requestBuilder, np_com_id)
        earned_trophies = trophy_builder.earned_game_trophies_with_metadata(accountID, "PS4", "default", 500)
        for trophy in earned_trophies:
            if trophy.earned:
                print(trophy)


    def test(self):
        games_data, games_titles = self.list_games()

        while True:
            print("Your nick is: " + client.online_id + "\n")
            option = int(input("1 - Show my games\n" +
                           "2 - Show trophies for specific game\n" +
                           "3 - Exit\n"))

            show_library_data(option)


    def test2(self):
        return "dupa"


