import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import re

# Hangman stages
hangman_stages = [
    """
 ------
 |    |
      |
      |
      |
      |
 -----------
    """,
    """
 ------
 |    |
 O    |
      |
      |
      |
 -----------
    """,
    """
 ------
 |    |
 O    |
 |    |
      |
      |
 -----------
    """,
    """
 ------
 |    |
 O    |
/|    |
      |
      |
-----------
    """,
    """
 ------
 |    |
 O    |
/|\   |
      |
      |
 -----------
    """,
    """
 ------
 |    |
 O    |
/|\   |
/     |
      |
      |
-----------
    """,
    """
 ------
 |    |
 O    |
/|\   |
/ \   |
      |
 -----------
    """
]

# Select a random word
def select_word():
    words = ["python", "java", "kotlin", "javascript"]
    return random.choice(words)

# Update the hangman drawing
def update_hangman():
    hangman_label.config(text=hangman_stages[current_stats["tries"]])

# Function to update the word_completion variable
def update_word_completion():
    global word_completion
    display_word = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    word_completion.set(display_word)

# Function to check the guessed letter
def check_guess(event=None):
    global current_stats, guessed_letters
    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)
    
    if not guess:
        messagebox.showinfo("Info", "You must enter a letter.")
        return

    if guess in guessed_letters:
        messagebox.showinfo("Info", f"You already guessed the letter {guess}.")
    elif guess in word:
        guessed_letters.append(guess)
        messagebox.showinfo("Info", f"{guess} is in the word!")
        update_word_completion()
        if "_" not in word_completion.get():
            messagebox.showinfo("Congratulations", f"{current_stats['name']} You guessed the word!")
            current_stats["wins"] += 1
            current_stats["streak"] += 1
            if current_stats["streak"] >= current_stats["life time streak"]:
                current_stats["life time streak"] = current_stats["streak"]
            
            if current_stats["name"] != "single player":
                switch_turn()
            else:
                single_player()
    else:
        guessed_letters.append(guess)

        if len(guess) == 1:
            messagebox.showinfo("Info", f"{guess} is not in the word!")
            current_stats["tries"] += 1
            update_hangman()
        else:
            messagebox.showinfo("Info", "You must enter a letter")

        if current_stats["tries"] == len(hangman_stages) - 1:
            current_stats["losses"] += 1
            current_stats["streak"] = 0
            messagebox.showinfo("Game Over", f"{current_stats['name']} You lost! The word was: {word}")
            
            if current_stats["name"] != "single player":
                switch_turn()
            else:
                single_player()

#unused since doesn't make sense (in my opinon)
# Replay the game (reset the current round to begin guessing from scratch no new word chosen no change to stats)
def replay_round():
    global word_completion, guessed_letters, current_stats
    word_completion.set(" ".join("_" * len(word)))
    guessed_letters = []
    current_stats["tries"] = 0
    update_word_completion()
    update_hangman()

    #commented out showing stats since stats are unchanged
    # --and for debugging
    #new_window(current_stats)

#reselect word (in case of mistake made during selection --primarily for pvp)
#like replay game, does not affect score, resets tries and hangmand, chooses new word instead of keeping old one
#used in case of mistake made in word slection (two player), or a secondary skip button wihtout consequence (single player)
def choose_new_word():
    global word, word_completion, guessed_letters, current_stats

    #check game type then the current player
    if game_type == "player vs computer":
        word == select_word() if current_stats == player_vs_computer_stats else word == computer_turn()
    elif game_type == "player vs player":
        word == first_player_word() if current_stats == first_player_stats else word == second_player_word()
    else:
        word == select_word()

    word_completion.set(" ".join("_" * len(word)))
    guessed_letters = []
    current_stats["tries"] = 0
    update_word_completion()
    update_hangman()

# Reset the game
def reset_stats():
    global word, word_completion, guessed_letters, current_stats
    word_completion = tk.StringVar(value=" ".join("_" * len(word)))
    word_completion.set(" ".join("_" * len(word)))
    guessed_letters = []
    current_stats["tries"] = 0
    current_stats["wins"] = 0
    current_stats["losses"] = 0
    current_stats["streak"] = 0
    current_stats["rounds"] = 0
    current_stats["life time streak"] = 0
    update_hangman()

    new_window(current_stats)

    #could be uncommented
    #would cause a double show score for the single player (reset + begining of new round)
    #switch_turn()

def new_window(stats):
    messagebox.showinfo("Your stats", f"{stats}")

# Function to start a new game
def new_round():
    global word, guessed_letters, current_stats
    guessed_letters = []
    current_stats["tries"] = 0
    update_word_completion()
    update_hangman()
    game_frame.pack()
    menu_frame.pack_forget()

    new_window(current_stats)



