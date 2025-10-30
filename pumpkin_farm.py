# ==================== Estratégia de colheita paralela de abóboras ====================

import plantacoes

TARGET_PATCH_SIZE = 6
STABLE_MEASUREMENTS = 4


def move_to_origin_row():
        while get_pos_y() > 0:
                move(South)
        return True


def move_to_column(column_index):
        move_to_origin_row()
        while get_pos_x() < column_index:
                move(East)
        while get_pos_x() > column_index:
                move(West)
        return True


def ensure_tracker_entry(tracker, key):
        if key not in tracker:
                tracker[key] = {}
        return tracker[key]


def ensure_tile_state(column_tracker, row_index):
        if row_index not in column_tracker:
                column_tracker[row_index] = {"last_size": 0, "stable_count": 0}
        return column_tracker[row_index]


def normalize_measurement(value):
        if value == None:
                return 0
        if value < 0:
                return 0
        return value


def reset_state(state):
        state["last_size"] = 0
        state["stable_count"] = 0
        return state


def should_harvest_pumpkin(state, current_size):
        last_size = state["last_size"]
        if current_size > last_size:
                state["last_size"] = current_size
                state["stable_count"] = 1
        elif current_size == last_size:
                state["stable_count"] = state["stable_count"] + 1
        else:
                state["last_size"] = current_size
                state["stable_count"] = 1
        if current_size >= TARGET_PATCH_SIZE:
                if state["stable_count"] >= STABLE_MEASUREMENTS:
                        if can_harvest():
                                return True
        return False


def replant_pumpkin(column_tracker, row_index):
        state = ensure_tile_state(column_tracker, row_index)
        reset_state(state)
        plantacoes.plant_pumpkin()
        return True


def clean_dead_pumpkin(column_tracker, row_index):
        if get_entity_type() == Entities.Dead_Pumpkin:
                harvest()
                replant_pumpkin(column_tracker, row_index)
                return True
        return False


def evaluate_pumpkin_tile(column_tracker, row_index):
        if clean_dead_pumpkin(column_tracker, row_index):
                return False
        if get_entity_type() != Entities.Pumpkin:
                replant_pumpkin(column_tracker, row_index)
                return False
        size_value = normalize_measurement(measure())
        state = ensure_tile_state(column_tracker, row_index)
        if should_harvest_pumpkin(state, size_value):
                harvest()
                replant_pumpkin(column_tracker, row_index)
                return True
        return False


def monitor_column(column_index, field_size, tracker):
        move_to_column(column_index)
        column_tracker = ensure_tracker_entry(tracker, column_index)
        row_index = 0
        while row_index < field_size:
                evaluate_pumpkin_tile(column_tracker, row_index)
                if row_index < field_size - 1:
                        move(North)
                row_index = row_index + 1
        steps_down = field_size - 1
        while steps_down > 0:
                move(South)
                steps_down = steps_down - 1
        return True


def column_worker(start_column, stride, field_size):
        tracker = {}
        column_index = start_column
        while True:
                while column_index < field_size:
                        monitor_column(column_index, field_size, tracker)
                        column_index = column_index + stride
                column_index = start_column
        return True


def make_worker(start_column, stride, field_size):
        def run():
                return column_worker(start_column, stride, field_size)
        return run


def main():
        field_size = get_world_size()
        max_slots = max_drones()
        if max_slots < 1:
                max_slots = 1
        active_workers = field_size
        if active_workers > max_slots:
                active_workers = max_slots
        stride = active_workers
        spawned = 1
        while spawned < active_workers:
                        worker_function = make_worker(spawned, stride, field_size)
                        drone = spawn_drone(worker_function)
                        if drone != None:
                                spawned = spawned + 1
                        else:
                                break
        column_worker(0, stride, field_size)


main()
