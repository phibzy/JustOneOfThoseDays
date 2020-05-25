#!/usr/bin/python3

"""
Little script to sort cards file based on misery index

"""

import re

f1 = open("card_list.txt")

cardReg = re.compile(r"^(.*) (\d.*)$")

resultList = list()

for line in f1.readlines():
    mo = cardReg.search(line) 
    resultList.append((mo.group(1), float(mo.group(2))))

f1.close()

resultList.sort(key=lambda tup: tup[1])

for i in resultList:
    print(i)

f1 = open("card_list", "w")
for desc, val in resultList:
    f1.write(desc + ' ' + str(val) + '\n')
f1.close()
