import mcapi as mc
import time

env = {
    "width": 40,
    "height": 30,
    "origin": mc.BlockCoordinates(0, 4, 0),
    "front_wall": mc.Block("barrier"),
    "back_wall": mc.Block("obsidian"),
    "peg": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~-1 ~ ~ {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "left_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~ ~ ~1 {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "right_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~ ~ ~-1 {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "top_bouncer": mc.Block(
        "repeating_command_block",
        nbt=mc.NBT(
            {
                "Command": 'execute if entity @e[distance=..2] run summon minecraft:tnt ~ ~-1 ~ {"fuse":0}',
                "auto": 1,
            }
        ),
    ),
    "bouncer_walls": mc.Block("end_gateway"),
    "cover": mc.Block("bedrock"),
}

map_1 = """
#####O####################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
###O##################################O###
##########################################
##############################O###########
###########O##############################
###O##############################O#######
##########################################
#####O#####################O##############
#################O###################O####
#########O###############O################
##############################O###########
##########################################
##########################################
#####O#####################O##############
#################O###################O####
##########################################
#########O###############O################
##########################################
##############################O###########
#####O####################################
###########################O##############
####O#####O##########O###############O####
##########################################
##########################################
#######O#####################O############
##########################################
"""


def generate_board(clear=True, map=None):

    if clear:
        clear_map()

    x1, y1, z1 = env["origin"].set

    if map:
        untrimmed_grid = map.splitlines()
        grid = [x for x in untrimmed_grid if x]
        y2 = y1 + len(grid) - 1
        z2 = z1 + len(grid[0]) - 1

    else:

        y2 = y1 + env["height"] - 1
        z2 = z1 + env["width"] - 1

    void = mc.Zone((x1, y1, z1), (x1, y1 - 4, z2))
    mc.set_zone(void, mc.Block("air"))

    # Walls #

    front_wall = mc.Zone((x1 - 1, y1, z1), (x1 - 1, y2, z2))
    mc.set_zone(front_wall, env["front_wall"])

    back_wall = mc.Zone((x1 + 1, y1 - 4, z1), (x1 + 1, y2, z2))
    mc.set_zone(back_wall, env["back_wall"])

    # Left bouncer #

    left_bouncer = mc.Zone((x1, y1 - 4, z1 - 2), (x1, y2, z1 - 2))
    mc.set_zone(left_bouncer, env["left_bouncer"])

    left_bouncer_wall = mc.Zone((x1, y1 - 4, z1 - 1), (x1, y2, z1 - 1))
    mc.set_zone(left_bouncer_wall, env["bouncer_walls"])

    left_bouncer_cover = mc.Zone((x1 - 1, y1 - 4, z1 - 1), (x1 + 1, y2 + 3, z1 - 3))
    mc.set_zone(left_bouncer_cover, env["cover"], handler="keep")

    # Right bouncer #

    right_bouncer = mc.Zone((x1, y1 - 4, z2 + 2), (x1, y2, z2 + 2))
    mc.set_zone(right_bouncer, env["right_bouncer"])

    right_bouncer_wall = mc.Zone((x1, y1 - 4, z2 + 1), (x1, y2, z2 + 1))
    mc.set_zone(right_bouncer_wall, env["bouncer_walls"])

    right_bouncer_cover = mc.Zone((x1 - 1, y1 - 4, z2 + 1), (x1 + 1, y2 + 3, z2 + 3))
    mc.set_zone(right_bouncer_cover, env["cover"], handler="keep")

    # Cover

    top_bouncer = mc.Zone((x1, y2 + 2, z1), (x1, y2 + 2, z2))
    mc.set_zone(top_bouncer, env["top_bouncer"])

    top_bouncer_wall = mc.Zone((x1, y2 + 1, z1), (x1, y2 + 1, z2))
    mc.set_zone(top_bouncer_wall, env["bouncer_walls"])

    top_bouncer_cover = mc.Zone((x1 - 1, y2 + 1, z1 - 1), (x1 + 1, y2 + 3, z2 + 3))
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
            place_coords = (x1 + 1, y2 - coords[0], z1 + coords[1])
            mc.set_block(place_coords, env["peg"])


def clear_map():
    x1, y1, z1 = env["origin"].set
    clearance = mc.Zone((x1 - 3, y1, z1 - 4), (x1 + 3, 70, 60))
    print(mc.set_zone(clearance, mc.Block("air")))


if __name__ == "__main__":
    mc.connect("localhost", "test")
    generate_board(map=map_1, clear=True)
