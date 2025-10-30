# Extended treasure hunt with heading spins and straight segments.

from directions import EAST, NORTH, SOUTH, WEST


def create_maze():
    clear()
    plant(Entities.BUSH)
    unlock_level = num_unlocked(Unlocks.MAZES)
    amount = get_world_size() * 2 ** (unlock_level - 1)
    use_item(Items.WEIRD_SUBSTANCE, amount)


def next_clockwise(direction):
    if direction == NORTH:
        return EAST
    if direction == EAST:
        return SOUTH
    if direction == SOUTH:
        return WEST
    if direction == WEST:
        return NORTH
    return direction


def next_counter_clockwise(direction):
    if direction == NORTH:
        return WEST
    if direction == WEST:
        return SOUTH
    if direction == SOUTH:
        return EAST
    if direction == EAST:
        return NORTH
    return direction


def treasure_hunt_worker(
    start_direction,
    prefer_clockwise,
    warmup_steps,
    start_spin,
    turn_every,
):
    direction = start_direction
    spin_step = 0
    while spin_step < start_spin:
        if prefer_clockwise:
            direction = next_clockwise(direction)
        else:
            direction = next_counter_clockwise(direction)
        spin_step = spin_step + 1
    warmup_index = 0
    while warmup_index < warmup_steps:
        move(direction)
        warmup_index = warmup_index + 1
    last_x = get_pos_x()
    last_y = get_pos_y()
    moves_since_turn = 0
    while True:
        move(direction)
        current_x = get_pos_x()
        current_y = get_pos_y()
        if last_x == current_x and last_y == current_y:
            if prefer_clockwise:
                direction = next_clockwise(direction)
            else:
                direction = next_counter_clockwise(direction)
            move(direction)
            pushed_x = get_pos_x()
            pushed_y = get_pos_y()
            if pushed_x != last_x or pushed_y != last_y:
                last_x = pushed_x
                last_y = pushed_y
                moves_since_turn = 1
                if moves_since_turn >= turn_every:
                    if prefer_clockwise:
                        direction = next_counter_clockwise(direction)
                    else:
                        direction = next_clockwise(direction)
                    moves_since_turn = 0
        else:
            last_x = current_x
            last_y = current_y
            moves_since_turn = moves_since_turn + 1
            if moves_since_turn >= turn_every:
                if prefer_clockwise:
                    direction = next_counter_clockwise(direction)
                else:
                    direction = next_clockwise(direction)
                moves_since_turn = 0
        if get_entity_type() == Entities.TREASURE:
            harvest()
            return True


def make_runner(
    start_direction, prefer_clockwise, warmup_steps, start_spin, turn_every
):
    def run():
        return treasure_hunt_worker(
            start_direction,
            prefer_clockwise,
            warmup_steps,
            start_spin,
            turn_every,
        )

    return run


def treasure_hunt_parallel():
    drone_limit = max_drones()
    if drone_limit < 1:
        drone_limit = 1
    drones = []
    index = 0
    while index < drone_limit:
        remainder = index % 4
        if remainder == 0:
            base_direction = WEST
        elif remainder == 1:
            base_direction = NORTH
        elif remainder == 2:
            base_direction = EAST
        else:
            base_direction = SOUTH
        if index >= 4:
            start_direction = next_clockwise(base_direction)
        else:
            start_direction = base_direction
        if index % 2 == 0:
            prefer_clockwise = False
        else:
            prefer_clockwise = True
        warmup_steps = index % 4
        start_spin = (index // 2) % 4
        if index % 3 == 0:
            turn_every = 1
        elif index % 3 == 1:
            turn_every = 2
        else:
            turn_every = 3
        runner = make_runner(
            start_direction,
            prefer_clockwise,
            warmup_steps,
            start_spin,
            turn_every,
        )
        drone = spawn_drone(runner)
        if drone != None:
            drones.append(drone)
        index = index + 1
    found = False
    while not found:
        scan_index = 0
        while scan_index < len(drones):
            drone = drones[scan_index]
            if drone != None and has_finished(drone):
                result = wait_for(drone)
                if result:
                    found = True
                    break
            scan_index = scan_index + 1


def main():
    while True:
        create_maze()
        treasure_hunt_parallel()


main()
