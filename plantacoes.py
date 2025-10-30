# Helper planting routines shared by multiple strategies.


def ensure_soil():
    if get_ground_type() != Grounds.SOIL:
        till()


def ensure_grassland():
    if get_ground_type() != Grounds.GRASSLAND:
        till()


def plant_grass():
    ensure_grassland()
    plant(Entities.GRASS)


def plant_tree():
    ensure_grassland()
    plant(Entities.TREE)
    if get_water() < 0.75:
        use_item(Items.WATER)


def plant_carrot():
    ensure_soil()
    plant(Entities.CARROT)


def plant_pumpkin():
    ensure_soil()
    plant(Entities.PUMPKIN)


def plant_sunflower():
    ensure_soil()
    plant(Entities.SUNFLOWER)
    if get_water() < 0.5:
        use_item(Items.WATER)


def plant_cactus():
    ensure_soil()
    plant(Entities.CACTUS)


def plant_apple():
    ensure_soil()
    plant(Entities.APPLE)
    if get_water() < 0.5:
        use_item(Items.WATER)
