# Variant treasure hunt with increased spawn count.


def create_maze():
    clear()
    plant(Entities.BUSH)
    unlock_level = num_unlocked(Unlocks.MAZES)
    amount = get_world_size() * 2 ** (unlock_level - 1)
    use_item(Items.WEIRD_SUBSTANCE, amount)


def next_clockwise(direction):
    if direction == Direction.NORTH:
        return Direction.EAST
    if direction == Direction.EAST:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.NORTH
    return direction


def next_counter_clockwise(direction):
    if direction == Direction.NORTH:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.EAST
    if direction == Direction.EAST:
        return Direction.NORTH
    return direction


def treasure_hunt_worker(start_direction, prefer_clockwise, warmup_steps):
    direction = start_direction
    step = 0
    while step < warmup_steps:
        move(direction)
        step = step + 1
    last_x = get_pos_x()
    last_y = get_pos_y()
    while True:
        move(direction)
        current_x = get_pos_x()
        current_y = get_pos_y()
        if last_x == current_x and last_y == current_y:
            if prefer_clockwise:
                direction = next_clockwise(direction)
            else:
                direction = next_counter_clockwise(direction)
        else:
            last_x = current_x
            last_y = current_y
            if prefer_clockwise:
                direction = next_counter_clockwise(direction)
            else:
                direction = next_clockwise(direction)
        if get_entity_type() == Entities.TREASURE:
            harvest()
            return True


def make_runner(start_direction, prefer_clockwise, warmup_steps):
    def run():
        return treasure_hunt_worker(start_direction, prefer_clockwise, warmup_steps)

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
            start_direction = Direction.WEST
        elif remainder == 1:
            start_direction = Direction.NORTH
        elif remainder == 2:
            start_direction = Direction.EAST
        else:
            start_direction = Direction.SOUTH
        if index % 2 == 0:
            prefer_clockwise = False
        else:
            prefer_clockwise = True
        warmup_steps = index
        runner = make_runner(start_direction, prefer_clockwise, warmup_steps)
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
