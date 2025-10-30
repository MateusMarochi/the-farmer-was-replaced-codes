set_world_size(32)
clear()


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
                        for home in range(4):
                                move(West)
                        move(North)
                for home in range(4):
                        move(South)
                if top == bottom:
                        if can_harvest():
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
                        for home in range(6):
                                move(West)
                        move(North)
                for home in range(6):
                        move(South)
                if top == bottom:
                        if can_harvest():
                                harvest()


def prep_drone():
        for row in range(get_world_size()):
                if get_ground_type() != Grounds.Soil:
                        till()
                move(North)


def horizontal_sunflower_drone():
        change_hat(Hats.Gray_Hat)
        while True:
                for column in range(get_world_size()):
                        if can_harvest():
                                harvest()
                        if get_ground_type() != Grounds.Soil:
                                till()
                        plant(Entities.Sunflower)
                        move(East)


def vertical_sunflower_drone():
        change_hat(Hats.Traffic_Cone)
        while True:
                for row in range(get_world_size()):
                        if can_harvest():
                                harvest()
                        if get_ground_type() != Grounds.Soil:
                                till()
                        plant(Entities.Sunflower)
                        move(North)


# MAIN
for column in range(31):
        spawn_drone(prep_drone)
        move(East)

do_a_flip()
spawn_drone(prep_drone)
move(East)

for layout in range(4):
        spawn_drone(patch_drone)
        for travel in range(6):
                move(East)
        spawn_drone(vertical_sunflower_drone)
        move(East)
spawn_drone(minipatch_drone)
for hop in range(4):
        move(East)
for skip in range(6):
        move(North)
spawn_drone(horizontal_sunflower_drone)
move(North)

for extra_layout in range(3):
        for layout in range(4):
                spawn_drone(patch_drone)
                for travel in range(6):
                        move(East)
                move(East)
        spawn_drone(minipatch_drone)
        for hop in range(4):
                move(East)
        for skip in range(6):
                move(North)
        spawn_drone(horizontal_sunflower_drone)
        move(North)

for topper in range(3):
        spawn_drone(minipatch_drone)
        for jump in range(7):
                move(East)

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
                for home in range(4):
                        move(West)
                move(North)
        for home in range(4):
                move(South)
        if top == bottom:
                if can_harvest():
                        harvest()
