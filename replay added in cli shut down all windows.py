import math
import tkinter as tk
from tkinter import messagebox
import random

score = {'PvP': {'X': 0, 'O': 0, 'Ties': 0},
                      'PvC': {'very very easy': {'X': 0, 'O': 0, 'Ties': 0},
                              'very easy': {'X': 0, 'O': 0, 'Ties': 0},
                              'easy': {'X': 0, 'O': 0, 'Ties': 0},
                              'medium': {'X': 0, 'O': 0, 'Ties': 0},
                              'hard': {'X': 0, 'O': 0, 'Ties': 0},
                              'impossible': {'X': 0, 'O': 0, 'Ties': 0}}}
current_player = 'X'

class TicTacToe:
    def __init__(self, master=None, cli=False):
        self.master = master
        self.cli = cli
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.difficulty = 'impossible'  # Default difficulty
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.difficulty = None
        self.game_mode = None
        if not cli:
            self.create_board()
    
    def create_board(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text='', font=('normal', 40), width=5, height=2,
                                               command=lambda row=i, col=j: self.click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.score_label = tk.Label(self.master, text=score, font=('normal', 20))
        self.score_label.grid(row=3, column=0, columnspan=3)

        self.replay_button = tk.Button(self.master, text='Replay', font=('normal', 20), command=self.reset)
        self.replay_button.grid(row=4, column=0, columnspan=3)

    def create_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.master, text='', font=('normal', 40), width=5, height=2,
                                                   command=lambda r=row, c=col: self.click(r, c))
                self.buttons[row][col].grid(row=row, column=col)

    def set_game_mode(self, mode):
        self.game_mode = mode

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        if not self.cli:
            for row in range(3):
                for col in range(3):
                    self.buttons[row][col].config(text='')

    def update_score(self, tie=False):
        if self.game_mode == 'PvP':
            if tie:
                score['PvP']['Ties'] += 1
            else:
                score['PvP'][current_player] += 1
        elif self.game_mode == 'PvC':
            if tie:
                score['PvC'][self.difficulty]['Ties'] += 1
            else:
                score['PvC'][self.difficulty][current_player] += 1

    def evaluate(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] != '':
                return 10 if self.board[row][0] == 'O' else -10

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '':
                return 10 if self.board[0][col] == 'O' else -10

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return 10 if self.board[0][0] == 'O' else -10

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return 10 if self.board[0][2] == 'O' else -10

        return 0

    def is_moves_left(self):
        for row in self.board:
            if '' in row:
                return True
        return False

    def minimax(self, depth, is_max, max_depth, player, opponent):
        score = self.evaluate()

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        #if score == 0:
            #return score + depth

        if not self.is_moves_left() or depth == max_depth:
            return 0

        if is_max:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = player
                        best = max(best, self.minimax(depth + 1, not is_max, max_depth, player, opponent))
                        self.board[i][j] = ''
            #self.click(best[0],best[1])
            return best
        else:
            worst = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = opponent
                        worst = min(worst, self.minimax(depth + 1, not is_max, max_depth, player, opponent))
                        self.board[i][j] = ''
            #self.click(worst[0],worst[1])
            return worst

    def find_best_move(self, max_depth, player, opponent, winner):
        best_val = -math.inf
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = player
                    move_val = self.average_score(0, player, max_depth, player, opponent, winner)
                    self.board[i][j] = ''
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val
        self.click(best_move[0],best_move[1])
        return best_move

    def find_worst_move(self, max_depth, player, opponent, winner):
        worst_val = math.inf
        worst_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = player
                    move_val = self.average_score(0, player, max_depth, player, opponent, winner)
                    self.board[i][j] = ''
                    if move_val < worst_val:
                        worst_move = (i, j)
                        worst_val = move_val
        self.click(worst_move[0],worst_move[1])
        return worst_move

    def average_score(self, depth, is_max, max_depth, player, opponent, winner):
        score = self.evaluate()

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        #elif score == 0:
            #return score + depth

        if not self.is_moves_left() or depth == max_depth:
            return 0

        scores = []
        if is_max:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        if winner:
                            self.board[i][j] = opponent
                        else:
                            self.board[i][j] = player
                        scores.append(self.minimax(depth + 1, not is_max, max_depth, player, opponent))
                        self.board[i][j] = ''
        else:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        if winner:
                            self.board[i][j] = player
                        else:
                            self.board[i][j] = opponent
                        scores.append(self.minimax(depth + 1, not is_max, max_depth, player,opponent))
                        self.board[i][j] = ''
        
        return sum(scores) / len(scores) if scores else 0
    
    def computer_move(self):
        if self.difficulty == 'very very easy':
            #self.minimax(0, False, 9, player = 'X', opponent = 'O')
            self.find_worst_move(9, player = 'O', opponent = 'X', winner = False)
        elif self.difficulty == 'very easy':
            self.random_move()
        elif self.difficulty == 'easy':
            if not self.block_or_win_move():
                #self.minimax(0, False, 9)
                self.find_worst_move(9, player = 'O', opponent = 'X', winner = False)
        elif self.difficulty == 'medium':
            if not self.block_or_win_move():
                if not self.create_fork():
                    if not self.block_fork():
                        self.random_move()
        elif self.difficulty == 'hard':
            self.find_best_move(3, player = 'O', opponent = 'X', winner = True)
        elif self.difficulty == 'impossible':
            self.find_best_move(10, player = 'O', opponent = 'X', winner = True)

        current_player = 'X'

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def check_tie(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return False
        
        return True
    
    def random_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']
        row, col = random.choice(empty_cells)
        self.click(row, col)

    def block_or_win_move(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    # Check for winning move
                    self.board[row][col] = 'O'
                    if self.check_winner():
                        self.click(row, col)
                        return True
                    self.board[row][col] = ''
                    
                    # Check for blocking move
                    self.board[row][col] = 'X'
                    if self.check_winner():
                        self.board[row][col] = 'O'
                        self.click(row, col)
                        return True
                    self.board[row][col] = ''
        return False

    def create_fork(self):
        # Triangle tactic (gridStrategy1)
        if self.board[1][1] == '':
            self.click(1, 1)
            return True
        if self.board[1][1] == 'X':
            if self.board[0][0] == '':
                self.click(0, 0)
                return True
            if self.board[2][2] == '':
                self.click(2, 2)
                return True
            if self.board[0][2] == '':
                self.click(0, 2)
                return True
            if self.board[2][0] == '':
                self.click(2, 0)
                return True

        # Arrowhead tactic (gridStrategy2)
        if self.board[2][1] == '':
            self.click(2, 1)
            return True
        if self.board[2][1] == 'X':
            if self.board[1][1] == '':
                self.click(1, 1)
                return True
            if self.board[1][0] == '':
                self.click(1, 0)
                return True
            if self.board[1][2] == '':
                self.click(1, 2)
                return True
            if self.board[0][0] == '':
                self.click(0, 0)
                return True
            if self.board[0][2] == '':
                self.click(0, 2)
                return True

        # Encirclement tactic (strategyCross)
        if self.board[0][0] == '':
            self.click(0, 0)
            return True
        if self.board[0][0] == 'X':
            if self.board[1][1] == '':
                self.click(1, 1)
                return True
            if self.board[2][2] == '':
                self.click(2, 2)
                return True
            if self.board[0][2] == '':
                self.click(0, 2)
                return True
            if self.board[2][0] == '':
                self.click(2, 0)
                return True

        return False

    def block_fork(self):
        # Triangle tactic (gridStrategy1)
        if self.board[1][1] == '':
            self.board[1][1] = 'X'
            if self.count_winning_moves('X') > 1:
                #self.board[1][1] = 'O'
                self.click(1,1)
                return True
            self.board[1][1] = ''
        if self.board[1][1] == 'X':
            if self.board[0][0] == '':
                self.board[0][0] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[0][0] = 'O'
                    self.click(0,0)
                    return True
                self.board[0][0] = ''
            if self.board[2][2] == '':
                self.board[2][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[2][2] = 'O'
                    self.click(2,2)
                    return True
                self.board[2][2] = ''
            if self.board[0][2] == '':
                self.board[0][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[0][2] = 'O'
                    self.click(0,2)
                    return True
                self.board[0][2] = ''
            if self.board[2][0] == '':
                self.board[2][0] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[2][0] = 'O'
                    self.click(2,0)
                    return True
                self.board[2][0] = ''

        # Arrowhead tactic (gridStrategy2)
        if self.board[2][1] == '':
            self.board[2][1] = 'X'
            if self.count_winning_moves('X') > 1:
                #self.board[2][1] = 'O'
                self.click(2,1)
                return True
            self.board[2][1] = ''
        if self.board[2][1] == 'X':
            if self.board[1][1] == '':
                self.board[1][1] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[1][1] = 'O'
                    self.click(1,1)
                    return True
                self.board[1][1] = ''
            if self.board[1][0] == '':
                self.board[1][0] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[1][0] = 'O'
                    self.click(1,0)
                    return True
                self.board[1][0] = ''
            if self.board[1][2] == '':
                self.board[1][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[1][2] = 'O'
                    self.click(1,2)
                    return True
                self.board[1][2] = ''
            if self.board[0][0] == '':
                self.board[0][0] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[0][0] = 'O'
                    self.click(0,0)
                    return True
                self.board[0][0] = ''
            if self.board[0][2] == '':
                self.board[0][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[0][2] = 'O'
                    self.click(0,2)
                    return True
                self.board[0][2] = ''

        # Encirclement tactic (strategyCross)
        if self.board[0][0] == '':
            self.board[0][0] = 'X'
            if self.count_winning_moves('X') > 1:
                #self.board[0][0] = 'O'
                self.click(0,0)
                return True
            self.board[0][0] = ''
        if self.board[0][0] == 'X':
            if self.board[1][1] == '':
                self.board[1][1] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[1][1] = 'O'
                    self.click(1,1)
                    return True
                self.board[1][1] = ''
            if self.board[2][2] == '':
                self.board[2][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[2][2] = 'O'
                    self.click(2,2)
                    return True
                self.board[2][2] = ''
            if self.board[0][2] == '':
                self.board[0][2] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[0][2] = 'O'
                    self.click(0,2)
                    return True
                self.board[0][2] = ''
            if self.board[2][0] == '':
                self.board[2][0] = 'X'
                if self.count_winning_moves('X') > 1:
                    #self.board[2][0] = 'O'
                    self.click(2,0)
                    return True
                self.board[2][0] = ''

        return False

    def count_winning_moves(self, player):
        count = 0
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = player
                    if self.check_winner():
                        count += 1
                    self.board[row][col] = ''
        return count

    def click(self, row, col):
        #if self.board[row][col] == '':
            global current_player
            self.board[row][col] = current_player
            if not self.cli:
                self.buttons[row][col].config(text=current_player)
            else:

                print_board(self.board)
                print('\n')

            if self.check_winner():
                self.update_score()
                self.display_scores(f"Player {current_player} wins!")
                #self.ask_play_again()

            elif self.check_tie():
                self.update_score(tie=True)
                self.display_scores("It's a tie!")
                #self.ask_play_again()
            else:
                current_player = 'O' if current_player == 'X' else 'X'
                if self.game_mode == 'PvC' and current_player == 'O':
                    self.computer_move()
    
    def reset_scores(self):
        score = {'PvP': {'X': 0, 'O': 0, 'Ties': 0},
                      'PvC': {'very easy': {'X': 0, 'O': 0, 'Ties': 0},
                              'easy': {'X': 0, 'O': 0, 'Ties': 0},
                              'medium': {'X': 0, 'O': 0, 'Ties': 0},
                              'hard': {'X': 0, 'O': 0, 'Ties': 0},
                              'impossible': {'X': 0, 'O': 0, 'Ties': 0}}}
    
    #ahh
    def display_scores(self, message):
        if self.cli:
            print(message)
            print("Player vs Player Scores:")
            print(f"X: {score['PvP']['X']}, O: {score['PvP']['O']}, Ties: {score['PvP']['Ties']}")
            print("Player vs Computer Scores:")
            for level in score['PvC']:
                print(f"Level {level.capitalize()}: X: {score['PvC'][level]['X']}, O: {score['PvC'][level]['O']}, Ties: {score['PvC'][level]['Ties']}")
        else:
            
            #result_window = tk.Toplevel(self.TicTacToe.root)
            result_window = tk.Toplevel()
            result_window.title("Game Over")
            #result_window.geometry("300x450")
            result_window.geometry("300x475")

            # Display the winning/tie message
            win_label = tk.Label(result_window, text=message, font=("Helvetica", 16))
            win_label.pack(pady=10)

            # Display Player vs Player Scores
            pvp_label = tk.Label(result_window, text="Player vs Player Scores:", font=("Helvetica", 14))
            pvp_label.pack(pady=5)

            pvp_scores = score['PvP']
            pvp_score_text = f"X: {pvp_scores['X']}, O: {pvp_scores['O']}, Ties: {pvp_scores['Ties']}"
            score_label = tk.Label(result_window, text=pvp_score_text, font=("Helvetica", 12))
            score_label.pack()

            # Display Player vs Computer Scores
            pvc_label = tk.Label(result_window, text="Player vs Computer Scores:", font=("Helvetica", 14))
            pvc_label.pack(pady=5)

            pvc_scores = score['PvC']
            for level, level_scores in pvc_scores.items():
                level_label = tk.Label(result_window, text=f"Level {level.capitalize()}:", font=("Helvetica", 12))
                level_label.pack()
                level_score_text = f"X: {level_scores['X']}, O: {level_scores['O']}, Ties: {level_scores['Ties']}"
                score_label = tk.Label(result_window, text=level_score_text, font=("Helvetica", 12))
                score_label.pack()
            
            
            close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
            close_button.pack()
            #self.ask_play_again(result_window)
            self.ask_play_again(result_window)


    #ahh
    #def ask_play_again(self, result_window):
    def ask_play_again(self, result_window):
        if not self.cli:
            play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
            self.master.destroy()
            #result_window.destroy()

            #self.root.destroy()
            #tk.Tk.destroy(self)
            #result_window.destroy()
            #window.destory(result_window)

        else:
            play_again = input("Play again? (y/n): ").lower() == 'y'

        if play_again:
            
            #print(current_player)
            #current_player = 'O' if current_player == 'X' else 'X'
            #self.reset_board()
            main()
        else:
            exit()


def print_board(board):
    for row in board:
        print('|'.join([cell if cell != '' else ' ' for cell in row]))
        print('-' * 5)

def get_move(board):
    while True:
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1
            if row in range(3) and col in range(3):
                if board[row][col] != 'O' and board[row][col] != 'X':
                    return row, col
                else:
                    print("That space is already filled. Please choose another.")
            else:
                print("Invalid input. Please enter numbers between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter numbers between 1 and 3.")

def cli_game():
    game = TicTacToe(cli=True)
    game.set_game_mode('PvP')
    while True:
        print_board(game.board)
        row, col = get_move(game.board)
        game.click(row, col)
        if game.check_winner() or game.check_tie():
            game.display_scores()
            if game.ask_play_again() != 'y':
                break
            game.reset_board()
#TicTacToe.current_player = 'X'
def main():
    while True:
        mode = input("Choose game mode: 1 for Player vs Player, 2 for Player vs Computer: ")
        if mode == '1' or mode == '2':
            break    
        else:
            print("Please enter 1 or 2")

    if mode == '1':
        if input("Play in CLI? (y/n): ").lower() == 'y':
            cli_game()
        else:
            root = tk.Tk()
            game = TicTacToe(root)
            game.set_game_mode('PvP')
            root.mainloop()
    elif mode == '2':
        while True:
            difficulty = input("Choose difficulty: very very easy, very easy, easy, medium, hard, impossible: ").lower()
                
            if difficulty not in ['ver very easy', 'very easy', 'easy', 'medium', 'hard', 'impossible']:
                print("Please enter very very easy, very easy, easy, medium, hard, impossible: ")
            else:
                break
        
        while True:
            cli = input("Play in CLI? (y/n): ").lower()
            if cli != 'y' and cli != 'n':
                print("Enter y or n")
            else:
                break

        if cli == 'y':
            game = TicTacToe(cli=True)
            game.set_game_mode('PvC')
            game.set_difficulty(difficulty)
            while True:
                print_board(game.board)
                
                if current_player == 'X':
                    row, col = get_move(game.board)
                    game.click(row, col)
                else:
                    game.computer_move()
                    print_board(game.board)

                if game.check_winner() or game.check_tie():

                    game.update_score()
                    game.display_scores()
                    if game.ask_play_again() != 'y':
                        break
                    game.reset_board()
        else:
            root = tk.Tk()
            game = TicTacToe(root)
            game.set_game_mode('PvC')
            game.set_difficulty(difficulty)
            root.mainloop()

if __name__ == "__main__":
    main()
