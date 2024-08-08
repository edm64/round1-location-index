#!/usr/bin/env python3
import csv
from enum import IntEnum

readme_file="README.md"
data_file="r1index.csv"

class column(IntEnum):
    code = 0
    shop = 1
    city = 2
    state= 3
    zenius=4

tablehead="|:---:|--------|----|-----|"

# slim down the existing file, deleting the existing tables
readme = []
with open(readme_file, 'r') as md:
    while True:
        line = md.readline()
        if line == "":
            break
        elif not line.startswith("|*"):
            readme.append(line.strip())

# build the first table from csv, ordered by shop code
with open(data_file, 'r', newline="") as data:
    reader = csv.reader(data)
    # csv should already be in order, but it can't hurt to be sure
    table_list = sorted(reader, key=lambda r: r[column.code])

# format shop codes in bold
for line in table_list:
    if line[column.zenius] == "N/A":
        line[column.code] = "**"+line[column.code]+"**"
    else:
        line[column.code] = "[**"+line[column.code]+"**]"+"("+line[column.zenius]+")"

# convert to string & add markdown separators
table = ["|".join([""]+line[:4]+[""]) for line in table_list if line[column.zenius] != ""]

# reorder for the hidden table
table_list.sort(key=lambda r: (r[column.state], r[column.city]))
alt_table = ["|".join([""]+line[:4]+[""]) for line in table_list if line[column.zenius] != ""]

# find where the table entries will be inserted
tablepos1 = readme.index(tablehead)+1
tablepos2 = readme.index(tablehead, tablepos1)+1

# split list into sections
top = readme[:tablepos1]
mid = readme[tablepos1:tablepos2]
bot = readme[tablepos2:]

# overwrite the readme with new tables
with open(readme_file,'w') as md:
    for block in (top, table, mid, alt_table, bot):
        for line in block:
            md.write(line+'\r\n')
