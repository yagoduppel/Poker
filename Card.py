class Card:

    def __init__(self, value:int, suit:str):

        """
        Initiates a Card object with a given value and suit. Card objects can
        be compared to one another. The comparisons only check the value, not
        the suit, meaning 6h == 6d will evaluate to True.
        """

        self.value = value
        self.suit = suit

        self.repr_list = [str(x) for x in range(2,10)] + ["T", "J", "Q", "K", "A"]


    def __repr__(self):
        return self.repr_list[self.value-1] + self.suit[0]

    # Comparisons only check the value, not the suit
    def __eq__(self, other):
        return self.value == other.value
    def __ne__(self, other):
        return self.value != other.value
    def __lt__(self, other):
        return self.value < other.value
    def __le__(self, other):
        return self.value <= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __ge__(self, other):
        return self.value >= other.value
