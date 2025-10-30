# Deploy complex pumpkin layouts based on world and drone capacity.


def move_steps(direction, steps):
    index = 0
    while index < steps:
        move(direction)
        index = index + 1


def minipatch_drone():
    change_hat(Hats.GREEN_HAT)
    while True:
        top_measure = 0
        bottom_measure = 0
        row = 0
        while row < 4:
            column = 0
            while column < 4:
                if get_entity_type() != Entities.PUMPKIN:
                    plant(Entities.PUMPKIN)
                if row == 0 and column == 0:
                    measurement = measure()
                    if measurement != None:
                        top_measure = measurement
                elif row == 2 and column == 2:
                    measurement = measure()
                    if measurement != None:
                        bottom_measure = measurement
                move(Direction.EAST)
                column = column + 1
            move_steps(Direction.WEST, 4)
            move(Direction.NORTH)
            row = row + 1
        move_steps(Direction.SOUTH, 4)
        if top_measure == bottom_measure and can_harvest():
            harvest()


def patch_drone():
    change_hat(Hats.PURPLE_HAT)
    while True:
        top_measure = 0
        bottom_measure = 0
        row = 0
        while row < 6:
            column = 0
            while column < 6:
                if get_entity_type() != Entities.PUMPKIN:
                    plant(Entities.PUMPKIN)
                if row == 0 and column == 0:
                    measurement = measure()
                    if measurement != None:
                        top_measure = measurement
                elif row == 4 and column == 4:
                    measurement = measure()
                    if measurement != None:
                        bottom_measure = measurement
                move(Direction.EAST)
                column = column + 1
            move_steps(Direction.WEST, 6)
            move(Direction.NORTH)
            row = row + 1
        move_steps(Direction.SOUTH, 6)
        if top_measure == bottom_measure and can_harvest():
            harvest()


def prep_drone():
    field_size = get_world_size()
    step = 0
    while step < field_size:
        if get_ground_type() != Grounds.SOIL:
            till()
        move(Direction.NORTH)
        step = step + 1


def horizontal_sunflower_drone():
    change_hat(Hats.GRAY_HAT)
    while True:
        field_size = get_world_size()
        step = 0
        while step < field_size:
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.SOIL:
                till()
            plant(Entities.SUNFLOWER)
            move(Direction.EAST)
            step = step + 1


def vertical_sunflower_drone():
    change_hat(Hats.TRAFFIC_CONE)
    while True:
        field_size = get_world_size()
        step = 0
        while step < field_size:
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.SOIL:
                till()
            plant(Entities.SUNFLOWER)
            move(Direction.NORTH)
            step = step + 1


def maintain_minipatch_cycle():
    change_hat(Hats.GREEN_HAT)
    while True:
        top_measure = 0
        bottom_measure = 0
        row = 0
        while row < 4:
            column = 0
            while column < 4:
                if get_entity_type() != Entities.PUMPKIN:
                    plant(Entities.PUMPKIN)
                if row == 0 and column == 0:
                    measurement = measure()
                    if measurement != None:
                        top_measure = measurement
                elif row == 2 and column == 2:
                    measurement = measure()
                    if measurement != None:
                        bottom_measure = measurement
                move(Direction.EAST)
                column = column + 1
            move_steps(Direction.WEST, 4)
            move(Direction.NORTH)
            row = row + 1
        move_steps(Direction.SOUTH, 4)
        if top_measure == bottom_measure and can_harvest():
            harvest()


def deploy_full_layout(field_size):
    column = 0
    while column < field_size - 1:
        spawn_drone(prep_drone)
        move(Direction.EAST)
        column = column + 1
    spawn_drone(prep_drone)
    move(Direction.EAST)
    block = 0
    while block < 4:
        spawn_drone(patch_drone)
        move_steps(Direction.EAST, 6)
        spawn_drone(vertical_sunflower_drone)
        move(Direction.EAST)
        block = block + 1
    spawn_drone(minipatch_drone)
    move_steps(Direction.EAST, 4)
    move_steps(Direction.NORTH, 6)
    spawn_drone(horizontal_sunflower_drone)
    move(Direction.NORTH)
    row_block = 0
    while row_block < 3:
        column_block = 0
        while column_block < 4:
            spawn_drone(patch_drone)
            move_steps(Direction.EAST, 6)
            move(Direction.EAST)
            column_block = column_block + 1
        spawn_drone(minipatch_drone)
        move_steps(Direction.EAST, 4)
        move_steps(Direction.NORTH, 6)
        spawn_drone(horizontal_sunflower_drone)
        move(Direction.NORTH)
        row_block = row_block + 1
    tail = 0
    while tail < 3:
        spawn_drone(minipatch_drone)
        move_steps(Direction.EAST, 7)
        tail = tail + 1


def deploy_compact_layout(field_size):
    column = 0
    while column < field_size:
        spawn_drone(prep_drone)
        if column < field_size - 1:
            move(Direction.EAST)
        column = column + 1
    move_steps(Direction.WEST, field_size - 1)
    row_count = 4
    column_count = 2
    patch_width = 6
    gap = 4
    row_width = column_count * patch_width + (column_count - 1) * gap
    row_index = 0
    while row_index < row_count:
        column_index = 0
        while column_index < column_count:
            spawn_drone(patch_drone)
            move_steps(Direction.EAST, patch_width)
            if row_index == 0 and column_index < column_count:
                spawn_drone(vertical_sunflower_drone)
            if column_index < column_count - 1:
                move_steps(Direction.EAST, gap)
            column_index = column_index + 1
        if row_index == 0 or row_index == 2:
            spawn_drone(minipatch_drone)
        move_steps(Direction.WEST, row_width)
        if row_index < row_count - 1:
            move_steps(Direction.NORTH, patch_width)
            if row_index == 0 or row_index == 2:
                spawn_drone(horizontal_sunflower_drone)
            move(Direction.NORTH)
        row_index = row_index + 1
    spawn_drone(minipatch_drone)
    move_steps(Direction.SOUTH, (row_count - 1) * (patch_width + 1))


def main():
    field_size = get_world_size()
    available_drones = max_drones()
    if available_drones >= 32 and field_size >= 32:
        clear()
        deploy_full_layout(field_size)
    elif available_drones >= 16 and field_size >= 22:
        clear()
        deploy_compact_layout(field_size)
    else:
        print("Insufficient world size or drones for pumpkin_farm_2 layout.")


main()
