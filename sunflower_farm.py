# Sunflower farming with column workers sized to available drones.

from directions import EAST, NORTH, SOUTH, WEST
import plantacoes


def move_to_column(target_column):
    while get_pos_x() < target_column:
        move(EAST)
    while get_pos_x() > target_column:
        move(WEST)


def move_to_row(target_row):
    while get_pos_y() < target_row:
        move(NORTH)
    while get_pos_y() > target_row:
        move(SOUTH)


def maintain_sunflower_tile():
    if get_entity_type() != Entities.SUNFLOWER:
        if can_harvest():
            harvest()
        plantacoes.plant_sunflower()
    else:
        if can_harvest():
            harvest()
            plantacoes.plant_sunflower()


def sunflower_column_worker(column_index, field_size):
    move_to_column(column_index)
    move_to_row(0)
    while True:
        row = 0
        while row < field_size:
            maintain_sunflower_tile()
            if row < field_size - 1:
                move(NORTH)
            row = row + 1
        move_to_row(0)


def make_sunflower_worker(column_index, field_size):
    def runner():
        sunflower_column_worker(column_index, field_size)

    return runner


def deploy_sunflower_farm(field_size, available_slots):
    assigned_columns = available_slots
    if assigned_columns > field_size:
        assigned_columns = field_size
    column = 1
    while column < assigned_columns:
        runner = make_sunflower_worker(column, field_size)
        drone = spawn_drone(runner)
        if drone == None:
            break
        column = column + 1
    sunflower_column_worker(0, field_size)


def main():
    field_size = get_world_size()
    available_slots = max_drones()
    if available_slots < 1:
        available_slots = 1
    deploy_sunflower_farm(field_size, available_slots)


main()
