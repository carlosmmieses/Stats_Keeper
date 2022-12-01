"""
  
        Class Responsible for most of the operation
        Data Extraction from the PDF file
        Data Handling and insertion or update into the database
"""

import os, pathlib
from stat_keeper.pdf_file import PdfFile
from stat_keeper.player import Player
from stat_keeper.team import Team
from database.db_manager import DBManager

class StatKeeper:
    def __init__(self) -> None:
        self.pdf_directory = str(pathlib.Path(__file__).parent.parent.resolve()) + "\pdf"
        self.players_info = []
        self.db_manager = DBManager()
        try:
            os.path.isdir(self.pdf_directory)
        except Exception as e:
            print("Unable to find PDF directory")
            print(f"ERROR: {e}")
            print(f"PDF dir: {self.pdf_directory}")

    # list all PDF files in the pdf directory
    def get_pdf_files(self):
        return os.listdir(self.pdf_directory)

    # extract PDF contents
    def get_pdf_contents(self, pdf_file: str):
        pdf_file = PdfFile(self.pdf_directory + "\\" + pdf_file)
        return pdf_file.get_page(0)

    # extract player stats from PDF
    def extract_data(self, page, team_number):
        return list(filter(None, page[0].split("MIN")[team_number].split("Team")[0].split("\n")))
        
    # create a player object with all the data
    def store_extracted_data(self, extracted_data, team_name):
        player_info = []
        column_num = 0
        for info in extracted_data:
            if column_num == 13:
                column_num += 1
                continue
            player_info.append(info)
            column_num += 1
            if ":" in info or "DNP" in info:
                if "DNP" in info:
                    info = "00:00"
                self.players_info.append(Player(player_info, team_name))
                player_info = []
                column_num = 0
        return self.players_info
    
    # update the stats of the player
    def update_player_data(self, old_data: Player, new_data: Player, player_id):
        tfg_digit0 = int(old_data.tfg.split("/")[0]) + int(new_data.tfg.split("/")[0])
        tfg_digit1 = int(old_data.tfg.split("/")[1]) + int(new_data.tfg.split("/")[1])
        new_data.tfg = f"{tfg_digit0}/{tfg_digit1}"
        _2fg_digit0 = int(old_data._2fg.split("/")[0]) + int(new_data._2fg.split("/")[0])
        _2fg_digit1 = int(old_data._2fg.split("/")[1]) + int(new_data._2fg.split("/")[1])
        new_data._2fg = f"{_2fg_digit0}/{_2fg_digit1}"
        _3pt_digit0 = int(old_data._3pt.split("/")[0]) + int(new_data._3pt.split("/")[0])
        _3pt_digit1 = int(old_data._3pt.split("/")[1]) + int(new_data._3pt.split("/")[1])
        new_data._3pt = f"{_3pt_digit0}/{_3pt_digit1}"
        ft_digit0 = int(old_data.ft.split("/")[0]) + int(new_data.ft.split("/")[0])
        ft_digit1 = int(old_data.ft.split("/")[1]) + int(new_data.ft.split("/")[1])
        new_data.ft = f"{ft_digit0}/{ft_digit1}"
        
        new_data.pts += old_data.pts
        new_data.orb += old_data.orb
        new_data.drb += old_data.drb
        new_data.tr += old_data.tr 
        new_data.pf += old_data.pf 
        new_data.fd += old_data.fd 
        new_data.ast += old_data.ast
        new_data.to += old_data.to 
        new_data.bs += old_data.bs
        new_data.st += old_data.st
        time_minutes = int(old_data.minutes.split(":")[0]) + int(new_data.minutes.split(":")[0])
        time_seconds = int(old_data.minutes.split(":")[1]) + int(new_data.minutes.split(":")[1])
        new_data.minutes = f"{time_minutes}:{time_seconds}"
        if time_seconds or time_minutes:
            new_data.games_played = old_data.games_played + 1
        else:
            new_data.games_played = old_data.games_played
        if new_data.games_played:
            new_data.pts_per_game = new_data.pts / new_data.games_played
            new_data.drb_per_game = new_data.drb / new_data.games_played
            new_data.orb_per_game = new_data.orb / new_data.games_played
            new_data.tr_per_game = new_data.tr / new_data.games_played
            new_data.pf_per_game = new_data.pf / new_data.games_played
            new_data.fd_per_game = new_data.fd / new_data.games_played
            new_data.ast_per_game = new_data.ast / new_data.games_played
            new_data.to_per_game = new_data.to / new_data.games_played
            new_data.bs_per_game = new_data.bs / new_data.games_played
            new_data.st_per_game = new_data.st / new_data.games_played
        else:
            new_data.pts_per_game = 0
            new_data.drb_per_game = 0
            new_data.orb_per_game = 0
            new_data.tr_per_game = 0
            new_data.pf_per_game = 0
            new_data.fd_per_game = 0
            new_data.ast_per_game = 0
            new_data.to_per_game = 0
            new_data.bs_per_game = 0
            new_data.st_per_game = 0
        self.db_manager.update_player_data(new_data, player_id)

    # create database in case it does not exist
    def setup(self):
        if not self.db_manager.check_table_exists("FILE_HISTORY"):
            self.db_manager.create_files_table()
        if not self.db_manager.check_table_exists(self.db_manager.table_name):
            self.db_manager.create_table()
        if not self.db_manager.check_table_exists("TEAM_STATS"):
            self.db_manager.create_team_stats_table()
        self.db_manager.connection.commit()
        self.db_manager.connection.close()
        
    def print_pdf_contents(self, pdf):
        team = ["Visitors: ", "Home: "]
        for team_number in range(1, 3):
            page = self.get_pdf_contents(pdf)
            team_name = page[0].split(team[team_number-1])[1].split("\n")[0]
            info = self.extract_data(page, team_number)
            self.store_extracted_data(info, team_name)
      

    # workflow of extraction and insertion of the data into the database
    def run(self):
        print("Fetching for files...")
        pdf_files = self.get_pdf_files()
        print(f"{len(pdf_files)} files found!")
        for index, pdf in enumerate(pdf_files):
            print(f"\rExtracting data {index+1} / {len(pdf_files)}", end="")
            pdf_in_db = self.db_manager.get_files_uploaded(pdf)
            if not pdf_in_db:
                team = ["Visitors: ", "Home: "]
                for team_number in range(1,3):
                    page = self.get_pdf_contents(pdf)
                    team_name = page[0].split(team[team_number-1])[1].split("\n")[0].strip()
                    info = self.extract_data(page, team_number)
                    self.store_extracted_data(info, team_name)
                    team_obj = Team(team_name)
                    team_obj.update_num_games()
                    old_team_stats = self.db_manager.get_team_stats_id(team_obj.team)
                    if len(old_team_stats):
                        team_obj.update_num_games()
                        self.db_manager.update_team_stats_data(team_obj, old_team_stats[0][0])
                        self.db_manager.connection.commit()
                    else:
                        self.db_manager.insert_team_stats_data(team_obj)
                        self.db_manager.connection.commit()
                    for player in self.players_info:
                        old_player_stats = self.db_manager.get_player_id(player.name)
                        if len(old_player_stats):
                            self.update_player_data(Player(old_player_stats[0][2:], team_name), player, old_player_stats[0][0])
                            self.db_manager.connection.commit()
                        else:
                            self.db_manager.insert_player_data(player)
                            self.db_manager.connection.commit()
                    self.players_info = []
                self.db_manager.insert_file_data(pdf)
        team_list = self.db_manager.get_all_teams()
        for team_record in team_list:
          players_data = self.db_manager.get_player_stats_by_team(team_record[1])
          new_record = Team(team_record[1], team_record[17])
          new_record.update_values(players_data)
          self.db_manager.update_team_stats_data(new_record, team_record[0])
          self.db_manager.connection.commit()      
        self.db_manager.connection.commit()
        self.db_manager.connection.close()
        print("\nDone!")
