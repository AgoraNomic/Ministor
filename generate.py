from random import choice
from math import ceil
from csv import reader

# Import focuses
focuses = {}

focus_lists = {"Unfocused": [], "Legacy": [], "Participation": [], "Compliance": [], "Economy": [], "Legislation": []}

with open('focuses.txt', 'r') as infile:
    infocuses = reader(infile, delimiter=',', quotechar="\"")
    for row in infocuses:
        focuses[row[0]] = row[1]
        focus_lists[row[1]].append(row[0])
        
# Build focus list
focus_table = ""

#for key in focus_lists:
    #focus_table += "\n"
    #focus_table += (key + " (" + str(len(focus_lists[key])) + "): " + ", ".join(focus_lists[key]) + "\n")

for key in sorted(focuses.keys()):
    focus_table += key + ": " + focuses[key] + "\n"

# Calculate Legacy stuff
legacy_players = focus_lists["Legacy"]

if len(legacy_players)==0:
    winner = "no one, as there are no legacy focused players"
    runner_ups = "no one"
else:
    winner = choice(legacy_players)
    legacy_players.remove(winner)
    
runner_ups = ", ".join(legacy_players)

# Calculate Econ stuff
boatloads = 2.38
econ_pot = 50 * boatloads
econ_players = len(focus_lists["Economy"])
if econ_players == 0:
    econ_split = "an undefined amount of"
else:
    econ_split = int(ceil(econ_pot / econ_players))

# The map
mapping = {'winner': winner, 'runner_ups': runner_ups, 
           'econ_players': econ_players, 'econ_split': econ_split,
           'econ_pot': round(econ_pot,2), 'focus_table': focus_table}

# Apply the map we built above to the template.
with open('template.txt', 'r') as infile:
    template = infile.read()
    
with open('report.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))