#check
#check

#add menu continue with score(s) reset and end question
# end the game
def end_game():
    if game_type == "player vs computer":
        if current_stats == player_vs_computer_stats:
            new_window(player_vs_computer_stats)
            new_window(computer_stats)
        else:
            new_window(computer_stats)
            new_window(player_vs_computer_stats)
    elif game_type == "player vs player":
        if current_stats == first_player_stats:
            new_window(first_player_stats)
            new_window(second_player_stats)
        else:
            new_window(second_player_stats)
            new_window(first_player_stats)
    else:
        new_window(single_player_stats)

    # Confirm the streak will be lost
    if messagebox.askyesno("Warning", "Your streak will be lost. Are you sure you want to end the game?"):
        # Confirm if this is the decision the player wants to make
        if messagebox.askyesno("Warning", "Are you sure you want to lose your streak and close the window?"):
            # Tell the player that they gave up the round, display the word they were supposed to guess, then change to the other player's turn
            messagebox.showinfo("Hangman", "Thanks for playing!")
            game_frame.quit()

#give up on the round
#go to next round (which includes next player if applicable)
def give_up():
    global current_stats
    current_stats["losses"] += 1
    current_stats["streak"] = 0
    current_stats["rounds"] += 1

    #Confirm the streak will be lost
    if messagebox.askyesno("Warning", "Your streak will be lost. Are you sure you want to give up?"):
        #confirm if this is the decision the player wants to make
        if messagebox.askyesno("Warning", "Are you sure you want to lose your streak and begin the next turn?"):
        
            #Tell the player that they gave up the round, display the word they were supposed to guess, then change to the other players turn
            messagebox.showinfo("Hangman", f"You gave up the round. The word was {word}.\n wins: {current_stats['wins']}\nlosses: {current_stats['losses']}\nstreak: {current_stats['streak']}\nLifetime streak: {current_stats['life time streak']}\nrounds: {current_stats['rounds']}")
            switch_turn()
    
#Go back to menu
def go_back_to_menu():
    if game_type == "player vs computer":
        new_window(player_vs_computer_stats), new_window(computer_stats) if current_stats == player_vs_computer_stats else new_window(computer_stats), new_window(player_vs_computer_stats) 
    elif game_type == "player vs player":
        new_window(first_player_stats), new_window(second_player_stats) if current_stats == first_player_stats else new_window(second_player_stats), new_window(first_player_stats)
    else:
        new_window(single_player_stats)

    game_frame.pack_forget()
    menu_frame.pack()

#Function to switch turns between players or player and computer
def switch_turn():
    global word, guessed_letters, current_stats, player_vs_computer_stats, computer_stats, first_player_stats, second_player_stats, game_type
    
    if game_type == "player vs computer":
        computer_turn() if current_stats == player_vs_computer_stats else player_turn()
    elif game_type == "player vs player":
        second_player_word() if current_stats == first_player_stats else first_player_word()
    #for single player
    else:
        #could do word select and then new round functions instead feels unecessary
        single_player()
        
# Choosing who goes first
def choose_first_player():
    choice = simpledialog.askstring("Choose First Player", "Enter 'user', 'computer', or 'random' (u, c, r):").lower()
    if choice in ['user', 'u']:
        return True
    elif choice in ['computer', 'c']:
        return False
    elif choice in ['random', 'r']:
        return random.choice([True, False])
    else:
        messagebox.showinfo("Invalid Input", "Please enter a valid option.")
        return choose_first_player()

# Choosing who goes first for two players
def choose_first_player_two():
    while True:
        choice = simpledialog.askstring("Choose First Guessing Player", "Enter 'first', 'second', or 'random' (1, 2, r):").lower()
        if choice in ['first', 'first player', 'fp', 'f', '1']:
            return True
        elif choice in ['second', 'second player', 'sp', 's', '2']:
            return False
        elif choice in ['random', 'r', '3']:
            return random.choice([True, False])
        else:
            messagebox.showinfo("Invalid Input", "Please enter a valid option.")

# Obfuscated word entry
def obfuscated_word_entry(prompt):
    while True:
        global word
        word = simpledialog.askstring("Word Entry", prompt, show='*')

        if word.isalpha():
            return word
        else:
            messagebox.showinfo("Invalid Input", "Please enter a valid word containing only letters.")

