from turtle import Turtle, Screen, numinput
import random
import time
from board import Board

class Game():
    def __init__(self):
        self.screen = Screen()
        self.board = None
        self.name = ''
        self.config = ''
        self.num = 0

    def get_name(self):
        '''Prompt the player to imput his/her name'''
        name = self.screen.textinput("CS 5001 Memory", "Please enter your name:")
        # Make sure the player must input something
        while name == '':
            self.screen.update()
            new_name = self.screen.textinput("CS 5001 Memory", "Please enter your name:")
            name = new_name
        self.screen.clear()
        self.name = name

    def choose_carddeck(self):
        '''Prompt the player to choose a card deck to play (between pokers & dogs)'''
        self.screen.register_shape("file_error.gif")
        chosen_deck = self.screen.textinput("Choose a card deck", "Poker(p) or Dog(d)")
        if chosen_deck.lower() == 'p' or chosen_deck == 'poker' or chosen_deck == 'pokers':
            self.config = 'config_poker.txt'
        elif chosen_deck.lower() == 'd' or chosen_deck == 'dog' or chosen_deck == 'dogs':
            self.config = 'config_dog.txt'
        else:
            config_error = Turtle()
            config_error.teleport(0,0)
            config_error.shape("file_error.gif")
            config_error.showturtle()
            self.screen.ontimer(config_error.hideturtle, 2000)
            self.config = 'config_poker.txt'
            # Make sure the screen will stay to display the error message
            time.sleep(2)
        # Update the screen
        self.screen.update()
    
    def get_num(self): 
        '''# Prmopt the player to input how many cards they wanna play with'''
        self.screen.register_shape("card_warning.gif")
        # Specify the max & min values to 
        num = int(numinput("Set Up", "# of Cards to Play: (8, 10, or 12)", None, 8, 12))
        if num % 2 != 0:
            odd_warning = Turtle()
            odd_warning.shape("card_warning.gif")
            odd_warning.showturtle()
            # Wait for 2 seconds before hiding the message
            self.screen.ontimer(odd_warning.hideturtle, 2000)
            num += 1
            # Make sure the screen will stay to display the error message
            time.sleep(2)
        # Update the screen
        self.screen.update()
        self.num = num
    
    def read_file(self, dir_file):
        '''# Choose a card deck and ind all files in the config file'''
        with open(dir_file, 'r') as infile:
            files = list(line.strip() for line in infile if line.strip())
        return files

    def randomize_images(self, img_lst, n): 
        '''Randomize images for the card placement'''
        image_num = n // 2
        if image_num > len(img_lst):
            raise ValueError("Not enough images to display!")
        # Randomly select half of unique images from the list
        selected_images = random.sample(img_lst, image_num) #needs to revise
        # Create an array ranging from 1 to total counts & shuffle
        all_images = selected_images * 2
        random.shuffle(all_images)
        return all_images
    
    def setup_board(self):
        '''Set up the board for playing'''
        # Instantiate the board
        self.board = Board(self.name)
        # Draw out the basic layout
        self.board.draw_frame()
        self.board.draw_status_board()
        self.board.draw_leader_board()
        self.board.add_quit_button()

    def play_game(self):
        'Play the memory matching game'
        # Prompt the user to input name
        self.get_name()
        # Prompt the user to choose which card deck to play
        self.choose_carddeck()
        # Prompt the user to choose number of cards
        self.get_num()
        # Set up the board
        self.setup_board()
        # Read config file & randomize images
        files = self.read_file(self.config)
        images = self.board.prepare_images(files) 
        # Create a list that containing 2 copies of the exact same card
        card_shuffled = self.randomize_images(images, self.num) 
        self.board.setup_card(card_shuffled, self.num)
        # Start playing game (Enable user action)
        self.board.screen.onclick(self.board.handle_clicks)
        self.board.screen.mainloop()