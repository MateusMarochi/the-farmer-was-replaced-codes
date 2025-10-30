import plantacoes

# =================== Policultura simplificada e compatível com o ambiente ===================

pedidos = []  # lista de tuplas (x, y, tipo)

def plant_bush_fallback():
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)

def plant_entity(ptype):
	if ptype == Entities.Grass:
		plantacoes.plant_grass()
	elif ptype == Entities.Tree:
		plantacoes.plant_tree()
	elif ptype == Entities.Carrot:
		plantacoes.plant_carrot()
	elif ptype == Entities.Bush:
		plant_bush_fallback()
	elif ptype == Entities.Sunflower:              # <-- suporte explícito a sunflower
		plantacoes.plant_sunflower()
	else:
		plant(ptype)

def probe_cycle(step):
	mod = step % 4
	if mod == 0:
		return Entities.Grass
	elif mod == 1:
		return Entities.Tree
	elif mod == 2:
		return Entities.Carrot
	else:
		return Entities.Bush

def atender_pedidos_no_local():
	x = get_pos_x()
	y = get_pos_y()
	encontrou = False

	copia = []
	for item in pedidos:
		copia.append(item)

	for triple in copia:
		(px, py, ptype) = triple
		if px == x and py == y:
			plant_entity(ptype)
			if can_harvest():
				harvest()
			pedidos.remove(triple)
			encontrou = True

	return encontrou

def sondar_e_registrar_pedido(step):
	especie = probe_cycle(step)
	plant_entity(especie)
	comp = get_companion()

	if comp != None:
		ptype, pos = comp
		tx = pos[0]
		ty = pos[1]

		# evita duplicar pedidos
		existe = False
		for triple in pedidos:
			(px, py, _) = triple
			if px == tx and py == ty:
				existe = True

		if not existe:
			pedidos.append((tx, ty, ptype))

# ------------------- Movimentação utilitária -------------------

def move_to(x_target, y_target):
	x = get_pos_x()
	y = get_pos_y()

	while x < x_target:
		move(East)
		x = get_pos_x()
	while x > x_target:
		move(West)
		x = get_pos_x()

	while y < y_target:
		move(North)
		y = get_pos_y()
	while y > y_target:
		move(South)
		y = get_pos_y()

# ------------------- Trabalho em célula (colhe/atende/sonda) -------------------

def processar_celula(step_ref):
	# sempre colhe antes se possível
	if can_harvest():
		harvest()

	# =================== RESERVA DAS DUAS ÚLTIMAS COLUNAS PARA SUNFLOWERS ===================
	size = get_world_size()
	x = get_pos_x()
	if x >= size - 2:  # colunas (size-2) e (size-1)
		plant_entity(Entities.Sunflower)
		# nessas colunas não participamos do sistema de pedidos/sondagens
		return
	# ========================================================================================

	# fora das duas últimas colunas, segue a lógica normal de policultura coordenada
	handled = atender_pedidos_no_local()
	if not handled:
		sondar_e_registrar_pedido(step_ref[0])
		step_ref[0] = step_ref[0] + 1

# ------------------- Worker: cobre um PAR de colunas (x, x+1) -------------------

def worker_duas_colunas(col_inicio):
	size = get_world_size()
	move_to(col_inicio, 0)
	step_ref = [0]

	while True:
		# Sobe na coluna col_inicio
		j = 0
		while j < size:
			processar_celula(step_ref)
			if j < size - 1:
				move(North)
			j = j + 1

		# Vai para a coluna à direita (col_inicio + 1)
		move(East)

		# Desce nessa coluna
		j = 0
		while j < size:
			processar_celula(step_ref)
			if j < size - 1:
				move(South)
			j = j + 1

		# Volta para a coluna inicial
		move(West)

# ------------------- Envoltório para spawn_drone (sem lambda) -------------------

def make_runner_duas_colunas(col_inicio):
	def run():
		return worker_duas_colunas(col_inicio)
	return run

# ------------------- Orquestração: 11 drones intercalados e loop para todos -------------------

def iniciar_11_drones_em_22x22():
	size = get_world_size()
	# segurança: esperamos 22x22
	if size != 22:
		pass

	drones = []
	i = 0
	while i < 11:
		col = i * 2  # 0, 2, 4, ..., 20 (20 e 21 serão só sunflowers via processar_celula)
		func = make_runner_duas_colunas(col)
		d = spawn_drone(func)
		if d != None:
			drones.append(d)
		i = i + 1

	while True:
		move_to(0, 0)
		move_to(0, 0)

# ------------------- main -------------------

def main():
	iniciar_11_drones_em_22x22()

main()
