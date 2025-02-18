import eval7, pprint
deck = eval7.Deck()

# hand = deck.draw(2)
# board = deck.draw(5)
# opp_hr = eval7.HandRange("22+,A2s+")

# eval7.py_hand_vs_range_exact(hand, opp_hr, board)
# eval7.HandRange("AA")

# 50 in pot, we have 9s6h and 125 sb, villain has 250 BB, we are first to act
# effectively: pot = 50 + 125 + 250 = 425
# we need to call 125 to win 425
# pot odds 125 / 425 = 0.294
# stacks are 3250 for us, 825 villain
stack = 3250
villain_stack = 825
hand = [eval7.Card("9s"), eval7.Card("6h")]
pot = 425

sb = 125
bb = 250
ante = 25
players = 2
M = min(stack, villain_stack) / (sb + bb + ante * players)

# semi-bluffing equation: EV = fold% * pot + (1 - fold%) * (win% * pot + (1 - win%) * -call_cost)
# suppose we go all in for his stack amount plus the bb-sb. What are his pot odds?

raise_cost = villain_stack
new_pot = pot + villain_stack
call_cost = villain_stack
pot_odds = call_cost / (new_pot + call_cost)
print(f"Pot: {pot}, call cost: {call_cost}, Pot odds: {pot_odds}")

# so in theory, our villain needs 40% equity to call
# but the fact that we raised preflop means we have a stronger range.
# For now: say our opponent will call with 22+, A2+, JT+

call_range = eval7.HandRange("22+,A2+,JT,QT,KT,QJ,KJ,KQ")
equity = eval7.py_hand_vs_range_exact(hand, call_range, [])

print(f"Our Call Equity: {equity}")

# fold equity now. he calls with anything in this range, so he folds with anything else. what percentage of possible hands are in his range?

fold_prob = 1 - (len(call_range) / 1326)
print(f"Fold Probability: {fold_prob}")

# now, what is our EV for this raise?
print(f"Semi bluff equation: ({fold_prob}) * {pot} + (1 - {fold_prob}) * ({equity} * {new_pot} + (1 - {equity}) * -{call_cost})")
EV = fold_prob * pot + (1 - fold_prob) * (equity * (pot + call_cost) - (1-equity) * raise_cost)
print(f"EV: {EV}")

def above_x_percent_range(x):
    # for every possible preflop hand, calculate the equity against a random hand. Return all hands with equity at least X percent
    deck = eval7.Deck()
    hands = []
    for i in range(len(deck.cards)):
        for j in range(i+1, len(deck.cards)):
            hand = [deck.cards[i], deck.cards[j]]
            equity = eval7.py_hand_vs_range_exact(hand, eval7.HandRange("random"), [])
            if equity >= x:
                hands.append(hand)
            
eval7.py_all_hands_vs_range()

