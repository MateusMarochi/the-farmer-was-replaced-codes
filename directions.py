# Cardinal direction constants and helpers decoupled from the game API.

EAST = "East"
WEST = "West"
NORTH = "North"
SOUTH = "South"


def rotate_right(direction):
    # Return the direction to the right of *direction*.

    if direction == NORTH:
        return EAST
    if direction == EAST:
        return SOUTH
    if direction == SOUTH:
        return WEST
    return direction


def rotate_left(direction):
    # Return the direction to the left of *direction*.

    if direction == NORTH:
        return WEST
    if direction == WEST:
        return SOUTH
    if direction == SOUTH:
        return EAST
    return direction
