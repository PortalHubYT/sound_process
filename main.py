import pygame.midi
import mcapi as mc
import json
from nbtschematic import SchematicFile
from random import randrange
from copy import copy, deepcopy
from pprint import pprint


def print_devices():
    for n in range(pygame.midi.get_count()):
        print(n, pygame.midi.get_device_info(n))


def number_to_note(number):
    notes = [
        "Do",
        "Do#",
        "Ré",
        "Ré#",
        "Mi",
        "Fa",
        "Fa#",
        "Sol",
        "Sol#",
        "La",
        "La#",
        "Si",
    ]
    return notes[number % 12]


def read_input(input_device, bag, order):

    exists = set()

    while True:

        if input_device.poll():

            event = input_device.read(1)[0]
            data = event[0]
            note_number = data[1]
            note = note_number - 20
            velocity = data[2]

            if note in exists:
                exists.remove(note)
                continue

            else:
                exists.add(note)
                order = paste(bag, order, amplitude=1)


def print_bag_summary(bag):
    total_len = 0
    for block_type in bag:
        total_len += len(bag[block_type])
    for block_type in bag:
        l = len(bag[block_type])
        print(f"{block_type}: {l} ({round(l / total_len *100)}%)")


def paste(bag, order, amplitude=1):

    for _ in range(amplitude):

        if order:

            if f"minecraft:{order[0]}" in bag.keys():

                x, y, z = bag[f"minecraft:{order[0]}"].pop(0)
                block = f"setblock {x} {y} {z} minecraft:{order[0]}"

                if len(bag[f"minecraft:{order[0]}"]) == 0:
                    order.pop(0)
                    del bag[f"minecraft:{order[0]}"]

            else:

                order.pop(0)

            continue

        blocks = list(bag.keys())
        x, y, z = bag[blocks[0]].pop(0)
        block = f"setblock {x} {y} {z} {blocks[0]}"

        if len(bag[blocks[0]]) == 0:
            del bag[blocks[0]]

        print(block)
        mc.post(block)

    return order


def paste_random(bag, amplitude=1):
    for _ in range(amplitude):
        command = bag.pop(randrange(len(bag)))
        mc.post(command)


def split_bag(bag):
    """This will turn the bag into a dict split by
    each type of blocks"""

    new_bag = {}

    for block in bag:
        if block[1] not in list(new_bag.keys()):
            new_bag[block[1]] = []
        new_bag[block[1]].append(block[0])

    return new_bag


def sort_bag(bag):
    """This will sort a list of block_coordinates from Y: 0 to Y:255"""

    for key in bag.keys():
        bag[key].sort(key=lambda coord: coord[1])

    return bag


def parse_bag():
    sf = SchematicFile.load("steampunk.schematic")
    # sf = SchematicFile.load("file.schematic")
    ymax, zmax, xmax = sf.blocks.shape

    bag = []
    with open("simplified_blocklist.json", "r") as file:
        blocklist = json.load(file)

    print("Preparing bag")

    for y in range(ymax):
        for z in range(zmax):
            for x in range(xmax):
                block_id = str(int(sf.blocks[y, z, x]))
                if block_id != "0":
                    block_name = blocklist[block_id]
                    if "water" in block_name or "lava" in block_name:
                        continue
                    bag.append([(x, y + 5, z), block_name])

    print("Bag done")

    return bag


def outright_print(bag, block_list):
    new_bag = {}
    for b_to_print in block_list:
        for btype in bag:
            if f"minecraft:{b_to_print}" in btype:
                for x, y, z in bag[btype]:
                    block = f"setblock {x} {y} {z} {btype}"
                    mc.post(block)
            else:
                new_bag[btype] = bag[btype]
    return new_bag


def prepare_bag():

    bag = parse_bag()
    bag = split_bag(bag)
    bag = sort_bag(bag)
    bag = outright_print(bag, ["granite", "stone"])
    print_bag_summary(bag)

    return bag


if __name__ == "__main__":

    order = ["stone", "dirt", "grass_block", "granite", "polished_granite", "podzol"]

    bag = prepare_bag()

    mc.connect("localhost", "test")
    pygame.midi.init()

    input_device = pygame.midi.Input(3)
    read_input(input_device, bag, order)
