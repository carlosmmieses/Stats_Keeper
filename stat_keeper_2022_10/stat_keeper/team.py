class Team:
    def __init__(self, team_name, num_games = 0):
        self.team = str(team_name).upper()
        self.tfg = "0/0"
        self._2fg = "0/0"
        self._3pt = "0/0"
        self.ft = "0/0"
        self.pts = 0 
        self.drb = 0 
        self.orb = 0
        self.tr = 0 
        self.pf = 0 
        self.fd = 0 
        self.ast = 0 
        self._to = 0 
        self.bs = 0 
        self.st = 0 
        self.time_in_min = "" 
        self.num_games = num_games
        self.pts_per_game = 0
        self.drb_per_game = 0 
        self.orb_per_game = 0 
        self.tr_per_game = 0 
        self.pf_per_game = 0 
        self.fd_per_game = 0
        self.ast_per_game = 0
        self._to_per_game = 0 
        self.bs_per_game = 0 
        self.st_per_game = 0
        
    def update_values(self, players):
        for player in players:
            self.tfg = str(f"{int(player[4].split('/')[0])+int(self.tfg.split('/')[0])}/{int(player[4].split('/')[1])+int(self.tfg.split('/')[1])}")
            self._2fg = str(f"{int(player[5].split('/')[0])+int(self.tfg.split('/')[0])}/{int(player[5].split('/')[1])+int(self.tfg.split('/')[1])}")
            self._3pt = str(f"{int(player[6].split('/')[0])+int(self.tfg.split('/')[0])}/{int(player[6].split('/')[1])+int(self.tfg.split('/')[1])}")
            self.ft = str(f"{int(player[7].split('/')[0])+int(self.tfg.split('/')[0])}/{int(player[7].split('/')[1])+int(self.tfg.split('/')[1])}")
            self.pts += player[8]
            self.drb += player[9] 
            self.orb += player[10]
            self.tr += player[11] 
            self.pf += player[12] 
            self.fd += player[13] 
            self.ast += player[14] 
            self._to += player[15] 
            self.bs += player[16] 
            self.st += player[17]
        if self.num_games:
            self.time_in_min = str(self.num_games * 200)
            self.pts_per_game = self.pts / self.num_games
            self.drb_per_game = self.drb / self.num_games 
            self.orb_per_game = self.orb / self.num_games 
            self.tr_per_game = self.tr / self.num_games 
            self.pf_per_game = self.pf / self.num_games 
            self.fd_per_game = self.fd / self.num_games
            self.ast_per_game = self.ast / self.num_games
            self._to_per_game = self._to / self.num_games 
            self.bs_per_game = self.bs / self.num_games 
            self.st_per_game = self.st / self.num_games
    
    def update_num_games(self):
        self.num_games += 1
        