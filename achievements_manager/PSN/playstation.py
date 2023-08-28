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
        self.client = None
        self.request_builder = None
        self.search = None
        self.trophyTitles = None
        self.account_id = None


    def obtain_npsso(self):
        with staticfiles_storage.open('PSN/npssoSave.txt') as npssoSave:
            npsso_bytes = npssoSave.readline()
            npsso = npsso_bytes.decode('utf-8')
        npssoSave.close()
        if npsso is "":
            return "NO SAVE"
        else:
            return npsso

    def login(self, npsso):
        try:
            psnawp = PSNAWP(npsso)
            client = psnawp.me()
            authenticator = Authenticator(npsso)
            request_builder = RequestBuilder(authenticator)
            search = Search(request_builder)
            trophy_titles = TrophyTitles(request_builder, client.account_id)
            account_id = client.account_id

            self.client = client
            self.request_builder = request_builder
            self.search = search
            self.trophyTitles = trophy_titles
            self.account_id = account_id
        except Exception as e:
            print(f"Error while signing up to PlayStation Network: : {str(e)}")


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
        my_games = ""
        for trophy_title in self.client.trophy_titles(limit=None):
            my_games += trophy_title.title_name
            print(trophy_title.title_name)

            print(str(trophy_title.progress) + "%\t" +
                  sum_trophies(trophy_title, True) + '/' + sum_trophies(trophy_title, False) + "\n")
            return my_games


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
