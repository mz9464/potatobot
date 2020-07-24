import json

def load_data(people):
    with open("data.json") as f:
        data = json.load(f)

        for person in people:
            if person.id in data:
                person.rep = data[person.id]

def save_data(people):
    out = {}
    for person in people:
        out[person.id] = person.rep

    with open("data.json", "w") as f:
        json.dump(out, f)