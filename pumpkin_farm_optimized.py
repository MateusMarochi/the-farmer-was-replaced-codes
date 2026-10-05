def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Pumpkin)

def fill_field():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant_pumpkin()
			move(North)
		move(East)

def fix_pass():
	not_ready = 0
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if get_entity_type() != Entities.Pumpkin:
				# dead or empty-> replant
				plant_pumpkin()
				not_ready += 1
			elif not can_harvest():
				not_ready += 1
			move(North)
		move(East)
	return not_ready

def farm_pumpkin():
	fill_field()
	while fix_pass() > 0:
		pass
	harvest()

def farm_carrot():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
			move(North)
		move(East)

while True:
	# make sure that we have enough + more carrot for planting
	while num_items(Items.Carrot) < get_world_size() * get_world_size() * 2:
		farm_carrot()
	farm_pumpkin()
