"""
file: person.py
author: Misty Zheng
description: helper methods read and write bot data into a JSON file
"""
import json
""" 
Loads bot data from a JSON file and changes a Person's reputation 
:param people: a list of object type Person
"""
def load_data(people):
    with open("data.json") as f:
        data = json.load(f)

        for person in people:
            idstr = str(person.id)
            if idstr in data:
                person.rep = data[idstr]
    return people

""" 
Saves bot data into a JSON file and stores reputation of people
:param people: a list of object type Person
"""
def save_data(people):
    out = {}
    for person in people:
        out[person.id] = person.rep

    with open("data.json", "w") as f:
        json.dump(out, f)