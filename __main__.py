#from Card import Card
from Game import Game


def same_value(*cards):
    val = cards[0].value
    for card in cards:
        if card.value != val:
            return False
    return True

if __name__ == "__main__":

    player_names = ["Anna", "Bob", "Chiara", "Dylan", "Emilia", "Fabian"]
    game = Game(player_names = player_names)
    #ui = UI(game)











