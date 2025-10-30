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

	# percorre cópia da lista para poder remover enquanto itera
	copia = []
	for item in pedidos:
		copia.append(item)

	for (px, py, ptype) in copia:
		if px == x and py == y:
			plant_entity(ptype)
			if can_harvest():
				harvest()
			pedidos.remove((px, py, ptype))  # remove apenas o atendido
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
		for (px, py, _) in pedidos:
			if px == tx and py == ty:
				existe = True

		if not existe:
			pedidos.append((tx, ty, ptype))

def policultura_scan():
	size = get_world_size()
	step = 0

	i = 0
	while i < size:
		j = 0
		while j < size:
			if can_harvest():
				harvest()

			# se esta posição foi pedida, atenda
			handled = atender_pedidos_no_local()

			# se não houve pedido, faz uma sonda para gerar possíveis companheiros
			if not handled:
				sondar_e_registrar_pedido(step)
				step = step + 1

			move(North)
			j = j + 1

		move(East)
		i = i + 1

def main():
	while True:
		# duas passagens ajudam a resolver todos os pedidos
		policultura_scan()
		policultura_scan()

main()
