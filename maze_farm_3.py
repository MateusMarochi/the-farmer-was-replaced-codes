# ------------------- Estado compartilhado -------------------


MAZE_READY = False


# ------------------- Geração do labirinto (SEM chamar hunt aqui) -------------------


def create_maze():
    global MAZE_READY
    clear()
    plant(Entities.Bush)
    substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)
    MAZE_READY = True
    return True


# ------------------- Posicionamento inicial -------------------


def move_axis(direction, steps):
    count = 0
    while count < steps:
        moved = move(direction)
        if not moved:
            return False
        count = count + 1
    return True


def move_to_center():
    size = get_world_size()
    half = size // 2

    moved_horizontal = move_axis(East, half)
    if not moved_horizontal:
        return False

    moved_vertical = move_axis(South, half)
    if not moved_vertical:
        return False

    return True


# ------------------- Helpers de direção (sem lambda/ternário) -------------------


def next_cw(d):
    if d == North:
        return East
    elif d == East:
        return South
    elif d == South:
        return West
    elif d == West:
        return North
    return d


def next_ccw(d):
    if d == North:
        return West
    elif d == West:
        return South
    elif d == South:
        return East
    elif d == East:
        return North
    return d


# ------------------- Posicionamento auxiliar -------------------


def move_to_position(target_x, target_y):
    current_x = get_pos_x()
    while current_x < target_x:
        moved = move(East)
        if not moved:
            return False
        current_x = get_pos_x()
    while current_x > target_x:
        moved = move(West)
        if not moved:
            return False
        current_x = get_pos_x()

    current_y = get_pos_y()
    while current_y < target_y:
        moved = move(South)
        if not moved:
            return False
        current_y = get_pos_y()
    while current_y > target_y:
        moved = move(North)
        if not moved:
            return False
        current_y = get_pos_y()

    return True


def compute_edge_offsets(radius):
    offsets = []
    if radius <= 0:
        offsets.append(0)
        return offsets
    steps = 7
    index = 0
    while index <= steps:
        numerator = 2 * radius * index
        base = numerator // steps
        offset = base - radius
        offsets.append(offset)
        index = index + 1
    return offsets


def clamp_edge_coordinate(value, low_limit, high_limit):
    if value < low_limit:
        return low_limit
    if value > high_limit:
        return high_limit
    return value


def build_distribution_positions(center_x, center_y, radius):
    positions = []
    if radius <= 0:
        single = (center_x, center_y)
        positions.append(single)
        return positions

    offsets = compute_edge_offsets(radius)
    top_y = center_y - radius
    bottom_y = center_y + radius
    left_x = center_x - radius
    right_x = center_x + radius

    count = len(offsets)
    index = 0
    while index < count:
        value = offsets[index]
        x_pos = center_x + value
        positions.append((x_pos, top_y))
        index = index + 1

    index = 0
    while index < count:
        value = offsets[index]
        x_pos = center_x + value
        positions.append((x_pos, bottom_y))
        index = index + 1

    index = 0
    while index < count:
        value = offsets[index]
        y_pos = center_y + value
        adjusted = y_pos
        if adjusted == top_y:
            adjusted = adjusted + 1
        elif adjusted == bottom_y:
            adjusted = adjusted - 1
        adjusted = clamp_edge_coordinate(adjusted, top_y, bottom_y)
        positions.append((left_x, adjusted))
        index = index + 1

    index = 0
    while index < count:
        value = offsets[index]
        y_pos = center_y + value
        adjusted = y_pos
        if adjusted == top_y:
            adjusted = adjusted + 1
        elif adjusted == bottom_y:
            adjusted = adjusted - 1
        adjusted = clamp_edge_coordinate(adjusted, top_y, bottom_y)
        positions.append((right_x, adjusted))
        index = index + 1

    return positions


def determine_start_direction(center_x, center_y, target_x, target_y):
    if target_x > center_x:
        return East
    if target_x < center_x:
        return West
    if target_y > center_y:
        return South
    if target_y < center_y:
        return North
    return North


def wait_cycles(amount):
    waited = 0
    while waited < amount:
        get_pos_x()
        waited = waited + 1
    return True


def idle_until_maze_ready():
    global MAZE_READY
    while not MAZE_READY:
        get_pos_y()
    return True


# ------------------- Algoritmo BASE da caça (worker do drone) -------------------
def treasure_hunt_worker(
    index,
    target_x,
    target_y,
    start_dir,
    prefer_cw,
    delay_cycles,
):
    wait_cycles(delay_cycles)
    move_to_position(target_x, target_y)
    idle_until_maze_ready()

    dir = start_dir
    x = get_pos_x()
    y = get_pos_y()

    while True:
        if get_entity_type() == Entities.Treasure:
            harvest()
            return True

        side_dir = next_cw(dir)
        if not prefer_cw:
            side_dir = next_ccw(dir)

        move(side_dir)
        sx = get_pos_x()
        sy = get_pos_y()
        if sx != x or sy != y:
            dir = side_dir
            x = sx
            y = sy
            continue

        move(dir)
        fx = get_pos_x()
        fy = get_pos_y()
        if fx != x or fy != y:
            x = fx
            y = fy
            continue

        if prefer_cw:
            dir = next_ccw(dir)
        else:
            dir = next_cw(dir)


# ------------------- Envoltório para spawn_drone (sem lambda) -------------------


def make_runner(
    index,
    target_x,
    target_y,
    start_dir,
    prefer_cw,
    delay_cycles,
):
    # Retorna a função que o drone deve executar com os parâmetros fixados
    def run():
        return treasure_hunt_worker(
            index,
            target_x,
            target_y,
            start_dir,
            prefer_cw,
            delay_cycles,
        )

    return run


# ------------------- Coordenador paralelo: primeiro que terminar ganha -------------------


def treasure_hunt_parallel():
    global MAZE_READY
    MAZE_READY = False

    move_to_center()
    center_x = get_pos_x()
    center_y = get_pos_y()

    world_size = get_world_size()
    radius = world_size // 2
    if radius > 1:
        radius = radius - 1

    positions = build_distribution_positions(center_x, center_y, radius)

    drones = []

    max_slots = max_drones()
    if max_slots < 1:
        max_slots = 1

    total_positions = len(positions)
    limit = max_slots
    if limit > total_positions:
        limit = total_positions

    index = 0
    while index < limit:
        target = positions[index]
        target_x = target[0]
        target_y = target[1]
        start_dir = determine_start_direction(center_x, center_y, target_x, target_y)

        if index % 2 == 0:
            prefer_cw = True
        else:
            prefer_cw = False

        delay = index % 8

        func = make_runner(
            index,
            target_x,
            target_y,
            start_dir,
            prefer_cw,
            delay,
        )
        d = spawn_drone(func)
        if d != None:
            drones.append(d)
        else:
            break
        index = index + 1

    created = create_maze()
    if not created:
        return False

    found = False
    while not found:
        j = 0
        while j < len(drones):
            d = drones[j]
            if d != None and has_finished(d):
                res = wait_for(d)
                if res:
                    found = True
                    break
            j = j + 1

    return True


# ------------------- Loop principal -------------------


def main():
    while True:
        got = treasure_hunt_parallel()
        if got:
            continue


main()
