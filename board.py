from turtle import Turtle, Screen
from card import Card

class Board():
    def __init__(self, name):
        # Class Board inherits all method of Turtle & Screen
        self.screen = Screen()
        self.turtle=Turtle()
        # Initiate basic layout of the screen
        self.screen.screensize(canvwidth=600, canvheight=600)
        self.screen.title("CS 5001 Memory Game")
        # Register images for later use
        self.default_shapes = ["quitbutton.gif", "quitmsg.gif", "card_back.gif", "winner.gif", "leaderboard_error.gif"]
        self.register_default_shape()
        # Initiate a status turtle as the attribute of each board
        self.status_score = Turtle()
        self.status_score.color("black")
        # Hide the status score unless called to update
        self.status_score.hideturtle()
        self.guesses = 0
        self.matches = 0
        # Initiate a leader turtle as the attribute of each board
        self.name = name
        # Initiate an empty list to track how many cards are placed
        self.cards = []
    
    def register_default_shape(self):
        '''Register shapes for later use.'''
        for shape in self.default_shapes:
            self.screen.register_shape(shape)

    def draw_frame(self):
        '''Draws the basic layout of the board'''
        frame = self.turtle
        frame.width(5)
        frame.penup()
        # draw frame of main board
        frame.teleport(-325, 300)
        frame.pendown()
        self.direct_frame(frame, 450, 500)
        frame.penup()
        # draw frame of status board
        frame.teleport(-325, -240)
        frame.pendown()
        self.direct_frame(frame, 450, 50)
        frame.penup()
        # draw frame of leader board
        frame.teleport(165, 300)
        frame.color('blue')
        frame.pendown()
        self.direct_frame(frame, 150, 500)

        frame.hideturtle()

    # Used only when draw a rectangle frame
    @staticmethod
    def direct_frame(turt, x, y):
        turt.forward(x)
        turt.right(90)
        turt.forward(y)
        turt.right(90)
        turt.forward(x)
        turt.right(90)
        turt.forward(y)
        turt.right(90)

    # Write text with default font & style
    @staticmethod
    def write_text(turt, txt):
        turt.write(txt, align="left", font=("Arial", 20, "normal"))

    def read_record(self):
        '''Read the historical records from file'''
        records = []
        try: 
            with open("leader_board.txt", 'r') as infile:
                lines = infile.readlines()
                for line in lines:
                    cols = line.strip().split()
                    name = cols[0]
                    guesses = int(cols[1])
                    records.append([name, guesses])
        except: 
            leader_board = Turtle()
            leader_board.shape("leaderboard_error.gif")
            leader_board.showturtle()
            self.screen.ontimer(leader_board.hideturtle, 2000) 
            
        return records
    
    def draw_leader_board(self):
        '''Display leader board & rankd current leaders'''
        leader = self.turtle
        leader.hideturtle()
        leader.color("blue")
        leader.teleport(180, 265)
        self.write_text(leader, "Leaders:")
        # Read historical records
        records = self.read_record()
        # Sort records by descending orders
        ranked_records = sorted(records, key=lambda x: x[1])
        # Display the top 8 players
        for i in range(len(ranked_records[:8])): 
            record = ranked_records[i]
            name=record[0]
            guesses = record[1]
            leader.teleport(180, 215 - i * 50)
            self.write_text(leader, f'{guesses} : {name}')
    
    def draw_status_board(self):
        '''Display status board'''
        self.status_score.teleport(-310, -270)
        self.update_status()

    def update_status(self):
        '''Update score & display in the status board'''
        # Clear out the current score before writing the new one! 
        self.status_score.clear()
        self.write_text(self.status_score, f"Status: {self.guesses} Guesses, {self.matches} Matches")
    
    def add_quit_button(self):
        '''Display a quit button'''
        quit_button = Turtle()
        quit_button.teleport(210, -275)
        quit_button.shape("quitbutton.gif")
        quit_button.showturtle()
        # Quit the game when quit button is clicked on
        quit_button.onclick(self.quit_game)

    def quit_game(self, x, y):
        '''Close the game & display message'''
        quit_msg = Turtle()
        quit_msg.hideturtle()
        quit_msg.shape("quitmsg.gif")
        quit_msg.showturtle()
        self.screen.ontimer(self.screen.bye, 3000)
    
    def prepare_images(self, files):
        '''Register each image from the config file(list)'''
        registered_images = []
        for file in files:
            try: 
                self.screen.register_shape(file) 
                registered_images.append(file)
            except Exception as e:
                print(f"Error registering shape{file}: {e}")
        return registered_images
    
    def setup_card(self, images, num_cards):
        '''Set up cards in proper positions.'''
        start_x, start_y = -250, 210
        gap_x, gap_y = 100, 160

        for i in range(num_cards):
            row = i // 4
            col = i % 4 
            x = start_x + col * gap_x
            y = start_y - row * gap_y
            # Assign a unique back image to each card
            back_image = images[i]
            card = Card(x, y, back_image)
            # Need to keep track of each card for click actions
            self.cards.append(card)

    def handle_clicks(self, x, y):
        '''Handle clicks on the board.'''
        # Ignore clicks when resolving matches
        if Card.lock_flip:
            return
        for card in self.cards:
            if card.distance(x,y) < 50 and not card.matched:
                flipped_cards = card.flip_image(x,y)
                if len(flipped_cards) == 2:
                    self.guesses += 1
                    self.update_match()
                    self.update_status()

                if self.judge_win():
                    self.display_win()
                    self.save_record()
    
    def update_match(self):
        '''Update matching only when two cards are matched.'''
        if Card.resolve_match():
            self.matches += 1
            self.update_status()

    def judge_win(self):
        '''Decide the condition for winning.'''
        if self.matches == len(self.cards) // 2:
            return True
        return False
            
    def display_win(self):
        '''Display the winning message and exit the game.'''
        win_msg=Turtle()
        win_msg.shape("winner.gif")
        win_msg.showturtle()
        self.screen.ontimer(self.screen.bye, 3000)

    def save_record(self):
        '''Append the current players' record to the record file.'''
        with open("leader_board.txt", 'a+') as outfile:
            outfile.write(f'{self.name} {self.guesses}\n')