# Coordinated polyculture routine with shared request queue.

from directions import EAST, NORTH
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


def polyculture_scan():
    field_size = get_world_size()
    step = 0
    column = 0
    while column < field_size:
        row = 0
        while row < field_size:
            if can_harvest():
                harvest()
            handled = handle_requests_on_tile()
            if not handled:
                probe_and_record_request(step)
                step = step + 1
            move(NORTH)
            row = row + 1
        move(EAST)
        column = column + 1


def main():
    while True:
        polyculture_scan()
        polyculture_scan()


main()
