import numpy as np
import matplotlib.pyplot as plt
import mplcursors

from random import randint
from random import shuffle

# TO DO ------------------------------------
# "get out of jail free" card needs to be implemented
# go to jail doesn't put you in jail
# Jail system?
# ------------------------------------------


square_names = ["Go", "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax",
                "Reading Railroad", "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue",
                "Jail", "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue",
                "Pennsylvania Railroad", "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue",
                "Free Parking", "Kentucky Avenue", "Chance", "Indiana Avenue", "Illinois Avenue", "B&O Railroad",
                "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go to jail",
                "Pacific Avenue", "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue",
                "Short Line", "Chance", "Park Place", "Luxury Tax", "Boardwalk"]


# Helper function to find the nearest railroad based of the current player postition
def nearest_railroad(position):
    if position >= 25:
        return 5
    elif position >= 15:
        return 25
    elif position >= 5:
        return 15
    else:
        return 5

# Helper to find the nearest utility based off current player position
def nearest_utility(position):
    if position >= 28:
        return 12
    elif position >= 12:
        return 28
    else:
        return 12

# moves the players position based off the card they pull from chance or community chest deck.
def apply_card(position, card):
    if -1 < card < 40:
        return card
    elif card == 40:
        return nearest_railroad(position)
    elif card == 41:
        return nearest_utility(position)
    elif card == 42:
        return position - 3


# For chance and community cards, numbers represent the following...
# -1 --> a card that does nothing
# 0 through 39 --> player is moved to that position on the board
# 40 --> player is moved to the nearest railroad
# 41 --> player is moved to the nearest utility
# 42 --> player is moved back 3 spaces


chance = [39, 0, 24, 11, 40, 40, 41, -1,
          -1, 42, 10, -1, -1, 5, -1, -1]

community = [0, -1, -1, -1, -1, 10, -1, -1,
             -1, -1, -1, -1, -1, -1, -1, -1]

# Creates a list of board squares numbered 0-39 all starting at a count of 0
# landing on each spot will increment the counter
position_counter = [0] * 40


num_games = 100000
num_players = 4
num_of_turns = 30

# used for calculating percentages at the end of the simulation
total_landings = num_games * num_players * num_of_turns

for i in range(num_games):

    # for each game, make a list of player positions starting at 0
    player_positions = [0] * num_players

    # shuffle both decks
    shuffle(chance)
    shuffle(community)

    for j in range(num_of_turns):
        for x in range(num_players):

            roll = randint(1, 6)
            player_positions[x] = (player_positions[x] + roll) % 40
            position_counter[player_positions[x]] += 1

            # if player lands on community chest
            if player_positions[x] == 2 or player_positions[x] == 17 or player_positions[x] == 33:
                card = community[0]
                community.pop(0)
                community.append(card)

                if card != -1:
                    player_positions[x] = apply_card(player_positions[x], card)
                    position_counter[player_positions[x]] += 1
                    total_landings += 1

            # if player lands on "chance"
            elif player_positions[x] == 7 or player_positions[x] == 22 or player_positions[x] == 36:
                card = chance[0]
                chance.pop(0)
                chance.append(card)

                if card != -1:
                    player_positions[x] = apply_card(player_positions[x], card)
                    position_counter[player_positions[x]] += 1
                    total_landings += 1

            # if player lands on "Go to jail"
            elif player_positions[x] == 30:
                player_positions[x] = 10
                position_counter[player_positions[x]] += 1
                total_landings += 1

# calculates total percentage of times a spot was landed on
scaled_counter = [ x / total_landings for x in position_counter]



#Plotting our data with matplotlib

plt.rcdefaults()
fig, ax = plt.subplots()

y_pos = np.arange(len(square_names))

ax.barh(y_pos, scaled_counter)
ax.set_yticks(y_pos, labels=square_names)

# giving each horizontal bar its percentage value
for index, value in enumerate(scaled_counter):
    plt.text(value, index,
             (str('%.4f' % (value*100))) + "%" )

ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('% of time landed on')
ax.set_title('Monopoly simulation')

plt.show()

