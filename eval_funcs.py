from Card import Card
from collections import Counter

def _straight_check_raw(cards_list):

    """
    Inputs: A list of cards. \
    Outputs: A straight if it can be made, otherwise an empty list.

    Note: The straight returned may have more than 5 cards. This is necessary \
        for the straight flush check to work properly.
    """

    # You need at least 5 cards to make a straight
    if len(cards_list) < 5:
        return []
    else:
        # Sort in descending order
        sorted_cards = cards_list.copy()

        # Add a 1 for every ace
        for card in sorted_cards:

            # Vals go from 1 to 13, Aces have value 13
            if card.value == 13:
                sorted_cards.append(Card(0, card.suit))

            # Since the list is sorted in descending order,
            # we can stop when reaching the first non-Ace card
            else:
                break

        n = len(sorted_cards)
        straight_counter = 1
        doubles = 0
        for index, card in enumerate(sorted_cards):

            # If we are too close to the end to make a straight and haven't
            # made a straight yet, return empty list
            if index > n-6 + straight_counter and straight_counter < 5:
                return []

            # If we are at the end of the list, return the straight we have
            elif index == n-1:
                return sorted_cards[index-straight_counter-doubles+1:index+1]

            # Otherwise if the next card is just 1 below, increase straight_counter by 1
            elif sorted_cards[index + 1].value == card.value-1:
                straight_counter += 1

            # If the next card has the same value, we don't want to reset
            # Take into account how many "double" cards we have to know where to slice
            elif sorted_cards[index + 1].value == card.value:
                doubles += 1

            # If the next card is further than 1 away and we already have a straight,
            # return that straight (might be more than 5 cards long)
            elif straight_counter >= 5:
                return sorted_cards[index-straight_counter-doubles+1:index+1]

            # Otherwise try again
            else:
                straight_counter = 1
                doubles = 0

        return sorted_cards

def straight_check(card_list):

    """
    Inputs: A reverse-sorted list of Cards.

    Outputs: The highest straight in the given cards or, if there \
        is no straight, an empty list.
    """

    straight = _straight_check_raw(card_list)
    i = -1
    # Check if we have a straight
    while straight:

        # If the straight ends with an ace, change the value back from
        # the dummy value 0 to actual ace value of 13
        if straight[i].value == 0:
            straight[i].value = 13
            i -= 1 #if we have multiple aces, we don't want to change just the last one
        else:
            break
    return straight

# allows us to check if any number of cards are all of the same suit
def suited(card_list):

    """
    Inputs: A list of cards.
    Outputs: True if all cards have the same suit or list is empty, \
        False otherwise.
    """

    if not card_list:
        return True

    target_suit = card_list[0].suit

    for card in card_list:
        if card.suit != target_suit:
            return False
    return True

def max_suit(card_list):

    """
    Inputs: A list of cards
    Outputs: A pair consisting of the most common suit and how often it appears.
    """

    suits = {"h":0, "c":0, "d":0, "s":0}

    for card in card_list:
        card_suit = card.suit[0] #take just the first letter
        suits[card_suit] += 1   #change corresponding dic value

    max_suit = max(suits, key = suits.get)
    return max_suit, suits[max_suit]

def flush_check(card_list):

    """
    Inputs: A reverse-sorted list of cards.
    Outputs: All cards of the flush suit if there is a flush \
        (meaning there are at least 5 such cards) or an empty list otherwise.

    Note: The fact that more than just the 5 highest cards are returned is \
        important for the straight flush check to work correctly.
    """

    suit_candidate, card_num_of_same_suit = max_suit(card_list)
    if card_num_of_same_suit < 5:
        return []
    else:
        return [card for card in card_list if card.suit[0] == suit_candidate]

def straight_flush_check(straight, flush):

    """
    Inputs: Two lists of cards, the first being a straight, the second a flush.
    Outputs: A straight flush if it exists, an empty list otherwise.

    Note: Both the straight and the flush can have more than 5 cards. The \
        straight flush returned can also have more than 5 cards.
    """

    if not straight or not flush:
        return []

    target_suit = flush[0].suit

    #filter out all wrong suits from the straight, then check if it's still a straight
    return straight_check([card for card in straight if card.suit == target_suit])

def quad_trips_pairs_check(card_list):

    """
    Inputs: A reverse-sorted list of cards.
    Outputs: The best hand among the card_list that is neither a straight, \
        nor a flush, nor a straight flush is returned as a tuple of the form \
        (name, list)

    Note: The hand returned consists of exactly the 5 best cards.
    """

    #card_list = sorted(card_list, reverse = True)

    counting_vals = Counter([card.value for card in card_list])
    #at_least_pair = [val for val in counting_vals.most_common(3) if val[1] > 1]


    # counting_vals[0] is a tuple of the form (card.value, occurances)
    # best is how often the most common value appears
    best = counting_vals[0][1]


    # no pairs, only high card
    if best == 1:
        candidate_hand = card_list
        hand_value = "high card"

    # quads
    elif best == 4:

        quad_val = counting_vals[0][0]
        kicker = counting_vals[1][0]

        # This ensures if we have four Ks and two Aces, we always return \
        # the four Ks and leave out an Ace
        candidate_hand = [card for card in card_list if card.value == quad_val] + \
                         [card for card in card_list if card.value == kicker]
        hand_value = "four of a kind"

    else:

        # first and second are both tuples
        first, second =  counting_vals[0], counting_vals[1]

        # multiply is the two highest occurances multiplied
        multiply = first[1] * second[1]

        # this must be 2*1 or 3*1, so pair or trips
        if multiply == 2 or multiply == 3:

            candidate_hand = [card for card in card_list if card.value == first[0]] + \
                             [card for card in card_list if card.value != first[0]]
            hand_value = "pair" if multiply == 2 else "three of a kind"

        else: #multiply is 2*2 or 3*2, meaning two pair or full house

            # cards with first most common value,
            # cards with second most common value,
            # all other cards in descending order
            candidate_hand = [card for card in card_list if card.value == first[0]] + \
                             [card for card in card_list if card.value == second[0]] + \
                             [card for card in card_list if (card.value != first[0] and card.value != second[0])]
            hand_value = "two pair" if multiply == 4 else "full house"

    return hand_value, candidate_hand[:5]

def evaluate_holdem(card_list):

    """
    Inputs: A list of cards.
    Outputs: The name of the best 5-card hand one can make, as well as a list \
        with the 5 cards.

    Note: This function only works for Hold'em as it makes a key assumptions \
        which is true for 7 cards but not necessarily for 9: If you have \
        a flush, you cannot also have a full house or four of a kind.
    """

    card_list = sorted(card_list, reverse = True)

    flush = flush_check(card_list)
    straight = straight_check(card_list)
    q_t_p_val, q_t_p_hand = quad_trips_pairs_check(card_list)

    if flush:

        if straight:

            straight_flush = straight_flush_check(straight, flush)

            if straight_flush:
                return "straight flush", straight_flush[:5]

        # With 7 cards, you cannot have a flush and also have quads \
        # or a full house. This would not be true in Omaha
        return "flush", flush


    elif q_t_p_val == "four of a kind" or q_t_p_val == "full house" or not straight:
        return q_t_p_val, q_t_p_hand

    # straight
    else:
        return "straight", straight