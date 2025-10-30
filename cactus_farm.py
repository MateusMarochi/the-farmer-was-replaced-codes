import plantacoes

WORLD_SIZE = 32
PREFERRED_DRONES = (32, 16)
VERTICAL_SWEEP_PASSES = WORLD_SIZE // 2
HORIZONTAL_SWEEP_PASSES = WORLD_SIZE // 2
PETS_PER_CYCLE = 10

ACTIVE_STRIDE = 1


def ensure_world_size():
    if "set_world_size" in globals():
        set_world_size(WORLD_SIZE)
    return get_world_size()


def choose_worker_count(max_available, field_size):
    for preferred in PREFERRED_DRONES:
        if max_available >= preferred and field_size >= preferred:
            return preferred
    if max_available < 1:
        return 1
    if field_size < 1:
        return 1
    if max_available < field_size:
        return max_available
    return field_size


def set_active_stride(value):
    global ACTIVE_STRIDE
    ACTIVE_STRIDE = max(1, value)


def get_active_stride():
    return ACTIVE_STRIDE


def move_to_column(target_column):
    while get_pos_x() < target_column:
        move(East)
    while get_pos_x() > target_column:
        move(West)


def move_to_row(target_row):
    while get_pos_y() < target_row:
        move(North)
    while get_pos_y() > target_row:
        move(South)


def ensure_cactus_here():
    if get_entity_type() != Entities.Cactus:
        if can_harvest():
            harvest()
        plantacoes.plant_cactus()


def safe_measure(direction=None):
    if direction is None:
        value = measure()
    else:
        value = measure(direction)
    if value is None:
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
        north_value = safe_measure(North)
        if current_value > north_value:
            swap(North)
            current_value = safe_measure()
    if has_south():
        south_value = safe_measure(South)
        if current_value < south_value:
            swap(South)


def compare_horizontal(field_size):
    current_value = safe_measure()
    if has_east(field_size):
        east_value = safe_measure(East)
        if current_value > east_value:
            swap(East)
            current_value = safe_measure()
    if has_west():
        west_value = safe_measure(West)
        if current_value < west_value:
            swap(West)


def vertical_pass(field_size):
    steps_up = 0
    while True:
        ensure_cactus_here()
        compare_vertical(field_size)
        if has_north(field_size):
            move(North)
            steps_up += 1
        else:
            break
    while steps_up > 0:
        move(South)
        steps_up -= 1


def horizontal_pass(field_size):
    steps_east = 0
    while True:
        ensure_cactus_here()
        compare_horizontal(field_size)
        if has_east(field_size):
            move(East)
            steps_east += 1
        else:
            break
    while steps_east > 0:
        move(West)
        steps_east -= 1


def sort_column(field_size):
    for _ in range(VERTICAL_SWEEP_PASSES):
        vertical_pass(field_size)


def sort_row(field_size):
    for _ in range(HORIZONTAL_SWEEP_PASSES):
        horizontal_pass(field_size)


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
        column += stride
    move_to_column(0)
    move_to_row(0)


def run_horizontal_cycle(start_row, stride, field_size):
    row = start_row
    while row < field_size:
        move_to_row(row)
        move_to_column(0)
        sort_row(field_size)
        row += stride
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
        for _ in range(PETS_PER_CYCLE):
            pet_the_piggy()


def make_worker(start_index, field_size):
    def run():
        worker_loop(start_index, field_size)
    return run


def main():
    field_size = ensure_world_size()
    max_available = max_drones()
    worker_target = choose_worker_count(max_available, field_size)
    set_active_stride(worker_target)
    active_workers = 1
    while active_workers < worker_target:
        worker = make_worker(active_workers, field_size)
        drone = spawn_drone(worker)
        if drone is None:
            set_active_stride(active_workers)
            break
        active_workers += 1
    worker_loop(0, field_size)


main()
