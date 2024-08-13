import csv

from django.contrib.staticfiles.storage import staticfiles_storage

from psnawp_api import PSNAWP
from psnawp_api.core import RequestBuilderHeaders
from psnawp_api.core.authenticator import Authenticator
from psnawp_api.core.psnawp_exceptions import PSNAWPBadRequest
from psnawp_api.models.listing import PaginationArguments
from psnawp_api.models.trophies.trophy_titles import TrophyTitleIterator


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

        if npsso == "":
            return "NO SAVE"
        return npsso

    def login(self, npsso):
        try:
            psnawp = PSNAWP(npsso)
            request_builder_headers: RequestBuilderHeaders = {
                "User-Agent": "SampleUserAgent",
                "Accept-Language": "pl-PL",
                "Country": "PL",
            }
            authenticator = Authenticator(npsso, request_builder_headers)
            self.client = psnawp.me()
            pagination_arguments = PaginationArguments(1, 3, 10)
            self.trophyTitles = TrophyTitleIterator(authenticator,
                                                    "dupa", pagination_arguments, None)
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

    def obtain_title_id(self, title):
        with staticfiles_storage.open('PSN/data.tsv', 'r') as games_data_table:
            games_data = csv.reader(games_data_table, delimiter='\t')
            title = title.rstrip()
            title = title.lstrip()

            for game_data_line in games_data:
                if title in game_data_line[2]:
                    return game_data_line[0]

        raise PSNAWPBadRequest

    def trophies_for_game(self, title: str, requestBuilder, accountID):

        try:
            title_id = self.search.get_title_id(title)[1]
        except PSNAWPBadRequest:  # if the API responsible for obtaining IDs is down, read the IDs from the table
            title_id = self.obtain_title_id(title)

        np_com_id = self.trophyTitles.get_np_communication_id(requestBuilder, title_id, accountID)
        trophy_builder = TrophyBuilder(requestBuilder, np_com_id)
        earned_trophies = trophy_builder.earned_game_trophies_with_metadata(accountID, "PS4", "default", 500)
        trophies = []

        for trophy in earned_trophies:
            if trophy.earned:
                trophies.append(trophy)

        return trophies

    def show_library_data(self, choice):
        match choice:
            case 1:
                choice.show_my_games()
            case 2:
                choice.trophies_for_game(self.request_builder, self.account_id)
            case 3:
                exit()
