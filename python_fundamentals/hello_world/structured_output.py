#!/usr/bin/env python3
# language = "Python"
# version = 3
# pi_approx = 22 / 7
# computation_valid = version == 3

# print(f"Language: {language}")
# print(f"Version: {version}")
# print(f"Pi approx: {pi_approx:.2f}")
# print(f"Computation valid: {computation_valid}")

def pig_latin_sentence(sentence):
    words = sentence.split()

    result = []

    for word in words:
        result.append(word[1:] + word[0] + "ay")

    return " ".join(result)

print(pig_latin_sentence("hello world python"))