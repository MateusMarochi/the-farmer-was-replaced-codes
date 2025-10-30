"""Stubs that mirror the scripting API used by *The Farmer Was Replaced*.

These helpers do not attempt to emulate any in-game behaviour. They exist so
that strategy scripts contained in this repository can be executed as regular
Python modules without immediately failing due to missing symbols. Each
function exposes the signature documented on the official wiki and returns a
simple placeholder value that matches the documented return type.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional
import warnings


class Direction(str, Enum):
    """Cardinal movement directions for the drone."""

    EAST = "East"
    WEST = "West"
    NORTH = "North"
    SOUTH = "South"


# Compatibility aliases mirroring in-game constant names
East = Direction.EAST
West = Direction.WEST
North = Direction.NORTH
South = Direction.SOUTH


class Entities(str, Enum):
    """All entities that may occupy a farm tile."""

    BUSH = "Bush"
    CARROT = "Carrot"
    GRASS = "Grass"
    HEDGE = "Hedge"
    DEAD_PUMPKIN = "Dead_Pumpkin"
    Dead_Pumpkin = "Dead_Pumpkin"
    PUMPKIN = "Pumpkin"
    Pumpkin = "Pumpkin"
    SUNFLOWER = "Sunflower"
    TREASURE = "Treasure"
    TREE = "Tree"


class Grounds(str, Enum):
    """Ground types that can be present beneath the drone."""

    SOIL = "Soil"
    GRASSLAND = "Grassland"


class Items(str, Enum):
    """Inventory items available in the game."""

    CARROT = "Carrot"
    CARROT_SEED = "Carrot_Seed"
    EMPTY_TANK = "Empty_Tank"
    FERTILIZER = "Fertilizer"
    GOLD = "Gold"
    HAY = "Hay"
    PIGGY = "Piggy"
    POWER = "Power"
    PUMPKIN = "Pumpkin"
    PUMPKIN_SEED = "Pumpkin_Seed"
    SUNFLOWER_SEED = "Sunflower_Seed"
    WATER_TANK = "Water_Tank"
    WOOD = "Wood"


class Unlocks(str, Enum):
    """Research unlocks and upgrades."""

    AUTO_UNLOCK = "Auto_Unlock"
    CARROTS = "Carrots"
    COST_LISTS = "Cost_Lists"
    DEBUG = "Debug"
    EXPAND = "Expand"
    FERTILIZER = "Fertilizer"
    GRASS = "Grass"
    LISTS = "Lists"
    LOOPS = "Loops"
    MAZES = "Mazes"
    MULTI_TRADE = "Multi_Trade"
    OPERATORS = "Operators"
    PLANT = "Plant"
    POLYCULTURE = "Polyculture"
    PUMPKINS = "Pumpkins"
    RESET = "Reset"
    SENSES = "Senses"
    SPEED = "Speed"
    SUNFLOWERS = "Sunflowers"
    TIMED_RESET = "Timed_Reset"
    TREES = "Trees"
    VARIABLES = "Variables"
    WATERING = "Watering"


class Hats(str, Enum):
    """Drone hats available for cosmetic changes."""

    CARROT_HAT = "Carrot_Hat"
    DINOSAUR_HAT = "Dinosaur_Hat"


def _stub_warning(name: str) -> None:
    warnings.warn(f"{name}() is a placeholder stub and has no effect.")


def can_harvest() -> bool:
    """Return whether the entity under the drone is ready for harvesting."""

    _stub_warning("can_harvest")
    return False


def clear() -> None:
    """Reset the field and position the drone at the origin."""

    _stub_warning("clear")


def do_a_flip() -> None:
    """Trigger the drone flip animation."""

    _stub_warning("do_a_flip")


def get_companion() -> Optional[List[object]]:
    """Return the companion preference information for the current plant."""

    _stub_warning("get_companion")
    return None


def get_cost(thing: object) -> Dict[object, int]:
    """Return a cost breakdown for the given unlock, entity or item."""

    _stub_warning("get_cost")
    return {}


def get_entity_type() -> Optional[Entities]:
    """Return the entity located under the drone, if any."""

    _stub_warning("get_entity_type")
    return None


def get_ground_type() -> Grounds:
    """Return the ground type under the drone."""

    _stub_warning("get_ground_type")
    return Grounds.GRASSLAND


def get_pos_x() -> int:
    """Return the current x-coordinate of the drone."""

    _stub_warning("get_pos_x")
    return 0


def get_pos_y() -> int:
    """Return the current y-coordinate of the drone."""

    _stub_warning("get_pos_y")
    return 0


def get_time() -> float:
    """Return the elapsed game time in seconds."""

    _stub_warning("get_time")
    return 0.0


def get_water() -> float:
    """Return the soil water level beneath the drone (between 0 and 1)."""

    _stub_warning("get_water")
    return 0.0


def get_world_size() -> int:
    """Return the edge length of the square farm grid."""

    _stub_warning("get_world_size")
    return 1


def harvest() -> bool:
    """Harvest the entity under the drone and report if something was removed."""

    _stub_warning("harvest")
    return False


def measure() -> Optional[int]:
    """Measure entity-specific metrics, such as sunflower petal counts."""

    _stub_warning("measure")
    return None


def move(direction: Direction | str) -> bool:
    """Move the drone a single tile in the requested direction."""

    _stub_warning("move")
    return False


def num_drones() -> int:
    """Return the number of drones currently active on the farm."""

    _stub_warning("num_drones")
    return 1


def num_items(item: Items) -> int:
    """Return how many copies of *item* are currently in the inventory."""

    _stub_warning("num_items")
    return 0


def num_unlocked(thing: object) -> int:
    """Return the unlock count for upgrades, entities, grounds or items."""

    _stub_warning("num_unlocked")
    return 0


def plant(entity: Optional[Entities] = None) -> bool:
    """Attempt to plant *entity* on the tile beneath the drone."""

    _stub_warning("plant")
    return False


def quick_print(*values: object) -> None:
    """Print values instantly to the output page without smoke text."""

    _stub_warning("quick_print")


def spawn_drone(function) -> Optional[int]:
    """Spawn a new drone to execute *function* and return its identifier."""

    _stub_warning("spawn_drone")
    return None


def wait_for(drone: Optional[int]):
    """Wait for *drone* to finish execution and return its result."""

    _stub_warning("wait_for")
    return None


def has_finished(drone: Optional[int]) -> bool:
    """Return whether *drone* has finished running."""

    _stub_warning("has_finished")
    return True


def till() -> None:
    """Toggle tilling of the ground beneath the drone."""

    _stub_warning("till")


def max_drones() -> int:
    """Return the maximum number of simultaneous drones allowed."""

    _stub_warning("max_drones")
    return 1


def timed_reset() -> None:
    """Start a timed run and revert the farm to its previous state afterwards."""

    _stub_warning("timed_reset")


def trade(item: Items, amount: Optional[int] = None) -> bool:
    """Attempt to purchase one or more copies of an item."""

    _stub_warning("trade")
    return False


def unlock(unlockable: Unlocks) -> bool:
    """Attempt to unlock or upgrade a research node."""

    _stub_warning("unlock")
    return False


def use_item(item: Items) -> bool:
    """Consume one unit of *item*, if possible."""

    _stub_warning("use_item")
    return False


__all__ = [
    "Direction",
    "Entities",
    "Grounds",
    "Items",
    "Unlocks",
    "Hats",
    "can_harvest",
    "clear",
    "do_a_flip",
    "get_companion",
    "get_cost",
    "get_entity_type",
    "get_ground_type",
    "get_pos_x",
    "get_pos_y",
    "get_time",
    "get_water",
    "get_world_size",
    "harvest",
    "measure",
    "move",
    "num_drones",
    "num_items",
    "num_unlocked",
    "plant",
    "quick_print",
    "spawn_drone",
    "wait_for",
    "has_finished",
    "till",
    "max_drones",
    "timed_reset",
    "trade",
    "unlock",
    "use_item",
]
