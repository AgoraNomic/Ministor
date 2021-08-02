from sys import argv
from csv import reader
from datetime import datetime, timezone
from re import sub

# CL flags
isTest = "-t" in argv
doUpdate = "-u" in argv

# Update interests for new month
if doUpdate:
    with open('focuses.csv', 'r') as file:
        filedata = file.read()
        
    with open('plantoflips.csv', 'r') as file:
        replacement_list = reader(file, delimiter=',', quotechar="\"")
        for row in replacement_list:
            matcher = row[0] + "\S*"
            new_entry = row[0] + "," + row[1]
            filedata = sub(matcher,new_entry,filedata)
            
    with open('focuses.txt', 'w') as file:
        file.write(filedata)

# Determine timestamp
now = datetime.now(timezone.utc)

if isTest:
    report_name = "test"
else:
    report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

timestamp = str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2)
#TODO: use strftime?

# Import focuses
focuses = {}

focus_lists = {"Unfocused": [], "Legacy": [], "Participation": [], "Compliance": [], "Legislation": []}

max_name_len = 0
max_focus_len = 0

with open('focuses.csv', 'r') as infile:
    infocuses = reader(infile, delimiter=',', quotechar="\"")
    for row in infocuses:
        focus_lists[row[1]].append(row[0])

# Build focus table
focus_table = ""

for key in sorted(focus_lists.keys()):
    focus_table += key + " (" + str(len(focus_lists[key])) + "): " + ", ".join(sorted(focus_lists[key])) + "\n\n"

focus_table = focus_table[:-2]
    
# Legacy values (rolled in the discord)
winner = "ATMunn"

# Map variables to the template's variables
mapping = {'focus_table': focus_table, 'timestamp': timestamp}

mapping_vic = {'winner': winner}

# Apply the map we built above to the template to build a new report.
with open('template.txt', 'r') as infile:
    template = infile.read()

with open('template-victory.txt', 'r') as infile:
    template_vic = infile.read()

with open('reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))

with open('reports/' + report_name + '-victory.txt', 'w') as ofile:
    ofile.write(template_vic.format_map(mapping_vic))
