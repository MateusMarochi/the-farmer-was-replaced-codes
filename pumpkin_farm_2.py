"""Rotina parametrizada para a fazenda de abóboras.

Altere WORLD_SIZE e DRONE_TARGET conforme desejado:
- WORLD_SIZE: 22 ou 32.
- DRONE_TARGET: 16 para a malha compacta ou 32 para a malha completa.

A versão completa reproduz o layout original otimizado para 32 drones.
A versão compacta posiciona 15 drones auxiliares (8 patch, 2 horizontais,
2 verticais e 3 mini) e utiliza o drone principal como o 16º operador.
"""

WORLD_SIZE = 32
DRONE_TARGET = 32  # Use 16 para a versão compacta.


def move_steps(direction, steps):
    """Movimenta o drone principal várias vezes na mesma direção."""
    for _ in range(steps):
        move(direction)


def minipatch_drone():
    top = 0
    bottom = 0
    change_hat(Hats.Green_Hat)
    while True:
        for row in range(4):
            for column in range(4):
                if get_entity_type() != Entities.Pumpkin:
                    plant(Entities.Pumpkin)
                if row == 0 and column == 0:
                    top = measure()
                elif row == 2 and column == 2:
                    bottom = measure()
                move(East)
            move_steps(West, 4)
            move(North)
        move_steps(South, 4)
        if top == bottom and can_harvest():
            harvest()


def patch_drone():
    top = 0
    bottom = 0
    change_hat(Hats.Purple_Hat)
    while True:
        for row in range(6):
            for column in range(6):
                if get_entity_type() != Entities.Pumpkin:
                    plant(Entities.Pumpkin)
                if row == 0 and column == 0:
                    top = measure()
                elif row == 4 and column == 4:
                    bottom = measure()
                move(East)
            move_steps(West, 6)
            move(North)
        move_steps(South, 6)
        if top == bottom and can_harvest():
            harvest()


def prep_drone():
    for _ in range(get_world_size()):
        if get_ground_type() != Grounds.Soil:
            till()
        move(North)


def horizontal_sunflower_drone():
    change_hat(Hats.Gray_Hat)
    while True:
        for _ in range(get_world_size()):
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Sunflower)
            move(East)


def vertical_sunflower_drone():
    change_hat(Hats.Traffic_Cone)
    while True:
        for _ in range(get_world_size()):
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Sunflower)
            move(North)


def deploy_full_layout_32():
    for _ in range(31):
        spawn_drone(prep_drone)
        move(East)
    do_a_flip()
    spawn_drone(prep_drone)
    move(East)

    for _ in range(4):
        spawn_drone(patch_drone)
        move_steps(East, 6)
        spawn_drone(vertical_sunflower_drone)
        move(East)
    spawn_drone(minipatch_drone)
    move_steps(East, 4)
    move_steps(North, 6)
    spawn_drone(horizontal_sunflower_drone)
    move(North)

    for _ in range(3):
        for _ in range(4):
            spawn_drone(patch_drone)
            move_steps(East, 6)
            move(East)
        spawn_drone(minipatch_drone)
        move_steps(East, 4)
        move_steps(North, 6)
        spawn_drone(horizontal_sunflower_drone)
        move(North)

    for _ in range(3):
        spawn_drone(minipatch_drone)
        move_steps(East, 7)


def deploy_compact_layout(world_size):
    for column in range(world_size):
        spawn_drone(prep_drone)
        if column < world_size - 1:
            move(East)
    do_a_flip()
    move_steps(West, world_size - 1)
    do_a_flip()

    patch_columns = 2
    patch_rows = 4
    patch_width = 6
    gap = 4
    row_width = patch_columns * patch_width + (patch_columns - 1) * gap

    for row in range(patch_rows):
        for column in range(patch_columns):
            spawn_drone(patch_drone)
            move_steps(East, patch_width)
            if row == 0 and column < patch_columns:
                spawn_drone(vertical_sunflower_drone)
            if column < patch_columns - 1:
                move_steps(East, gap)
        if row in (0, 2):
            spawn_drone(minipatch_drone)
        move_steps(West, row_width)
        if row < patch_rows - 1:
            move_steps(North, patch_width)
            if row in (0, 2):
                spawn_drone(horizontal_sunflower_drone)
            move(North)

    spawn_drone(minipatch_drone)
    move_steps(South, (patch_rows - 1) * (patch_width + 1))


def maintain_minipatch_cycle():
    while True:
        top = 0
        bottom = 0
        change_hat(Hats.Green_Hat)
        for row in range(4):
            for column in range(4):
                if get_entity_type() != Entities.Pumpkin:
                    plant(Entities.Pumpkin)
                if row == 0 and column == 0:
                    top = measure()
                elif row == 2 and column == 2:
                    bottom = measure()
                move(East)
            move_steps(West, 4)
            move(North)
        move_steps(South, 4)
        if top == bottom and can_harvest():
            harvest()


set_world_size(WORLD_SIZE)
clear()

if DRONE_TARGET == 32:
    if WORLD_SIZE != 32:
        raise ValueError("O layout completo requer um mundo 32x32.")
    deploy_full_layout_32()
elif DRONE_TARGET == 16:
    if WORLD_SIZE not in (22, 32):
        raise ValueError("A malha compacta aceita mundos 22x22 ou 32x32.")
    deploy_compact_layout(WORLD_SIZE)
else:
    raise ValueError("Configure DRONE_TARGET como 16 ou 32.")

maintain_minipatch_cycle()