# Computer guessing logic
def computer_guess():
    global current_stats
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    current_stats["tries"] = 0
    while current_stats["tries"] < len(hangman_stages) - 1:
        guess = random.choice(alphabet)
        alphabet = alphabet.replace(guess, '')
        if guess in guessed_letters:
            continue
        elif guess not in word:
            messagebox.showinfo("Hangman", f"Computer guessed {guess}. It's not in the word.")
            current_stats["tries"] += 1
            guessed_letters.append(guess)
        else:
            messagebox.showinfo("Hangman", f"Computer guessed {guess}. It's in the word!")
            guessed_letters.append(guess)
            word_as_list = list(word_completion.get().replace(" ", ""))
            indices = [i for i, letter in enumerate(word) if letter == guess]
            for index in indices:
                word_as_list[index] = guess
            word_completion.set(" ".join(word_as_list))
            if "_" not in word_as_list:
                current_stats["wins"] += 1
                current_stats["streak"] += 1
                if current_stats["streak"] >= current_stats["life time streak"]:
                    current_stats["life time streak"] = current_stats["streak"]

                messagebox.showinfo("Hangman", "Computer guessed the word! You lose!")
                switch_turn()
                return
        update_hangman()
        if current_stats["tries"] == len(hangman_stages) - 1:
            current_stats["losses"] += 1
            messagebox.showinfo("Hangman", f"Computer ran out of tries. The word was {word}. You win!")
            switch_turn()
            return

# Function to switch to computer's turn
def computer_turn():
    global current_stats, word
    current_stats = computer_stats
    while True:
        choice = simpledialog.askstring("Word Selection", "Enter 'random' or 'r' for a random word, or 'choose' or 'c' to enter a word for the computer to guess:").lower()
        current_stats["tries"] = 0
        if choice in ['random', 'r']:
            word = select_word()
            new_round()
            break
        elif choice in ['choose', 'c']:
            while True:
                word = obfuscated_word_entry("Enter a word for the computer to guess:")
                if word.isalpha():
                    break
            new_round()
            break
        else:
            messagebox.showinfo("Invalid Input", "Please enter a valid option.")
    
    # Proceed to the computer's guesses/guessing
    computer_guess()


#player_turn and start_single_player could be combined with an if statement to check which gametype it is.
#would make code shorter, but slower due to the extra check

# Function to switch to player's turn
def player_turn():
    global current_stats, word
    current_stats = player_vs_computer_stats
    word = select_word()
    new_round()

# Start single player game
def single_player():
    global current_stats, word, game_type
    game_type = 'single player'
    current_stats = single_player_stats
    word = select_word()
    new_round()

# Start game against computer
def start_against_computer():
    global game_type
    game_type = 'player vs computer'

    if choose_first_player():
        # User goes first
        player_turn()
    else:
        # Computer goes first
        computer_turn()
    
    game_frame.pack()
    menu_frame.pack_forget()

def first_player_word():
    global word, current_stats
    current_stats = first_player_stats
    while True:
        
        choice = simpledialog.askstring("Word Selection", "Player 2 Enter 'random' or 'r' for a random word, or 'choose' or 'c' to enter a word for Player 1 to guess:", show='*').lower()
        if choice in ['random', 'r']:
            word = select_word()
            break
        elif choice in ['choose', 'c']:
            word = obfuscated_word_entry("Player 2, enter a word for Player 1 to guess:")
            break
        else:
            messagebox.showinfo("Invalid Input", "Please enter a valid option.")
    
    new_round()

def second_player_word():
    global word, current_stats
    current_stats = second_player_stats
    while True:
        choice = simpledialog.askstring("Word Selection", "Player 1 Enter 'random' or 'r' for a random word, or or 'choose' or 'c' to enter a word for Player 2 to guess:", show='*').lower()
        if choice in ['random', 'r']: 
            word = select_word()
            break
        elif choice in ['choose', 'c']:
            word = obfuscated_word_entry("Player 1, enter a word for Player 2 to guess:")
            break
        else:
            messagebox.showinfo("Invalid Input", "Please enter a valid option.")
    
    new_round()

# Function to start a game against another player
def start_against_player():
    global current_stats, game_type, word, guessed_letters
    game_type = 'player vs player'
    if choose_first_player_two():
        first_player_word()
    else:
        second_player_word()



# Initiate/ Reset Stats dictionaries
def Stats():
    global single_player_stats, player_vs_computer_stats, computer_stats, first_player_stats, second_player_stats, current_stats
    single_player_stats = {"name": 'single player', "tries": 0, "wins": 0, "losses": 0, "streak": 0, "rounds": 0, "life time streak" : 0}
    player_vs_computer_stats = {"name": 'player vs computer', "tries": 0, "wins": 0, "losses": 0, "streak": 0, "rounds": 0, "life time streak" : 0}
    computer_stats = {"name": 'computer', "tries": 0, "wins": 0, "losses": 0, "streak": 0, "rounds": 0, "life time streak" : 0}
    first_player_stats = {"name": 'first player', "tries": 0, "wins": 0, "losses": 0, "streak": 0, "rounds": 0, "life time streak" : 0}
    second_player_stats = {"name": 'second player', "tries": 0, "wins": 0, "losses": 0, "streak": 0, "rounds": 0, "life time streak" : 0}

    current_stats = single_player_stats

