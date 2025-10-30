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
# Parâmetros extras, simples:
#   start_spin  -> 0..3 giros de 90° antes de começar (espalha heading)
#   turn_every  -> só vira após este número de MOVES bem-sucedidos (>=1)
# Mantém:
#   start_dir, prefer_cw, warmup

def treasure_hunt_worker(start_dir, prefer_cw, warmup, start_spin, turn_every):
	dir = start_dir

	# giros iniciais (espalha heading)
	s0 = 0
	while s0 < start_spin:
		if prefer_cw:
			dir = next_cw(dir)
		else:
			dir = next_ccw(dir)
		s0 = s0 + 1

	# aquecimento simples: anda alguns passos na direção atual
	s = 0
	while s < warmup:
		move(dir)
		s = s + 1

	x = get_pos_x()
	y = get_pos_y()

	moves_since_turn = 0  # controla quando aplicar a virada complementar

	while True:
		move(dir)

		x2 = get_pos_x()
		y2 = get_pos_y()

		if x == x2 and y == y2:
			# BLOQUEADO -> vira para a parede preferida
			if prefer_cw:
				dir = next_cw(dir)
			else:
				dir = next_ccw(dir)

			# Empurrão pós-bloqueio: tenta um passo imediato após girar
			move(dir)
			xb = get_pos_x()
			yb = get_pos_y()
			if xb != x or yb != y:
				# saiu do lugar; atualiza e zera o contador de reta
				x = xb
				y = yb
				moves_since_turn = 1  # já contamos esse avanço
				# aplica a virada complementar apenas quando atingir turn_every
				if moves_since_turn >= turn_every:
					if prefer_cw:
						dir = next_ccw(dir)
					else:
						dir = next_cw(dir)
					moves_since_turn = 0
		else:
			# MOVEU -> atualiza e contabiliza o avanço reto
			x = x2
			y = y2
			moves_since_turn = moves_since_turn + 1

			if moves_since_turn >= turn_every:
				# aplica a virada complementar padrão
				if prefer_cw:
					dir = next_ccw(dir)
				else:
					dir = next_cw(dir)
				moves_since_turn = 0

		if get_entity_type() == Entities.Treasure:
			harvest()
			return True

# ------------------- Envoltório para spawn_drone (sem lambda) -------------------

def make_runner(start_dir, prefer_cw, warmup, start_spin, turn_every):
	# Retorna a função que o drone deve executar com os parâmetros fixados
	def run():
		return treasure_hunt_worker(start_dir, prefer_cw, warmup, start_spin, turn_every)
	return run

# ------------------- Coordenador paralelo: primeiro que terminar ganha -------------------

NUM_DRONES = 8  # ajuste conforme quiser

def treasure_hunt_parallel():
	drones = []

	i = 0
	while i < NUM_DRONES:
		# Direções iniciais: W,N,E,S e rotaciona no segundo bloco de 4
		if i % 4 == 0:
			base_dir = West
		elif i % 4 == 1:
			base_dir = North
		elif i % 4 == 2:
			base_dir = East
		else:
			base_dir = South

		if i >= 4:
			start_dir = next_cw(base_dir)
		else:
			start_dir = base_dir

		# alterna preferência de giro para variar o "wall follower"
		if i % 2 == 0:
			prefer_cw = False   # esquerda (bloq CCW, move CW)
		else:
			prefer_cw = True    # direita (bloq CW, move CCW)

		# warmup pequeno e diferente por drone
		warmup = i % 4  # 0..3

		# novos parâmetros simples:
		start_spin = (i // 2) % 4   # 0..3 (muda heading inicial com giros)
		# turn_every: 1 mantém base; 2 ou 3 dá mais reta antes de virar
		if i % 3 == 0:
			turn_every = 1
		elif i % 3 == 1:
			turn_every = 2
		else:
			turn_every = 3

		func = make_runner(start_dir, prefer_cw, warmup, start_spin, turn_every)
		d = spawn_drone(func)
		if d != None:
			drones.append(d)
		i = i + 1

	found = False
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
