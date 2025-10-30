# Parallel polyculture routine with reserved sunflower columns.

from directions import EAST, NORTH, SOUTH, WEST
import plantacoes

requests_queue = []


def plant_bush_fallback():
    if get_ground_type() != Grounds.GRASSLAND:
        till()
    plant(Entities.BUSH)


def plant_entity(entity_type):
    if entity_type == Entities.GRASS:
        plantacoes.plant_grass()
    elif entity_type == Entities.TREE:
        plantacoes.plant_tree()
    elif entity_type == Entities.CARROT:
        plantacoes.plant_carrot()
    elif entity_type == Entities.BUSH:
        plant_bush_fallback()
    elif entity_type == Entities.SUNFLOWER:
        plantacoes.plant_sunflower()
    else:
        plant(entity_type)


def probe_cycle(step):
    remainder = step % 4
    if remainder == 0:
        return Entities.GRASS
    if remainder == 1:
        return Entities.TREE
    if remainder == 2:
        return Entities.CARROT
    return Entities.BUSH


def handle_requests_on_tile():
    x_position = get_pos_x()
    y_position = get_pos_y()
    handled = False
    copy_queue = []
    index = 0
    while index < len(requests_queue):
        copy_queue.append(requests_queue[index])
        index = index + 1
    index = 0
    while index < len(copy_queue):
        request = copy_queue[index]
        target_x, target_y, entity_type = request
        if target_x == x_position and target_y == y_position:
            plant_entity(entity_type)
            if can_harvest():
                harvest()
            requests_queue.remove(request)
            handled = True
        index = index + 1
    return handled


def probe_and_record_request(step):
    entity_type = probe_cycle(step)
    plant_entity(entity_type)
    companion = get_companion()
    if companion != None:
        target_type, position = companion
        target_x = position[0]
        target_y = position[1]
        exists = False
        index = 0
        while index < len(requests_queue):
            request = requests_queue[index]
            if request[0] == target_x and request[1] == target_y:
                exists = True
            index = index + 1
        if not exists:
            requests_queue.append((target_x, target_y, target_type))


def move_to(target_x, target_y):
    while get_pos_x() < target_x:
        move(EAST)
    while get_pos_x() > target_x:
        move(WEST)
    while get_pos_y() < target_y:
        move(NORTH)
    while get_pos_y() > target_y:
        move(SOUTH)


def process_tile(step_ref):
    if can_harvest():
        harvest()
    field_size = get_world_size()
    x_position = get_pos_x()
    if x_position >= field_size - 2:
        plant_entity(Entities.SUNFLOWER)
        return
    handled = handle_requests_on_tile()
    if not handled:
        probe_and_record_request(step_ref[0])
        step_ref[0] = step_ref[0] + 1


def column_pair_worker(start_column):
    field_size = get_world_size()
    move_to(start_column, 0)
    step_ref = [0]
    while True:
        row = 0
        while row < field_size:
            process_tile(step_ref)
            if row < field_size - 1:
                move(NORTH)
            row = row + 1
        move(EAST)
        row = 0
        while row < field_size:
            process_tile(step_ref)
            if row < field_size - 1:
                move(SOUTH)
            row = row + 1
        move(WEST)


def make_runner(start_column):
    def run():
        column_pair_worker(start_column)

    return run


def orchestrate_workers():
    field_size = get_world_size()
    drones = []
    max_available = max_drones()
    if max_available < 1:
        max_available = 1
    target_pairs = field_size // 2
    if target_pairs > max_available:
        target_pairs = max_available
    index = 0
    while index < target_pairs:
        start_column = index * 2
        runner = make_runner(start_column)
        drone = spawn_drone(runner)
        if drone != None:
            drones.append(drone)
        index = index + 1
    while True:
        move_to(0, 0)


def main():
    orchestrate_workers()


main()
