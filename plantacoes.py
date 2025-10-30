def plant_grass():
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Grass)
		
def plant_tree():
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Tree)
	if get_water() < 0.75:
		use_item(Items.Water) 
	
def plant_carrot():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)
	
def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Pumpkin)
	
def plant_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Sunflower)
	if get_water() < 0.5:
		use_item(Items.Water) 

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Cactus)
		
def plant_apple():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Apple)
	if get_water() < 0.5:
		use_item(Items.Water) 
		