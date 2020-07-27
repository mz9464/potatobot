import json

def load_data(people):
    with open("data.json") as f:
        data = json.load(f)

        for person in people:
            print("testing person " + str(person.id))
            if person.id in data:
                print('match')
                person.rep = data[person.id]
            else:
                print('no match')

def save_data(people):
    out = {}
    for person in people:
        out[person.id] = person.rep

    with open("data.json", "w") as f:
        json.dump(out, f)