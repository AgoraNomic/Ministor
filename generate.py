from sys import argv
from random import choice
from math import ceil
from csv import reader
from datetime import datetime, timezone
from re import sub

# CL flags
isTest = "-t" in argv
doUpdate = "-u" in argv

# Update interests for new month
if doUpdate:
    with open('focuses.txt', 'r') as file:
        filedata = file.read()
        
    with open('plantoflips.txt', 'r') as file:
        replacement_list = reader(file, delimiter=',', quotechar="\"")
        for row in replacement_list:
            matcher = row[0] + "\S*"
            new_entry = row[0] + "," + row[1]
            filedata = sub(matcher,new_entry,filedata)
            
    with open('focuses.txt', 'w') as file:
        file.write(filedata)

# Determine timestamp
now = datetime.now(timezone.utc)
report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
timestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2)

# Import focuses
focuses = {}

focus_lists = {"Unfocused": [], "Legacy": [], "Participation": [], "Compliance": [], "Economy": [], "Legislation": []}

max_name_len = 0
max_focus_len = 0

with open('focuses.txt', 'r') as infile:
    infocuses = reader(infile, delimiter=',', quotechar="\"")
    for row in infocuses:
        focus_lists[row[1]].append(row[0])

# Build focus table
focus_table = ""

for key in sorted(focus_lists.keys()):
    focus_table += key + " (" + str(len(focus_lists[key])) + "): " + ", ".join(sorted(focus_lists[key])) + "\n\n"

focus_table = focus_table[:-2]

# Import interests
interests = {}

max_office_len = 0

with open('interests.txt', 'r') as infile:
    ininterests = reader(infile, delimiter=',')
    for row in ininterests:
        interests[row[0]] = row[1]
        max_office_len = max(max_office_len, len(row[0]))

# Build interest table
interest_table = ""

for key in sorted(interests.keys()):
    interest_table += (key).ljust(max_office_len+3) + interests[key] + "\n"

interest_table = interest_table[:-1]

# Calculate Legacy stuff
legacy_players = focus_lists["Legacy"]

if len(legacy_players)==0:
    winner = "no one, as there are no legacy focused players"
else:
    winner = choice(legacy_players)
    legacy_players.remove(winner)

runner_ups = ", ".join(legacy_players)

# Calculate Econ stuff
boatloads = 4.6212
econ_pot = 50 * boatloads
econ_players = len(focus_lists["Economy"])

if econ_players == 0:
    econ_split = "an undefined amount of"
else:
    econ_split = int(ceil(econ_pot / econ_players))

# Map variables to the template's variables
mapping = {'econ_players': econ_players, 'econ_split': econ_split,
           'econ_pot': round(econ_pot), 'focus_table': focus_table, 'interest_table': interest_table, 'timestamp': timestamp}

mapping_vic = {'winner': winner, 'runner_ups': runner_ups}

# Apply the map we built above to the template to build a new report.
with open('template.txt', 'r') as infile:
    template = infile.read()

with open('template-victory.txt', 'r') as infile:
    template_vic = infile.read()

if isTest:
    report_name = "test"

with open('reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))

with open('reports/' + report_name + '-victory.txt', 'w') as ofile:
    ofile.write(template_vic.format_map(mapping_vic))
