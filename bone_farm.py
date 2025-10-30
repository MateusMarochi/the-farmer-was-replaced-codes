# Dinosaur hat sweep strategy with consistent movement helpers.

from directions import EAST, NORTH, SOUTH, WEST


def dinosaur_safe_move(direction):
    # Move in *direction* or toggle hats when blocked.

    if can_move(direction):
        move(direction)
        return
    change_hat(Hats.CARROT_HAT)
    change_hat(Hats.DINOSAUR_HAT)


def travel_vertical(target_row):
    # Travel vertically until reaching *target_row*.

    while get_pos_y() != target_row:
        if target_row > get_pos_y():
            dinosaur_safe_move(NORTH)
        else:
            dinosaur_safe_move(SOUTH)


def travel_horizontal(target_column):
    # Travel horizontally until reaching *target_column*.

    while get_pos_x() != target_column:
        if target_column > get_pos_x():
            dinosaur_safe_move(EAST)
        else:
            dinosaur_safe_move(WEST)


def sweep_columns(field_size):
    # Snake through every column of the field.

    column_index = 0
    while column_index < field_size:
        if column_index % 2 == 0:
            target_row = field_size - 1
        else:
            target_row = 1
        travel_vertical(target_row)
        if column_index < field_size - 1:
            dinosaur_safe_move(EAST)
        column_index = column_index + 1


def return_to_origin():
    # Return to position (0, 0).

    travel_vertical(0)
    travel_horizontal(0)


def main():
    # Execute the endless dinosaur sweep.

    clear()
    change_hat(Hats.DINOSAUR_HAT)
    field_size = get_world_size()
    while True:
        sweep_columns(field_size)
        return_to_origin()


main()
