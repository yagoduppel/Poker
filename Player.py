#from main import Game

class Player:

    def __init__(self,
                 game,
                 chips:int = 1_000,
                 position:int = 0,
                 player_name = 0,
                 *args, **kwargs):
        """
        Initiates a Player object with the chip number and position being
        given by the parameters (defaults are 1_000 chips and position 0).
        Once dealt, the hole cards are stored in self.hole_cards.
        """
        self.chips = chips
        self.hole_cards = []
        self.position = position
        self.bet = 0
        self.all_in = False
        self.name = player_name
        self.folded = False
        self.game = game

        #the actions the player can make
        self.allowed_actions_no_bets =      ("Fold", "Check", "Bet")
        self.allowed_actions_previous_bet = ("Fold", "Call", "Raise")

    def __repr__(self):
        return f"Player {self.name} with {self.chips} chips."

    def place_bet(self, betsize:int = 0):

        #Going All-in
        if betsize >= self.chips:
            betsize = self.chips
            self.all_in = True
            self.game.players_in_it.remove(self.position)

        self.bet += betsize
        self.chips -= betsize
        self.game.bets[self.position] = self.bet

    def get_decision(self, verbose = False):
        bets = self.game.bets
        size_to_call = max(bets)-self.bet
        actions = self.get_allowed_actions(size_to_call)


        while True:
            if verbose:
                decision = input(
f"""Hello {self.name}. Your hand is {self.hole_cards}.You can choose to \
{actions[0]}, {actions[1]} or {actions[2]}. Type f to {actions[0]}, c to \
{actions[1]} {'for another '+ str(size_to_call) + ' chips' if actions[1] == "Call" else ''}, \
or type {actions[2][0].lower()} and a number to {actions[2]} to that amount of chips.\n""")
            else:
                decision = input(
f"""{self.name}: {self.hole_cards}
Options: {actions[0]}, {actions[1]}\
{" " + str(size_to_call) if actions[1] == "Call" else ''}, \
{actions[2]}\n """)

            #if this is true, we are talking about a bet or a raise
            if contains_Number(decision):

                #first attempt to split the input
                #this works for strings like "r 500"
                try:
                    decision_new = decision.split(" ")
                    raise_amount = int(decision_new[1])
                except IndexError:

                    #second attempt to split the input
                    #this works for strings like "r, 500"
                    try:
                        decision_new = decision.split(",")
                        raise_amount = int(decision_new[1])
                    except IndexError:
                        print("I do not understand what you are saying. Please try again.")
                        continue

                #If we raise, it must be to more than the current largest bet
                if raise_amount-self.bet <= size_to_call:
                    print(f"You must raise to at least {max(bets)+self.blinds[1]}!")

                #We cannot bet more than we have
                elif raise_amount > self.bet + self.chips:
                    print(f"You only have {self.chips} chips left! You can go all-in to make it {self.chips + self.bet} in total.")

                #If the above 2 checks are passed, we are ready to raise or bet
                elif decision_new[0][0].lower() == actions[2][0].lower():
                    print(f"{self.name} {actions[2].lower()}s to {raise_amount}.")
                    return (decision_new[0].strip()[0].lower(), raise_amount)
                else:
                    print("I do not understand what you are saying. Please try again.")



            #folding
            elif decision[0].lower() == "f":
                print(f"{self.name} folds.")
                self.folded = True
                return ("f",0)
            #calling or checking
            elif decision[0].lower() == "c":
                print(f"{self.name} {actions[1].lower()}s.")
                return ("c",size_to_call)



    def get_allowed_actions(self,
                        size_to_call = 0):
        """
        Returns the saved tuple of allowed actions depending on whether a bet \
        has been placed.
        """
        return self.allowed_actions_no_bets if size_to_call == 0 else self.allowed_actions_previous_bet



def contains_Number(string:str):

    """
    Returns True if the string contains a number, False otherwise
    """

    for char in string:
        if char.isdigit():
            return True
    return False