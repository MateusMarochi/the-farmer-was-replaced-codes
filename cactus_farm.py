# Parallel cactus sorting routine with consistent naming and helpers.

from directions import EAST, NORTH, SOUTH, WEST
import plantacoes

PREFERRED_DRONES = (32, 16)
PETS_PER_CYCLE = 10

_active_stride = 1


def choose_worker_count(max_available, field_size):
    # Return the desired number of workers based on availability and size.

    index = 0
    while index < len(PREFERRED_DRONES):
        preferred = PREFERRED_DRONES[index]
        if max_available >= preferred and field_size >= preferred:
            return preferred
        index = index + 1
    if max_available < 1:
        return 1
    if field_size < 1:
        return 1
    if max_available < field_size:
        return max_available
    return field_size


def set_active_stride(value):
    # Store the stride shared by all workers.

    global _active_stride
    if value < 1:
        _active_stride = 1
        return
    _active_stride = value


def get_active_stride():
    # Return the stride shared by all workers.

    return _active_stride


def move_to_column(target_column):
    # Move horizontally until reaching *target_column*.

    while get_pos_x() < target_column:
        move(EAST)
    while get_pos_x() > target_column:
        move(WEST)


def move_to_row(target_row):
    # Move vertically until reaching *target_row*.

    while get_pos_y() < target_row:
        move(NORTH)
    while get_pos_y() > target_row:
        move(SOUTH)


def ensure_cactus_here():
    # Plant a cactus on the current tile if necessary.

    if get_entity_type() != Entities.CACTUS:
        if can_harvest():
            harvest()
        plantacoes.plant_cactus()


def safe_measure(direction=None):
    # Measure the tile in *direction* or the current tile when omitted.

    if direction == None:
        value = measure()
    else:
        value = measure(direction)
    if value == None:
        return -1
    return value


def has_north(field_size):
    return get_pos_y() < field_size - 1


def has_south():
    return get_pos_y() > 0


def has_east(field_size):
    return get_pos_x() < field_size - 1


def has_west():
    return get_pos_x() > 0


def compare_vertical(field_size):
    current_value = safe_measure()
    if has_north(field_size):
        north_value = safe_measure(NORTH)
        if current_value > north_value:
            swap(NORTH)
            current_value = safe_measure()
    if has_south():
        south_value = safe_measure(SOUTH)
        if current_value < south_value:
            swap(SOUTH)


def compare_horizontal(field_size):
    current_value = safe_measure()
    if has_east(field_size):
        east_value = safe_measure(EAST)
        if current_value > east_value:
            swap(EAST)
            current_value = safe_measure()
    if has_west():
        west_value = safe_measure(WEST)
        if current_value < west_value:
            swap(WEST)


def vertical_pass(field_size):
    steps_up = 0
    while True:
        ensure_cactus_here()
        compare_vertical(field_size)
        if has_north(field_size):
            move(NORTH)
            steps_up = steps_up + 1
        else:
            break
    while steps_up > 0:
        move(SOUTH)
        steps_up = steps_up - 1


def horizontal_pass(field_size):
    steps_east = 0
    while True:
        ensure_cactus_here()
        compare_horizontal(field_size)
        if has_east(field_size):
            move(EAST)
            steps_east = steps_east + 1
        else:
            break
    while steps_east > 0:
        move(WEST)
        steps_east = steps_east - 1


def sort_column(field_size):
    passes = field_size // 2
    if passes < 1:
        passes = 1
    index = 0
    while index < passes:
        vertical_pass(field_size)
        index = index + 1


def sort_row(field_size):
    passes = field_size // 2
    if passes < 1:
        passes = 1
    index = 0
    while index < passes:
        horizontal_pass(field_size)
        index = index + 1


def trigger_chain_harvest():
    if can_harvest():
        harvest()
        ensure_cactus_here()


def run_vertical_cycle(start_column, stride, field_size):
    column = start_column
    while column < field_size:
        move_to_column(column)
        move_to_row(0)
        sort_column(field_size)
        column = column + stride
    move_to_column(0)
    move_to_row(0)


def run_horizontal_cycle(start_row, stride, field_size):
    row = start_row
    while row < field_size:
        move_to_row(row)
        move_to_column(0)
        sort_row(field_size)
        row = row + stride
    move_to_row(0)
    move_to_column(0)


def worker_loop(start_index, field_size):
    while True:
        stride = get_active_stride()
        run_vertical_cycle(start_index, stride, field_size)
        run_horizontal_cycle(start_index, stride, field_size)
        move_to_row(0)
        move_to_column(0)
        trigger_chain_harvest()
        pets = 0
        while pets < PETS_PER_CYCLE:
            pet_the_piggy()
            pets = pets + 1


def make_worker(start_index, field_size):
    def run():
        worker_loop(start_index, field_size)

    return run


def main():
    field_size = get_world_size()
    max_available = max_drones()
    worker_target = choose_worker_count(max_available, field_size)
    set_active_stride(worker_target)
    active_workers = 1
    while active_workers < worker_target:
        worker = make_worker(active_workers, field_size)
        drone = spawn_drone(worker)
        if drone == None:
            set_active_stride(active_workers)
            break
        active_workers = active_workers + 1
    worker_loop(0, field_size)


main()
