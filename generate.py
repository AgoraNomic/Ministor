from random import choice
from math import ceil

# Calculate Legacy stuff
legacy_players = ["Aris", "Jason", "Gaelan", "ATMunn"]
winner = choice(legacy_players)
legacy_players.remove(winner)
runner_ups = ", ".join(legacy_players)

# Calculate Econ stuff
boatloads = 2.38
econ_pot = 51 * boatloads
econ_players = 5
econ_split = int(ceil(econ_pot / econ_players))

# The map
mapping = {'winner': winner, 'runner_ups': runner_ups, 
           'econ_players': econ_players, 'econ_split': econ_split,
           'econ_pot': round(econ_pot,2)}

# Apply the map we built above to the template.
with open('template.txt', 'r') as infile:
    template = infile.read()
    
with open('report.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))