#make sure the typed entry is only alphabet characters
#can use isalpha() along side is not None
def validate_char(char):
    return re.match(r"^[a-zA-Z]$", char) is not None

def on_validate(P):
    return (len(P) <= 1 and all(validate_char(char) for char in P)) or P == ''

# Button hover and click effects
def on_enter(e):
    e.widget['background'] = '#E6ECEF'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

# Initialize the game
root = tk.Tk()
root.title("Hangman Game")

word = select_word()
word_completion = tk.StringVar(value=" ".join("_ " * len(word)))
guessed_letters = []

# Menu frame
menu_frame = tk.Frame(root)
menu_frame.pack()

single_player_button = tk.Button(menu_frame, text="Single Player", command=single_player,activebackground="#CDD9DF", font=("Courier", 14))
single_player_button.pack(pady=10)
single_player_button.bind("<Enter>", on_enter)
single_player_button.bind("<Leave>", on_leave)

against_computer_button = tk.Button(menu_frame, text="Against Computer", command=start_against_computer,activebackground="#CDD9DF", font=("Courier", 14))
against_computer_button.pack(pady=10)
against_computer_button.bind("<Enter>", on_enter)
against_computer_button.bind("<Leave>", on_leave)

against_player_button = tk.Button(menu_frame, text="Against Player", command=start_against_player,activebackground="#CDD9DF", font=("Courier", 14))
against_player_button.pack(pady=10)
against_player_button.bind("<Enter>", on_enter)
against_player_button.bind("<Leave>", on_leave)

against_player_button = tk.Button(menu_frame, text="Reset ALL Stats", command=Stats,activebackground="#CDD9DF", font=("Courier", 14))
against_player_button.pack(pady=10)
against_player_button.bind("<Enter>", on_enter)
against_player_button.bind("<Leave>", on_leave)



# Game frame
game_frame = tk.Frame(root)

hangman_label = tk.Label(game_frame, text=hangman_stages[0], font=("Courier", 20))
hangman_label.pack(pady=20)

word_completion_label = tk.Label(game_frame, textvariable=word_completion,activebackground="#CDD9DF", font=("Courier", 20))
word_completion_label.pack(pady=20)

vcmd = (root.register(on_validate), '%P')
guess_entry = tk.Entry(game_frame, font=("Courier", 20), validate="key", validatecommand=vcmd)
guess_entry.pack(pady=20)
guess_entry.bind("<Return>", check_guess)

guess_button = tk.Button(game_frame, text="Guess", command=check_guess, activebackground="#CDD9DF", font=("Courier", 14))
guess_button.pack(pady=5)
guess_button.bind("<Enter>", on_enter)
guess_button.bind("<Leave>", on_leave)

menu_button = tk.Button(game_frame, text="Choose New Word", command=choose_new_word,activebackground="#CDD9DF", font=("Courier", 14))
menu_button.pack(pady=5)
menu_button.bind("<Enter>", on_enter)
menu_button.bind("<Leave>", on_leave)

'''
menu_button = tk.Button(game_frame, text="replay", command=replay_round,activebackground="#CDD9DF", font=("Courier", 14))
menu_button.pack(pady=5)
menu_button.bind("<Enter>", on_enter)
menu_button.bind("<Leave>", on_leave)
'''

reset_button = tk.Button(game_frame, text="Reset My Stats", command=reset_stats,activebackground="#CDD9DF", font=("Courier", 14))
reset_button.pack(pady=5)
reset_button.bind("<Enter>", on_enter)
reset_button.bind("<Leave>", on_leave)

abandon_button = tk.Button(game_frame, text="Give Up", command=give_up,activebackground="#CDD9DF", font=("Courier", 14))
abandon_button.pack(pady=5)
abandon_button.bind("<Enter>", on_enter)
abandon_button.bind("<Leave>", on_leave)

menu_button = tk.Button(game_frame, text="End Game", command=end_game,activebackground="#CDD9DF", font=("Courier", 14))
menu_button.pack(pady=5)
menu_button.bind("<Enter>", on_enter)
menu_button.bind("<Leave>", on_leave)

menu_button = tk.Button(game_frame, text="Menu", command=go_back_to_menu,activebackground="#CDD9DF", font=("Courier", 14))
menu_button.pack(pady=5)
menu_button.bind("<Enter>", on_enter)
menu_button.bind("<Leave>", on_leave)

Stats()
root.mainloop()
