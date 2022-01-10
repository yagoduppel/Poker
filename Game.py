from operator import attrgetter

from Deck import Deck
from eval_funcs import evaluate_holdem
from Player import Player
from UI import UI

class Game:

    def __init__(self, players = 6, *args, **kwargs):

        """
        Initiates the Game object with as many players as given by \
        the parameter players (default is 6). The player objects are stored \
        in self.players and then a new hand is dealt.
        """

        #See if the player names were given, else use numbers
        player_names = kwargs.get("player_names", list(range(players)))


        #The players still in the game
        self.players = [Player(self,
                               position = i,
                               player_name = player_names[i]) for i in range(players)]
        self.players_num = players
        self.winner = None

        #Player position whose turn it is, not to be confused with the Turn
        self.turn: int
        self.board = []
        self.deck = Deck()
        print([x.value for x in self.deck])

        #Other possible args and kwargs, idk bro, might need it later
        self.args = args
        self.kwargs = kwargs

        #Position names
        self.position_dic = {0:"SB", 1:"BB", len(self.players)-1:"D"}
        #Betting round names
        self.betting_rounds = ["Preflop", "Flop", "Turn", "River"]

        self.hand_strength = {"high card" : 1,
                              "pair" : 2,
                              "two pair" : 3,
                              "three of a kind" : 4,
                              "straight" : 5,
                              "flush" : 6,
                              "full house" : 7,
                              "four of a kind" : 8,
                              "straight flush" : 9}

        #Blinds and ante
        self.blinds = kwargs.get("blinds", [1,2])
        self.ante = kwargs.get("ante", 0)

        ui = UI(self)


        #Announce the winner
        print(f'The winner is {self.players[0].name}! Congratulations!')


    def __repr__(self):
        return f"There are {len(self.players)} players left. The chip leader is {self.chip_leader}."

    def update(self):

        """
        Calls all the update functions after a hand as ended.
        """
        self.update_deck()
        self.update_players()
        self.update_chip_leader()
        self.update_board()

    def update_players(self):

        """
        This method eliminates any players from self.players who have \
            no chips left and resets if they have folded that hand
        """

        self.move_positions()
        self.players = [player for player in self.players if player.chips > 0]
        self.players_num = len(self.players)
        self.winner = None
        for player in self.players:
            player.folded = False
            player.all_in = False

    def update_chip_leader(self):

        """
        Updates who the chip leader is.
        """

        self.chip_leader = max(self.players, key=attrgetter('chips'))

    def update_deck(self):

        """
        Adds the cards given to players and on \
        the board back to the deck, then shuffles
        """
        for player in self.players:
            self.deck += player.hole_cards
        self.deck += self.board
        self.deck.shuffle()

    def update_board(self, new_cards = None, print_cards = True):

        """
        Updates the bets, pot and community cards.
        """

        if new_cards is None:
            self.pot = 0
            self.board = []
        else:
            self.board += new_cards
            if print_cards == True:
                print(f"Dealt to the board: {new_cards}")

    def update_pot(self):

        """
        Adds the bets to the pot and resets the bets in the Game object \
        (not in the Player objects). Should be called at the end of every \
        betting round.
        """

        self.pot += sum(self.bets)
        self.bets = [0]*self.players_num

    def sort_by_position(self):

        """
        Sorts the list of players by their position.
        """

        self.players.sort(key = lambda player: player.position)

    def get_player_by_position(self, position = 0):

        """
        Returns the player sitting in the position given by the argument
        (default is 0). Assumes the list is sorted
        """

        return self.players[position]

    def evaluate(self, card_list):
        return evaluate_holdem(card_list)

    def move_positions(self):
        for player in self.players:
            player.position = (player.position + 1) % self.players_num
        SB = self.players.pop(0)
        self.players.append(SB)

    def new_hand(self, cards_per_player = 2, **kwargs):

        """
        This method should be called at the start of every hand.
        It rebuilds the deck and shuffles it, then gives every player as many
        cards as given by the parameter "cards_per_player" (default is 2).
        The hole cards of each player are saved in the Player objects, not as
        part of the Game class.
        """

        self.sort_by_position()
        self.players_in_it = list(range(self.players_num))
        self.bets = [0]*self.players_num

        for player in self.players:
            player.hole_cards = sorted(self.deck.draw(cards_per_player),
                                       reverse = True)

        #Preflop Betting
        self.betting_round(preflop = True, **kwargs)

        #Other betting rounds
        i = 0
        while self.winner is None and i < 3:

            #returns 3 for i = 0 and returns 1 for i = 1 or 2
            card_num = i**2-3*i+3
            self.update_board(self.deck.draw(card_num))
            self.betting_round(**kwargs)
            i += 1

        #Update the state of the game once the hand ends
        self.update()

    def betting_round(self, preflop = False, **kwargs):

        """
        Starts a new betting round. If preflop is True, the players in the
        blinds are forced to bet the blinds.
        """

        verbose = kwargs.get("verbose", False)

        #The person we have to get back to without raises
        #or new bets for the betting round to end
        self.last_to_bet = 2 if preflop else 0
        self.turn = self.last_to_bet
        complete_round_counter = 0

        continuation_actions = set(["r", "b", "c"])

        if preflop:

            #Everyone places the ante
            if self.ante > 0:
                for player in self.players:
                    player.place_bet(self.ante)

            #Blinds are placed
            self.get_player_by_position(0).place_bet(self.blinds[0])
            self.get_player_by_position(1).place_bet(self.blinds[1])
            self.turn = 2


        #Betting continues until we reach whoever was last to bet/raise
        #except if there are only limps preflop, then until we reach UTG again
        while True:

            #If only one person is left, the game ends
            if self.players_num == 1:
                break

            player = self.players[self.turn]

            #If we have reached the last person to have bet, quit out of
            #the while loop, except if we haven't gone around once yet
            if player.position == self.last_to_bet:
                if complete_round_counter != 0:
                    if verbose:
                        print(f"We have now reached {player.name} who was the last to bet/raise.")
                    break
                else:
                    complete_round_counter += 1


            #If they have folded or is all-in, move on to the next player
            if player.folded:
                self.turn = (self.turn + 1)%self.players_num
                if verbose:
                    print(f"{player.name} has folded already. Moving on...")
                continue
            elif player.all_in:
                self.turn = (self.turn + 1)%self.players_num
                if verbose:
                    print(f"{player.name} has already gone All-in. Moving on...")
                continue

            #Get the player's decision on how to play
            decision = player.get_decision(verbose = verbose)

            #Raise, Bet, Call or even Check
            if decision[0] in continuation_actions:
                player.place_bet(decision[1])

                #If the player bets or raises, update who is last to act
                if decision[0] == "r" or decision[0] == "b":
                    self.last_to_bet = self.turn
                    if verbose:
                        print(f"{player.name} is the last person to have bet.")
            #Fold
            else:
                self.players_in_it.remove(self.turn)


            self.turn = (self.turn + 1)%self.players_num

        self.update_pot()
        for player in self.players:
            player.bet = 0

        #Check if we already have a winner
        if len(self.players_in_it) == 1:
            self.winner = self.players[self.players_in_it[0]]
            self.winner.chips += self.pot
            print(f"{self.winner.name} wins the pot of {self.pot} chips.")











