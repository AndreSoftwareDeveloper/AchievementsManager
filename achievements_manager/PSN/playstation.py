from django.contrib.staticfiles.storage import staticfiles_storage

from psnawp_api import PSNAWP
from psnawp_api.core.authenticator import Authenticator
from psnawp_api.models.search import Search
from psnawp_api.models.trophies.trophy import TrophyBuilder
from psnawp_api.models.trophies.trophy_titles import TrophyTitles
from psnawp_api.utils.request_builder import RequestBuilder


class PlayStation:

    def __init__(self):
        self.client = None
        self.request_builder = None
        self.search = None
        self.trophyTitles = None
        self.account_id = None
        self.trophyTitles = None

    @staticmethod
    def obtain_npsso():
        with staticfiles_storage.open('PSN/npssoSave.txt') as npssoSave:
            npsso_bytes = npssoSave.readline()
            npsso = npsso_bytes.decode('utf-8')
        npssoSave.close()
        if npsso is "":
            return "NO SAVE"
        return npsso

    def login(self, npsso):
        try:
            psnawp = PSNAWP(npsso)
            authenticator = Authenticator(npsso)
            self.request_builder = RequestBuilder(authenticator)
            self.client = psnawp.me()
            self.search = Search(self.request_builder)
            self.trophyTitles = TrophyTitles(self.request_builder, self.client.account_id)
            self.account_id = self.client.account_id
        except Exception as e:
            print(f"Error while signing up to PlayStation Network: : {str(e)}")

    @staticmethod
    def sum_trophies(title, is_earned: bool):
        if is_earned:
            trophy_status = title.earned_trophies
        else:
            trophy_status = title.defined_trophies
        return str(trophy_status.bronze +
                   trophy_status.silver +
                   trophy_status.gold +
                   trophy_status.platinum)

    def show_my_games(self):
        my_games = {}
        for trophy_title in self.client.trophy_titles(limit=None):
            game_title = trophy_title.title_name
            progress = f"{trophy_title.progress}% {self.sum_trophies(trophy_title, True)} / " \
                       f"{self.sum_trophies(trophy_title, False)}"
            my_games[game_title] = progress
        return my_games

    def trophies_for_game(self, title: str, requestBuilder, accountID):
        title_id = self.search.get_title_id(title)[1]  # error lies here
        # np_com_id = self.trophyTitles.get_np_communication_id(requestBuilder, title_id, accountID)
        # trophy_builder = TrophyBuilder(requestBuilder, np_com_id)
        # earned_trophies = trophy_builder.earned_game_trophies_with_metadata(accountID, "PS4", "default", 500)
        trophies = []
        # for trophy in earned_trophies:
        #     if trophy.earned:
        #         trophies.append(trophy)
        return trophies

    def show_library_data(self, choice):
        if choice == 1:
            return self.show_my_games()
        elif choice == 2:
            title = input("Podaj nazwę gry: ")
            return self.trophies_for_game(title, self.request_builder, self.account_id)
        elif choice == 3:
            exit()
        else:
            return "Nieprawidłowy wybór"
