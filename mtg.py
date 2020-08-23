import random

from knapsack_solver import zeroOneKnapsack

# You need a card from each group here to win
# A: Untap Creatures, B: 0 mana artifacts, 
# C: win-cons (dmg/tap), D: untap instants, E: card draw, F: Mana
card_groups = ["A", "B", "C", "D", "E", "F"]
win_groups = [card_groups[0], card_groups[1], card_groups[2], card_groups[3]]

class Card:
    def __init__(self, name, cost, groups):
        self.name = name
        self.cost = int(cost)
        self.groups = groups
    def __str__(self):
        return self.name + "(" + str(self.groups) + ")"
    def __repr__(self):
        return self.name + "(" + str(self.groups) + ")"

def build_deck():
    deck_file = open("deck_list.txt", "r")
    deck_to_build = []
    line = deck_file.readline().rstrip('\n')
    while(line):
        line_parts = line.split(",")
        num_cards = line_parts[0]
        card_name = line_parts[1]
        card_cost = line_parts[2]
        card_groups = line_parts[3].split("|")

        card_to_add = Card(card_name, card_cost, card_groups)
        for i in range(int(num_cards)):
            deck_to_build.append(card_to_add)
        line = deck_file.readline().rstrip('\n')
    return deck_to_build

def draw_single(deck):
    deck_size = len(deck)
    n = random.randint(0, deck_size - 1)
    card = deck[n]
    # Remove card from deck
    del deck[n]
    return card

def draw_multiple(num_cards, deck):
    if(num_cards):
        cards = []
        for i in range(num_cards):
            card_to_add = draw_single(deck)
            if(card_to_add):
                cards.append(card_to_add)
        return cards

# Check if player holds the winning cards
def did_win(board_cards):
    seen_groups = []
    for card in board_cards:
        did_use_card = False
        for group in card.groups:
            if not group in seen_groups and group in win_groups and not did_use_card:
                seen_groups.append(group)
                did_use_card = True
    return len(seen_groups) >= len(win_groups)


def card_in_win_group(card):
    is_win_group = False
    for group in card.groups:
        if group in win_groups:
            is_win_group = True
    return is_win_group

# Check if the card's group is already represented on the board
def card_group_present_on_board(in_card, board):
    board_groups = []
    for card in board:
        for group in card.groups:
            if group not in board_groups:
                board_groups.append(group)

    is_present = False
    for group in in_card.groups:
        if group in board_groups:
            is_present = True
    return is_present

def get_optimal_mana_spend(hand, num_mana, board_cards):
    # Ignore playing lands for optimal mana spend, or cards that are in a group we already have on board
    hand_to_use = list(filter(lambda card: (card_in_win_group(card) and not card_group_present_on_board(card, board_cards)), hand))
    if(len(hand_to_use) == 0):
        return []
    card_values = list(map(lambda card: (1), hand_to_use))
    card_costs = list(map(lambda card: (card.cost), hand_to_use))
    res = zeroOneKnapsack(card_values, card_costs, num_mana)
 
    selected_cards = []
    for i in range(len(res[1]) - 1):
        if(res[1][i] != 0):
            selected_cards.append(hand_to_use[i])
    return selected_cards

def play_game():
    num_turns = 0
    has_won = False
    board_mana = []
    board_cards = []

    # Randomly select whether the player starts or not
    will_start = random.randint(0, 1)

    # Build deck from text file
    deck = build_deck()
    # Draw starting hand
    hand = draw_multiple(7, deck)

    # Play until we win or run out of cards
    while(not has_won and len(deck) > 0):
        # Draw card to hand
        if(not (will_start and num_turns == 0)):
            hand.append(draw_single(deck))
        has_played_mana = False
        for card in hand:
            # Play mana
            if "F" in card.groups and not has_played_mana:
                board_mana.append(card)
                hand.remove(card)
                has_played_mana = True
        
        # Spend Mana optimally for card cost
        cards_to_play = get_optimal_mana_spend(hand, len(board_mana), board_cards)
        # Remove cards from hand
        for card in cards_to_play:
            hand.remove(card)
        # Add to board
        board_cards += cards_to_play
        has_won = did_win(board_cards)
        num_turns += 1
        if(has_won):
            ""
            #print(f"Won a game after {num_turns} turns! Board state at win: ", board_cards)
    return (has_won, num_turns)

def main():
    # Number of games to play
    num_games = 1000
    results = []

    for n in range(num_games):
        # Play the actual games
        results.append(play_game())

    # Print Statistics
    won_games = 0
    lost_games = 0
    turn_wins = []
    for (result, num_turns) in results:
        if(result):
            won_games += 1
            turn_wins.append(num_turns)
        else:
            lost_games += 1
    if(won_games <= 0):
        print("Won 0 games...")
    else:
        win_percentage = round(won_games / (won_games + lost_games) * 100, 2)
        avg_turns_to_win = round(sum(turn_wins) / len(turn_wins), 2)
        print(f"\nWon {win_percentage}% of {num_games} games. Avg. win by turn: {avg_turns_to_win}")

if __name__ == "__main__":
    main()

    