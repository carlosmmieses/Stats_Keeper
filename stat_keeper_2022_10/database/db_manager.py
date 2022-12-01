"""
        2022 - Pietro Nardelli Mezzadri
        Class Responsible for dealing with the Database
        contains all SQL queries

"""

import sqlite3
from stat_keeper.player import Player

class DBManager:
    def __init__(self):
        try:
            self.connection = sqlite3.connect("stat_keeper.db")
            self.cursor = self.connection.cursor()
            self.table_name = "PLAYER_STATS"
        except Exception as e:
            print("Unable to establish connection with database")
            print(f"ERROR: {e}")
    
    def create_table(self):
        try:
            return self.cursor.execute(f"""CREATE TABLE {self.table_name}(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TEAM TEXT,
            NUMBER TEXT NOT NULL,
            NAME TEXT NOT NULL,
            TFG TEXT NOT NULL,
            _2FG TEXT NOT NULL,
            _3PT TEXT NOT NULL,
            FT TEXT NOT NULL,
            PTS INTEGER NOT NULL,
            DRB INTEGER NOT NULL,
            ORB INTEGER NOT NULL,
            TR INTEGER NOT NULL,
            PF INTEGER NOT NULL,
            FD INTEGER NOT NULL,
            AST INTEGER NOT NULL,
            _TO INTEGER NOT NULL,
            BS INTEGER NOT NULL,
            ST INTEGER NOT NULL,
            TIME_IN_MIN TEXT NOT NULL,
            NUM_GAMES INTEGER NOT NULL,
            PTS_PER_GAME REAL NOT NULL,
            DRB_PER_GAME REAL NOT NULL,
            ORB_PER_GAME REAL NOT NULL,
            TR_PER_GAME REAL NOT NULL,
            PF_PER_GAME REAL NOT NULL,
            FD_PER_GAME REAL NOT NULL,
            AST_PER_GAME REAL NOT NULL,
            _TO_PER_GAME REAL NOT NULL,
            BS_PER_GAME REAL NOT NULL,
            ST_PER_GAME REAL NOT NULL
            );""")
        except Exception as e:
            print("Unable to create table")
            print(f"ERROR: {e}")

    def create_files_table(self):
        try:
            return self.cursor.execute("""CREATE TABLE FILE_HISTORY(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FILENAME TEXT,
            UPLOADED_AT TEXT
            );""")
        except Exception as e:
            print("Unable to create files table")
            print(f"ERROR: {e}")
    
    def insert_player_data(self, player: Player):
        try:
            query_vars = list(vars(player).values())
            sql = f"""
                INSERT INTO {self.table_name}
                (TEAM, "NUMBER", NAME, TFG, _2FG, _3PT, FT, PTS, ORB, DRB, TR, PF,
                FD, AST, _TO, BS, ST, TIME_IN_MIN, NUM_GAMES, PTS_PER_GAME,
                ORB_PER_GAME, DRB_PER_GAME, TR_PER_GAME, PF_PER_GAME, FD_PER_GAME,
                AST_PER_GAME, _TO_PER_GAME, BS_PER_GAME, ST_PER_GAME)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            return self.cursor.execute(sql, query_vars)
        except Exception as e:
            print("Unable to insert record into table")
            print(f"ERROR: {e}")
            print(list(vars(player).values()))

    def update_player_data(self, player: Player, ID: int):
        try:
            sql = f"""
                UPDATE {self.table_name}
                SET NUMBER = ?,  TFG = ?,  _2FG = ?, _3PT = ?,  FT = ?,
                PTS = ?, ORB = ?,DRB = ?, TR = ?,  PF = ?, FD = ?, 
                AST = ?, _TO = ?, BS = ?, ST = ?, TIME_IN_MIN = ?,
                NUM_GAMES = ?, PTS_PER_GAME = ?, ORB_PER_GAME = ?, DRB_PER_GAME = ?,
                TR_PER_GAME = ?, PF_PER_GAME = ?, FD_PER_GAME = ?, AST_PER_GAME = ?,
                _TO_PER_GAME = ?, BS_PER_GAME = ?, ST_PER_GAME = ?
                WHERE ID = ?;
            """
            query_vars = list(vars(player).values())
            del query_vars[0]
            del query_vars[1]
            query_vars.append(ID)
            return self.cursor.execute(sql, query_vars)
        except Exception as e:
            print("Unable to update record")
            print(f"ERROR: {e}")

    def get_player_id(self, player_name):
        try:
            sql = f"""
                SELECT * FROM {self.table_name}
                WHERE NAME = "{player_name}";
            """
            result = self.cursor.execute(sql).fetchall()
            if len(result) > 1:
                raise Exception("More than one record with this information")
            else:
                return result
        except Exception as e:
            print("Unable to find player")
            print(f"ERROR: {e}")
            return []

    def check_table_exists(self, table_name):
        try:
            sql = f"""
                SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
            """
            return self.cursor.execute(sql).fetchone()
        except Exception as e:
            print("Unable to run sql")
            print(f"ERROR: {e}")

    def insert_file_data(self, file_name):
        try:
            sql = f"""
                INSERT INTO FILE_HISTORY (FILENAME, UPLOADED_AT)
                VALUES ("{file_name}", DATETIME('now'))
            """
            return self.cursor.execute(sql)
        except Exception as e:
            print("Unable to insert record into files table")
            print(f"ERROR: {e}")

    def get_files_uploaded(self, filename):
        try:
            return self.cursor.execute(f"""
                SELECT FILENAME FROM FILE_HISTORY
                WHERE FILENAME = "{filename}";
            """).fetchall()
        except Exception as e:
            print("Unable to get files")
            print(f"ERROR: {e}")
            
    def create_team_stats_table(self):
        try:
            return self.cursor.execute("""
            CREATE TABLE TEAM_STATS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TEAM TEXT NOT NULL,
                TFG TEXT NOT NULL,
                _2FG TEXT NOT NULL,
                _3PT TEXT NOT NULL,
                FT TEXT NOT NULL,
                PTS INTEGER NOT NULL,
                DRB INTEGER NOT NULL,
                ORB INTEGER NOT NULL,
                TR INTEGER NOT NULL,
                PF INTEGER NOT NULL,
                FD INTEGER NOT NULL,
                AST INTEGER NOT NULL,
                _TO INTEGER NOT NULL,
                BS INTEGER NOT NULL,
                ST INTEGER NOT NULL,
                TIME_IN_MIN TEXT NOT NULL,
                NUM_GAMES INTEGER NOT NULL,
                PTS_PER_GAME REAL NOT NULL,
                DRB_PER_GAME REAL NOT NULL,
                ORB_PER_GAME REAL NOT NULL,
                TR_PER_GAME REAL NOT NULL,
                PF_PER_GAME REAL NOT NULL,
                FD_PER_GAME REAL NOT NULL,
                AST_PER_GAME REAL NOT NULL,
                _TO_PER_GAME REAL NOT NULL,
                BS_PER_GAME REAL NOT NULL,
                ST_PER_GAME REAL NOT NULL
            )""")
        except Exception as e:
            print("Unable to create team statistics table")
            print(f"ERROR: {e}")
            
    def get_team_stats_id(self, team_name):
        try:
            return self.cursor.execute(f"""
                SELECT * FROM TEAM_STATS
                WHERE TEAM = "{team_name}";            
            """).fetchall()
        except Exception as e:
            print("Unable to retrieve team's id")
            print(f"ERROR: {e}")
            
    def insert_team_stats_data(self, team_data):
        try:
            sql = f"""
                INSERT INTO TEAM_STATS
                (TEAM, TFG, _2FG, _3PT, FT, PTS, ORB, DRB, TR, PF,
                FD, AST, _TO, BS, ST, TIME_IN_MIN, NUM_GAMES, PTS_PER_GAME,
                ORB_PER_GAME, DRB_PER_GAME, TR_PER_GAME, PF_PER_GAME, FD_PER_GAME,
                AST_PER_GAME, _TO_PER_GAME, BS_PER_GAME, ST_PER_GAME)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);                           
            """
            return self.cursor.execute(sql, list(vars(team_data).values()))
        except Exception as e:
            print("Unable to set team's data")
            print(f"ERROR: {e}")
            
    def update_team_stats_data(self, team_data, team_id):
        try:
            sql = f"""
                UPDATE TEAM_STATS
                SET TEAM = ?, TFG = ?, _2FG = ?, _3PT = ?, FT = ?, PTS = ?, ORB = ?, DRB = ?, TR = ?, PF = ?,
                FD = ?, AST = ?, _TO = ?, BS = ?, ST = ?, TIME_IN_MIN = ?, NUM_GAMES = ?, PTS_PER_GAME = ?,
                ORB_PER_GAME = ?, DRB_PER_GAME = ?, TR_PER_GAME = ?, PF_PER_GAME = ?, FD_PER_GAME = ?,
                AST_PER_GAME = ?, _TO_PER_GAME = ?, BS_PER_GAME = ?, ST_PER_GAME = ?
                WHERE ID = ?;                       
            """
            query_vars = list(vars(team_data).values())
            query_vars.append(team_id)
            return self.cursor.execute(sql, query_vars)
        except Exception as e:
            print("Unable to update team's data")
            print(f"ERROR: {e}")
            
    def get_all_teams(self):
        try:
            sql = f"""
                SELECT * FROM TEAM_STATS;
            """
            return self.cursor.execute(sql).fetchall()
        except Exception as e:
            print("Unable to fetch teams")
            print(f"ERROR: {e}")
            
    def get_player_stats_by_team(self, team_name):
        try:
            sql = f"""
                SELECT * FROM PLAYER_STATS
                WHERE TEAM = ?;
            """
            query_vars = [team_name]
            return self.cursor.execute(sql, query_vars).fetchall()
        except Exception as e:
            print("Unable to fetch column's data")
            print(f"ERROR: {e}")