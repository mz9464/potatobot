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
    try:
        with open("data.json") as f:
            data = json.load(f)

            for person in people:
                idstr = str(person.id)
                if idstr in data:
                    person.rep = data[idstr]
    except:
        save_data(people)

""" 
Deletes person's data from a JSON file
:param member: the member being deleted
:param people: a list of object type Person
"""
def delete_member(member, people):
    with open("data.json", "r") as f:
        data = json.load(f)

        idstr = str(member.id)
        for person in people:
            if idstr == str(person.id):
                people.pop(person.id, None) #TODO
    with open("data.json", "w") as f:
        json.dump(data, f)

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