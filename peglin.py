import mcapi as mc
import time
import json
from random import randrange
from maps import *

env = {
    "width": 60,
    "height": 50,
    "depth": 2,
    "origin": mc.BlockCoordinates(0, 4, 0),
    "front_wall": mc.Block("barrier"),
    "back_wall": mc.Block("red_concrete"),
    "peg": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~-1 ~-0.5 ~ {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "peg_tube": mc.Block(
        "oak_trapdoor", blockstate=mc.BlockState({"facing": "west", "half": "top"})
    ),
    "left_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~ ~ ~1.75 {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "right_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~ ~ ~-1.75 {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "top_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2.85, type=sheep] run summon minecraft:tnt ~ ~-1.65 ~ {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "bouncer_walls": mc.Block("slime_block"),
    "cover": mc.Block("bedrock"),
}


def generate_board(clear=True, map=None):

    if clear:
        clear_map()

    x1, y1, z1 = env["origin"].set

    if map:
        untrimmed_grid = map.splitlines()
        grid = [x for x in untrimmed_grid if x]
        x2 = x1 + env["depth"] - 1
        y2 = y1 + len(grid) - 1
        z2 = z1 + len(grid[0]) - 1

    else:

        x2 = x1 + env["depth"] - 1
        y2 = y1 + env["height"] - 1
        z2 = z1 + env["width"] - 1

    void = mc.Zone((x1, y1, z1), (x2, y1 - 4, z2))
    mc.set_zone(void, mc.Block("air"))

    # Walls #

    front_wall = mc.Zone((x1 - 1, y1 - 4, z1), (x1 - 1, y2, z2))
    mc.set_zone(front_wall, env["front_wall"])

    back_wall = mc.Zone((x2 + 1, y1 - 4, z1), (x2 + 1, y2, z2))
    mc.set_zone(back_wall, mc.Block("barrier"))

    back_wall = mc.Zone((x2 + 2, y1 - 4, z1), (x2 + 2, y2, z2))
    mc.set_zone(back_wall, env["back_wall"])

    # Left bouncer #

    for i in range(y1 - 4, y2):
        pass

    left_bouncer = mc.Zone((x1, y1 - 4, z1 - 2), (x2, y2, z1 - 2))
    # mc.set_zone(left_bouncer, env["left_bouncer"])

    left_bouncer_wall = mc.Zone((x1, y1 - 4, z1 - 1), (x2, y2, z1 - 1))
    mc.set_zone(left_bouncer_wall, env["bouncer_walls"])

    left_bouncer_cover = mc.Zone((x1 - 1, y1 - 4, z1 - 1), (x2 + 1, y2 + 3, z1 - 3))
    mc.set_zone(left_bouncer_cover, env["cover"], handler="keep")

    # Right bouncer #

    right_bouncer = mc.Zone((x1, y1 - 4, z2 + 2), (x2, y2, z2 + 2))
    # mc.set_zone(right_bouncer, env["right_bouncer"])

    right_bouncer_wall = mc.Zone((x1, y1 - 4, z2 + 1), (x2, y2, z2 + 1))
    mc.set_zone(right_bouncer_wall, env["bouncer_walls"])

    right_bouncer_cover = mc.Zone((x1 - 1, y1 - 4, z2 + 1), (x2 + 1, y2 + 3, z2 + 3))
    mc.set_zone(right_bouncer_cover, env["cover"], handler="keep")

    # Cover

    top_bouncer = mc.Zone((x1, y2 + 2, z1), (x2, y2 + 2, z2))
    # mc.set_zone(top_bouncer, env["top_bouncer"])

    top_bouncer_wall = mc.Zone((x1, y2 + 1, z1), (x2, y2 + 1, z2))
    mc.set_zone(top_bouncer_wall, env["bouncer_walls"])

    top_bouncer_cover = mc.Zone((x1 - 1, y2 + 1, z1 - 1), (x2 + 1, y2 + 3, z2 + 3))
    mc.set_zone(top_bouncer_cover, env["cover"], handler="keep")

    # Bottom

    bottom_line = mc.Zone((x1 - 1, y1 - 1, z1), (x1 - 1, y1 - 1, z2))
    mc.set_zone(bottom_line, env["cover"])

    if map:

        pegs_coords = []
        for x, line in enumerate(grid):
            for y, block in enumerate(line):
                if block == "O":
                    pegs_coords.append((x, y))

        for coords in pegs_coords:
            place_coords = (x2 + 1, y2 - coords[0], z1 + coords[1])
            mc.set_block(place_coords, env["peg"])

            place_coords = (x2, y2 - coords[0] - 1, z1 + coords[1])
            mc.set_block(place_coords, env["peg_tube"])


def clear_map():
    x1, y1, z1 = env["origin"].set

    for y in range(125):
        clearance = mc.Zone((x1 - 4, y1 + y, z1 - 3), (x1 + 4, y1 + y, 80))
        mc.set_zone(clearance, mc.Block("air"))


def spawn_random_balls(names, map=None):

    x1, y1, z1 = env["origin"].set

    if map:

        untrimmed_grid = map.splitlines()
        grid = [x for x in untrimmed_grid if x]
        y2 = y1 + len(grid) - 1
        z2 = z1 + len(grid[0]) - 1

        rand_z = randrange(env["origin"].x, z2)

    else:
        y2 = y1 + env["height"] - 1
        z2 = z1 + env["width"] - 1

        rand_z = randrange(env["origin"].x, env["origin"].z + env["width"] - 1)

    coords = mc.Coordinates(env["depth"] / 2, y2 - 0.5, rand_z)

    command = (
        f"summon slime {coords} "
        + '{Size:1,CustomNameVisible:1b,CustomName:\'{"text":"'
        + f"{names[randrange(len(names))]}"
        + "\"}',ActiveEffects:[{Id:11b,Amplifier:5b,Duration:900000,ShowParticles:0b},{Id:28b,Amplifier:1b,Duration:9000,ShowParticles:0b}]}"
    )

    ret = mc.post(command)


if __name__ == "__main__":

    with open("random_names_simplified.json", "r") as file:
        names = json.load(file)

    mc.connect("localhost", "test")

    mc.post("kill @e[type=slime]")
    mc.post("region flag __global__ tnt deny")
    generate_board(map=map_3, clear=True)

    while True:
        spawn_random_balls(names, map=map_3)
        time.sleep(0.5)
