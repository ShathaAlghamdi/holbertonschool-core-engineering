#!/usr/bin/env python3
alphabet = ""

for letter in "abcdefghijklmnopqrstuvwxyz":
    if letter != "q" and letter != "e":
        alphabet += letter

print("{}".format(alphabet))
