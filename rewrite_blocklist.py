import json


f = open("mcapi/functions/block_list.json")

data = json.loads(f.read())

new_data = {}


with open("simplified_blocklist.json", "w") as file:
    for block in data:
        print(block)
        for state in data[block]["states"]:
            new_data[state["id"]] = f"{block}"

    json.dump(new_data, file)

print(data)
