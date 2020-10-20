"""
file: person.py
author: Misty Zheng
description: helper methods read and write bot data into a JSON file
"""
import json

"""global variable that holds the file name"""
filename = "data.json";

"""
Changed the default filename to the appropriate file for the guild
:param guid_id: the id of a specific guild, used in the filename
"""
def select_file(guild_id):
    global filename
    filename = (str(guild_id) + "data.json")
    try:
        with open(filename) as f:
            print(filename + " selected")
    except IOError:
        f = open(filename, "x")

""" 
Loads bot data from a JSON file and changes a Person's reputation 
:param people: a list of object type Person
"""

def load_data(people):
    try:
        with open(filename) as f:
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
    out = {}
    with open(filename, "r") as f:
        data = json.load(f)

        idstr = str(member.id)
        for person in people:
            if idstr != str(person.id):
                out[person.id] = person.rep
    with open(filename, "w") as f:
        json.dump(out, f)

""" 
Saves bot data into a JSON file and stores reputation of people
:param people: a list of object type Person
"""
def save_data(people):
    out = {}
    for person in people:
        out[person.id] = person.rep

    with open(filename, "w") as f:
        json.dump(out, f)