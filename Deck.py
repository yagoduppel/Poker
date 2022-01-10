import random
from Card import Card

class Deck(list):

    def __init__(self, complete = True, *args, **kwargs):

        self.suits = ["hearts", "diamonds", "spades", "clubs"]
        self.vals = list(range(1,14))
        self.fill_up()


    def shuffle(self):

        """
        Shuffles the deck in-place.
        """

        random.shuffle(self)

    def draw(self, num: int = 1):

        """
        Returns a list with num many cards. Raises an IndexError if more cards \
        are to be drawn than are left in the deck or if fewer than 1 card is to \
        be drawn. Default number of cards is 1. The method returns a list even \
        if there is only one card in it.
        """

        if num > len(self):
            raise IndexError(
                f"There are only {len(self)} cards left in the deck, you cannot draw {num} {'cards' if num != 1 else 'card'}.")
        if num < 1:
            raise IndexError(
                "You cannot draw less than 1 card.")
        if num == 1:
            return [self.pop()]


        cards_drawn = []

        for i in range(num):
            cards_drawn.append(self.pop())
        return cards_drawn

    def fill_up(self):

        assert(len(self) == 0)

        for suit in self.suits:
            for val in self.vals:
                self.append(Card(val, suit))
