from random import choice
from math import ceil

# Calculate Legacy stuff
legacy_players = ["Aris", "nix", "Jason", "Gaelan"]
winner = choice(legacy_players)
legacy_players.remove(winner)
runner_ups = ", ".join(legacy_players)

# Calculate Econ stuff
boatloads = 1.1
econ_pot = 50 * boatloads
econ_players = 5
econ_split = int(ceil(econ_pot / econ_players))

# The map
mapping = {'winner': winner, 'runner_ups': runner_ups, 
           'econ_players': econ_players, 'econ_split': econ_split}

# Apply the map we built above to the template.
with open('template.txt', 'r') as infile:
    template = infile.read()
    
with open('report.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))
