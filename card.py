from turtle import Turtle

class Card(Turtle):
    # Start an empty list to keep track of which cards have been flipped.
    flipped_cards = []
    # Initiate a status to prevent flipping while resolving a match.
    lock_flip = False

    def __init__(self, x, y, back_image):
        # First of all: card is a turtle object
        super().__init__()
        # Move each card to a specific pos
        self.penup()
        self.goto(x,y)
        # Assign front & back to each card
        self.front_image = "card_back.gif"
        self.back_image = back_image
        # Card back is displayed by default
        self.current_image = self.front_image
        # Display its current image
        self.display_image()
        # Each card is by default not matched yet
        self.matched = False
        
    def display_image(self):
        '''Display the current image of the card.'''
        self.shape(self.current_image)
        
    def flip_image(self, x, y):
        '''Flip the card when it is not matched or locked.'''
        if not self.matched and not self.lock_flip:
            if self.current_image == self.front_image:
                self.current_image = self.back_image
            else:
                self.current_image = self.front_image
        self.display_image()
        # After flipping each time, append to flipped cards 
        if self not in Card.flipped_cards and self.current_image == self.back_image:
            Card.flipped_cards.append(self)
        # Flipped cards are stored for board's retrieval
        return Card.flipped_cards
    
    # Check whether two cards match.
    @classmethod
    def resolve_match(cls): 
        if len(cls.flipped_cards) == 2:
            # Lock flips during resolution
            cls.lock_flip = True
            card1 = cls.flipped_cards[0]
            card2 = cls.flipped_cards[1]

            if card1.back_image == card2.back_image:
                card1.matched = True
                card2.matched = True
                card1.hideturtle()
                card2.hideturtle()
                # Reset list for another match
                cls.flipped_cards.clear()
                # Unlock flips after resolving
                cls.lock_flip = False
                # It is a match
                return True
            else:
                # Flip unmatched cards given a second of reacttion
                card1.screen.ontimer(cls.flip_back_unmatched, 1000)
                # It is not a match
                return False
    
    # Flip back unmatched cards and Reset for another round of resolution.
    @classmethod
    def flip_back_unmatched(cls):
        if len(cls.flipped_cards) == 2:
            card1 = cls.flipped_cards[0]
            card2 = cls.flipped_cards[1]
            card1.current_image = card1.front_image
            card2.current_image = card2.front_image
            card1.display_image()
            card2.display_image()
            # Reset list for another match
            cls.flipped_cards.clear()
            # Unlock flips after reset
            cls.lock_flip = False