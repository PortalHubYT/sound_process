import pygame.midi
import mcapi as mc
import json
from nbtschematic import SchematicFile
from random import randrange
from copy import copy, deepcopy
from pprint import pprint


def read_input(input_device, bag, play_area):

    board = []
    exists = set()

    while True:

        if input_device.poll():

            event = input_device.read(1)[0]
            data = event[0]
            note_number = data[1]
            note_repr = get_note_representation(note_number)
            note = note_number - 20
            velocity = data[2]

            if note in exists:
                exists.remove(note)
                continue

            else:
                exists.add(note)

                coords = get_random_point(play_area)
                place(bag, board, coords, note_repr)


def get_note_representation(note_number):
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
    return notes[note_number % 12]


def place(bag, board, coords, note_repr):

    keys = list(bag.keys())
    mc.post(f"clone {bag[keys[randrange(len(keys))]]['coords']} {coords} masked")


def get_random_point(play_area):

    pos1 = play_area.pos1
    pos2 = play_area.pos2

    if pos1.x > pos2.x:
        x = randrange(pos2.x, pos1.x)
    else:
        x = randrange(pos1.x, pos2.x)

    if pos1.z > pos2.z:
        z = randrange(pos2.z, pos1.z)
    else:
        z = randrange(pos1.z, pos2.z)

    coords = mc.BlockCoordinates(x, 4, z)
    return coords


def prepare(bag):

    bag["oak_tree_1"] = {
        "coords": mc.Zone((4, 8, 2), (0, 4, -2)),
    }

    bag["oak_tree_2"] = {
        "coords": mc.Zone((0, 4, -5), (4, 10, -9)),
    }

    bag["oak_trunk_1"] = {
        "coords": mc.Zone((3, 5, -18), (1, 4, -13)),
    }

    bag["oak_bush_1"] = {
        "coords": mc.Zone((6, 5, -22), (1, 4, -26)),
    }

    bag["coal_rock_1"] = {
        "coords": mc.Zone((4, 4, -35), (2, 6, -37)),
    }

    bag["diamond_rock_1"] = {
        "coords": mc.Zone((7, 5, -35), (10, 4, -32)),
    }

    bag["campfire"] = {
        "coords": mc.Zone((9, 3, -20), (10, 4, -22)),
    }

    bag["grass_1"] = {
        "coords": mc.Zone((-4, 4, 3), (-8, 5, -2)),
    }


if __name__ == "__main__":

    play_area = mc.Zone((32, 4, 14), (-16, 16, 57))

    bag = {}
    prepare(bag)

    exit()
    mc.connect("localhost", "test")
    pygame.midi.init()
    input_device = pygame.midi.Input(3)

    read_input(input_device, bag, play_area)
