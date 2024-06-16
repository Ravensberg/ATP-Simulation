from pointsimulation import PointSimulation
from player import Player
from dataclasses import dataclass, field
import random


@dataclass
class MatchSimulation:
    POINTS = [0, 15, 30, 40, 'AD', 'GAME']

    best_of_sets: int = 3
    winners_sets: int = 0
    match_score: list[list[int]] = field(default_factory=list)

    player_a: str = ''
    player_b: str = ''

    sim_count: int = 1000
    player_a_wins: int = 0
    player_b_wins: int = 0

    player_a_stats = {
        'ace': 0,
        'serve': 0,
        'return': 0,
        'double_fault': 0,
        '1st_serve_in': 0,
        '1st_serve_won': 0,
        '2nd_serve_won': 0,
        'break_point_faced': 0,
        'break_point_saved': 0,
        'break_point_oppy': 0,
        'break_point_won': 0,
        '1st_serve_return_won': 0,
        '2nd_serve_return_won': 0
    }

    player_b_stats = {
        'ace': 0,
        'serve': 0,
        'return': 0,
        'double_fault': 0,
        '1st_serve_in': 0,
        '1st_serve_won': 0,
        '2nd_serve_won': 0,
        'break_point_faced': 0,
        'break_point_saved': 0,
        'break_point_oppy': 0,
        'break_point_won': 0,
        '1st_serve_return_won': 0,
        '2nd_serve_return_won': 0
    }

    sets_score: list[int] = field(default_factory=list)
    games_score: list[int] = field(default_factory=list)
    points_score: list[int] = field(default_factory=list)
    match_winner: str = ''

    point_simulation: PointSimulation = None
    simulation_finished: bool = False

    def simulate_n_games(self, simulation_count: int):
        for i in range(simulation_count):
            match_winner, sets_score = self.simulate_match()
            if match_winner == self.player_a:
                self.player_a_wins += 1
            else:
                self.player_b_wins += 1
            self.reset_simulation()

        print(
            f'{self.player_a}: {self.player_a_wins / simulation_count:.2%} - {self.player_b}: {self.player_b_wins / simulation_count:.2%}. Wins over {simulation_count} games.')

    def initialize_simulation(self, player_a: Player, player_b: Player):
        # Reset all scores
        self.reset_simulation()
        self.player_a, self.player_b = player_a.name, player_b.name

        '''
        player_b.ace = 1
        player_b.double_fault = 1
        player_b.first_serve_in = 1
        player_b.first_serve_won = 1
        player_b.second_serve_won = 1
        player_b.break_point_saved = 1
        player_b.return_first_serve_won = 1
        player_b.return_second_serve_won = 1
        player_b.break_point_won = 1
        '''

        #print(
        #    f'player_a: {player_a.ace}, {player_a.first_serve_in}, {player_a.first_serve_won}, {player_a.return_first_serve_won}, {player_a.break_point_won} \n'
        #    f' vs \n'
        #    f'player_b: {player_b.ace}, {player_b.first_serve_in}, {player_b.first_serve_won}, {player_b.return_first_serve_won}, {player_b.break_point_won}')

        # Coin toss
        rng = random.randint(1, 100)
        if rng <= 50:
            self.point_simulation = PointSimulation(server=player_a, returner=player_b)
        else:
            self.point_simulation = PointSimulation(server=player_b, returner=player_a)

    def reset_simulation(self):
        # Reset Sets, Games and Points to 0
        self.sets_score = [0, 0]
        self.games_score = [0, 0]
        self.points_score = [0, 0]
        self.match_score = []

        if self.best_of_sets == 5:
            self.winners_sets = 3
        else:
            self.winners_sets = 2

    def swap_players(self):
        self.point_simulation.swap_server_returner()

    def simulate_match(self) -> (str, int):
        while not self.check_match_has_a_winner():
            self.simulate_set()

        return self.match_winner, sum(self.sets_score)

    def simulate_set(self):
        # Reset games for the new set
        self.games_score = [0, 0]

        while not self.check_set_has_a_winner():
            if self.games_score == [6, 6] and sum(self.sets_score) < self.best_of_sets:
                self.simulate_tie_break()
            else:
                self.simulate_game()

    def simulate_game(self):
        # Reset points for the new game
        self.points_score = [0, 0]

        while not self.check_game_has_a_winner():
            self.simulate_point(game_type='Standard')

        self.swap_players()

    def simulate_tie_break(self):
        # Reset points for the new game
        self.points_score = [0, 0]

        while not self.check_tie_break_has_a_winner():
            self.simulate_point(game_type='Tie-Break')

            # Change server every 2 points
            if sum(self.points_score) % 2 != 0:
                self.swap_players()

        self.swap_players()

    def check_match_has_a_winner(self) -> bool:
        if sum(self.sets_score) < self.winners_sets:
            return False

        for player_idx in range(2):
            if self.sets_score[player_idx] == self.winners_sets:
                self.simulation_finished = True
                if player_idx == 0:
                    self.match_winner = self.player_a
                else:
                    self.match_winner = self.player_b
                #print(f'{self.match_winner} has won the match {self.match_score} !')
                return True
        return False

    def check_set_has_a_winner(self) -> bool:
        if sum(self.games_score) < 6:
            return False

        # Set 3/5 needs a 2 games differences
        for player_idx in range(2):
            if (sum(self.sets_score) < self.best_of_sets - 1 and self.games_score[player_idx] == 6 and sum(
                    self.games_score) <= 10) or \
                    (sum(self.sets_score) < self.best_of_sets - 1 and self.games_score[player_idx] == 7) or \
                    (sum(self.sets_score) == self.best_of_sets - 1 and self.games_score[player_idx] >= 6 and
                     self.games_score[player_idx] > sum(self.games_score) - self.games_score[player_idx] + 1):
                self.sets_score[player_idx] += 1
                self.match_score.append(self.games_score)
                '''if player_idx == 0:
                    print(f'{self.player_a} has won the set {self.games_score}')
                else:
                    print(f'{self.player_b} has won the set {self.games_score}')
                '''
                return True
        return False

    def check_game_has_a_winner(self) -> bool:
        if sum(self.points_score) < 4:
            return False

        for player_idx in range(2):
            player_points = self.points_score[player_idx]
            if (player_points == 4 and sum(self.points_score) < 7) or \
                    (player_points > 4 and player_points > sum(self.points_score) - player_points + 1):
                self.games_score[player_idx] += 1
                '''if player_idx == 0:
                    print(f'{self.player_a} has won the game!')
                else:
                    print(f'{self.player_b} has won the game!')
                '''
                return True
        return False

    def check_tie_break_has_a_winner(self) -> bool:
        if sum(self.points_score) < 7:
            return False

        for player_idx in range(2):
            player_points = self.points_score[player_idx]
            if (player_points == 7 and sum(self.points_score) < 6) or \
                    (player_points >= 7 and player_points > sum(self.points_score) - player_points + 1):
                self.games_score[player_idx] += 1
                '''
                if player_idx == 0:
                    print(f'{self.player_a} has won the tie-break {self.points_score}!')
                else:
                    print(f'{self.player_b} has won the tie-break {self.points_score}!')
                '''
                return True
        return False

    def simulate_point(self, game_type: str = 'Standard'):
        point_winner, method, point_type, server_name = self.point_simulation.sim_point(points_score=self.points_score,
                                                                                        player_a=self.player_a,
                                                                                        game_type=game_type)
        self.keep_track_of_points_data(point_winner=point_winner, method=method, point_type=point_type,
                                       server_name=server_name)
        if point_winner == self.player_a:
            self.points_score[0] += 1
        else:
            self.points_score[1] += 1

        # self.print_score(game_type=game_type)

    def keep_track_of_points_data(self, point_winner: str, method: str, point_type: str, server_name: str) -> None:
        if server_name == self.player_a:
            self.player_a_stats['serve'] += 1
            self.player_b_stats['return'] += 1
            if point_winner == self.player_a:
                self.player_a_stats[method] += 1
            else:
                self.player_b_stats[method] += 1
            if method in ['ace', '1st_serve_won', '1st_serve_return_won']:
                self.player_a_stats['1st_serve_in'] += 1
        else:
            self.player_b_stats['serve'] += 1
            self.player_a_stats['return'] += 1
            if point_winner == self.player_b:
                self.player_b_stats[method] += 1
            else:
                self.player_a_stats[method] += 1
            if method in ['ace', '1st_serve_won', '1st_serve_return_won']:
                self.player_b_stats['1st_serve_in'] += 1

        if point_type == 'Break Oppy':
            if server_name == self.player_a:
                self.player_a_stats['break_point_faced'] += 1
                self.player_b_stats['break_point_oppy'] += 1
                if point_winner == self.player_a:
                    self.player_a_stats['break_point_saved'] += 1
                else:
                    self.player_b_stats['break_point_won'] += 1
            else:
                self.player_b_stats['break_point_faced'] += 1
                self.player_a_stats['break_point_oppy'] += 1
                if point_winner == self.player_b:
                    self.player_b_stats['break_point_saved'] += 1
                else:
                    self.player_a_stats['break_point_won'] += 1

    def print_score(self, game_type: str = 'Standard'):
        if game_type != 'Standard':
            score_a = self.points_score[0]
            score_b = self.points_score[1]

            if self.point_simulation.server.name == self.player_a:
                print(f'{score_a} - {score_b}!')
            else:
                print(f'{score_b} - {score_a}!')
            return

        if (self.points_score[0] == 4 and self.points_score[1] <= 2) or (
                self.points_score[0] >= 4 and self.points_score[0] - self.points_score[1] > 1):
            idx_a = 5
            idx_b = min(3, self.points_score[1])
        elif (self.points_score[1] == 4 and self.points_score[0] <= 2) or (
                self.points_score[1] >= 4 and self.points_score[1] - self.points_score[0] > 1):
            idx_a = min(3, self.points_score[0])
            idx_b = 5
        elif (self.points_score[0] >= 4 and self.points_score[0] == self.points_score[1]) or (
                self.points_score[1] >= 4 and self.points_score[0] == self.points_score[1]):
            # 40-40
            idx_a = 3
            idx_b = 3
        elif self.points_score[0] >= 4 and self.points_score[0] > self.points_score[1]:
            # AD
            idx_a = 4
            idx_b = 3
        elif self.points_score[1] >= 4 and self.points_score[1] > self.points_score[0]:
            idx_a = 3
            idx_b = 4
        else:
            idx_a = min(3, self.points_score[0])
            idx_b = min(3, self.points_score[1])

        score_a = self.POINTS[idx_a]
        score_b = self.POINTS[idx_b]

        if self.point_simulation.server.name == self.player_a:
            print(f'{score_a} - {score_b}!')
        else:
            print(f'{score_b} - {score_a}!')
