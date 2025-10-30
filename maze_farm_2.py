# ------------------- Geração do labirinto (SEM chamar hunt aqui) -------------------

def create_maze():
	clear()
	plant(Entities.Bush)
	substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	return True

# ------------------- Helpers de direção (sem lambda/ternário) -------------------

def next_cw(d):
	if d == North:
		return East
	elif d == East:
		return South
	elif d == South:
		return West
	elif d == West:
		return North
	return d

def next_ccw(d):
	if d == North:
		return West
	elif d == West:
		return South
	elif d == South:
		return East
	elif d == East:
		return North
	return d

# ------------------- Algoritmo BASE da caça (worker do drone) -------------------
# Agora aceita parâmetros de variabilidade:
#   start_dir  -> direção inicial distinta por drone
#   prefer_cw  -> se True: BLOQUEADO gira CW e AO MOVER gira CCW (inverte a regra)
#                 se False: mantém comportamento base (bloqueado CCW, ao mover CW)
#   warmup     -> passos de "aquecimento" na direção inicial (desincroniza spawns)

def treasure_hunt_worker(start_dir, prefer_cw, warmup):
	dir = start_dir

	# aquecimento simples: tenta andar alguns passos para espalhar os drones
	s = 0
	while s < warmup:
		move(dir)
		s = s + 1

	x = get_pos_x()
	y = get_pos_y()

	while True:
		move(dir)

		x2 = get_pos_x()
		y2 = get_pos_y()

		if x == x2 and y == y2:
			# BLOQUEADO
			if prefer_cw:
				dir = next_cw(dir)
			else:
				dir = next_ccw(dir)
		else:
			# MOVEU
			x = x2
			y = y2
			if prefer_cw:
				# se preferiu CW ao bloquear, ao mover vira CCW (regra invertida)
				dir = next_ccw(dir)
			else:
				# regra original: ao mover, vira CW
				dir = next_cw(dir)

		if get_entity_type() == Entities.Treasure:
			harvest()
			return True

# ------------------- Envoltório para spawn_drone (sem lambda) -------------------

def make_runner(start_dir, prefer_cw, warmup):
	# Retorna a função que o drone deve executar com os parâmetros fixados
	def run():
		return treasure_hunt_worker(start_dir, prefer_cw, warmup)
	return run

# ------------------- Coordenador paralelo: primeiro que terminar ganha -------------------

NUM_DRONES = 16 # ajuste conforme quiser

def treasure_hunt_parallel():
	drones = []

	# Padrões diferentes por índice: direção inicial, preferência de giro e warmup
	i = 0
	while i < NUM_DRONES:
		if i % 4 == 0:
			start_dir = West
		elif i % 4 == 1:
			start_dir = North
		elif i % 4 == 2:
			start_dir = East
		else:
			start_dir = South

		# alterna preferência de giro para variar o "wall follower"
		if i % 2 == 0:
			prefer_cw = False   # comportamento base (bloqueado CCW, moveu CW)
		else:
			prefer_cw = True    # invertido (bloqueado CW, moveu CCW)

		# pequeno deslocamento inicial para espalhar
		warmup = i  # 0,1,2,3,...

		func = make_runner(start_dir, prefer_cw, warmup)
		d = spawn_drone(func)
		if d != None:
			drones.append(d)
		i = i + 1

	found = False
	j = 0
	while not found:
		j = 0
		while j < len(drones):
			d = drones[j]
			if d != None and has_finished(d):
				res = wait_for(d)
				if res:
					found = True
					break
			j = j + 1

	return True

# ------------------- Loop principal -------------------

def main():
	while True:
		ok = create_maze()
		if ok:
			got = treasure_hunt_parallel()
			if got:
				continue

main()
