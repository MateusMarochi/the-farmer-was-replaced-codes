"""Fazenda de girassóis com 32 drones em um campo 32x32."""

import plantacoes

WORLD_SIZE = 32
DRONE_COUNT = 32


def ensure_world_size(expected_size):
        if "set_world_size" in globals():
                set_world_size(expected_size)
        size = get_world_size()
        if size != expected_size:
                raise ValueError("O tamanho do mundo precisa ser 32x32.")
        return size


def move_to_column(target_column):
        while get_pos_x() < target_column:
                move(East)
        while get_pos_x() > target_column:
                move(West)
        return True


def move_to_row(target_row):
        while get_pos_y() < target_row:
                move(North)
        while get_pos_y() > target_row:
                move(South)
        return True


def maintain_sunflower_tile():
        if get_entity_type() != Entities.Sunflower:
                if can_harvest():
                        harvest()
                plantacoes.plant_sunflower()
        else:
                if can_harvest():
                        harvest()
                        plantacoes.plant_sunflower()
        return True


def sunflower_column_worker(column_index, field_size):
        move_to_column(column_index)
        move_to_row(0)
        while True:
                row = 0
                while row < field_size:
                        maintain_sunflower_tile()
                        if row < field_size - 1:
                                move(North)
                        row = row + 1
                move_to_row(0)


def make_sunflower_worker(column_index, field_size):
        def runner():
                return sunflower_column_worker(column_index, field_size)
        return runner


def deploy_sunflower_farm(field_size, drone_target):
        column = 0
        limit = min(field_size, drone_target)
        while column < limit:
                runner = make_sunflower_worker(column, field_size)
                drone = spawn_drone(runner)
                if drone == None:
                        break
                column = column + 1
        return True


def main():
        size = ensure_world_size(WORLD_SIZE)
        clear()
        deploy_sunflower_farm(size, DRONE_COUNT)
        while True:
                move_to_column(0)
                move_to_row(0)


main()
