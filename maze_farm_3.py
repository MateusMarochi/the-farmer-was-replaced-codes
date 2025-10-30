# ------------------- Geração do labirinto (SEM chamar hunt aqui) -------------------


def create_maze():
    clear()
    plant(Entities.Bush)
    substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)
    return True


# ------------------- Posicionamento inicial -------------------


def move_axis(direction, steps):
    count = 0
    while count < steps:
        moved = move(direction)
        if not moved:
            return False
        count = count + 1
    return True


def move_to_center():
    size = get_world_size()
    half = size // 2

    moved_horizontal = move_axis(East, half)
    if not moved_horizontal:
        return False

    moved_vertical = move_axis(South, half)
    if not moved_vertical:
        return False

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
#   phase_delay -> após esta quantidade de movimentos, habilita nova fase
# Mantém:
#   start_dir, prefer_cw, warmup


def treasure_hunt_worker(
    start_dir,
    prefer_cw,
    warmup,
    start_spin,
    turn_every,
    phase_delay,
    phase_turn_every,
    phase_flip_preference,
    stuck_escape_threshold,
    extra_spins,
):
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
    total_moves = 0
    phase_applied = False
    current_prefer_cw = prefer_cw
    current_turn_every = turn_every
    blocked_streak = 0

    while True:
        move(dir)

        x2 = get_pos_x()
        y2 = get_pos_y()

        if x == x2 and y == y2:
            # BLOQUEADO -> vira para a parede preferida
            if current_prefer_cw:
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
                if moves_since_turn >= current_turn_every:
                    if current_prefer_cw:
                        dir = next_ccw(dir)
                    else:
                        dir = next_cw(dir)
                    moves_since_turn = 0
                blocked_streak = 0
                total_moves = total_moves + 1
            else:
                blocked_streak = blocked_streak + 1
        else:
            # MOVEU -> atualiza e contabiliza o avanço reto
            x = x2
            y = y2
            moves_since_turn = moves_since_turn + 1
            blocked_streak = 0
            total_moves = total_moves + 1

            if moves_since_turn >= current_turn_every:
                # aplica a virada complementar padrão
                if current_prefer_cw:
                    dir = next_ccw(dir)
                else:
                    dir = next_cw(dir)
                moves_since_turn = 0

        if not phase_applied and phase_delay > 0 and total_moves >= phase_delay:
            phase_applied = True
            if phase_flip_preference:
                current_prefer_cw = not current_prefer_cw
            if phase_turn_every > 0:
                current_turn_every = phase_turn_every

        if stuck_escape_threshold > 0 and blocked_streak >= stuck_escape_threshold:
            spin_count = 0
            while spin_count < extra_spins:
                if current_prefer_cw:
                    dir = next_ccw(dir)
                else:
                    dir = next_cw(dir)
                spin_count = spin_count + 1
            blocked_streak = 0
            moves_since_turn = 0

        if get_entity_type() == Entities.Treasure:
            harvest()
            return True


# ------------------- Envoltório para spawn_drone (sem lambda) -------------------


def make_runner(
    start_dir,
    prefer_cw,
    warmup,
    start_spin,
    turn_every,
    phase_delay,
    phase_turn_every,
    phase_flip_preference,
    stuck_escape_threshold,
    extra_spins,
):
    # Retorna a função que o drone deve executar com os parâmetros fixados
    def run():
        return treasure_hunt_worker(
            start_dir,
            prefer_cw,
            warmup,
            start_spin,
            turn_every,
            phase_delay,
            phase_turn_every,
            phase_flip_preference,
            stuck_escape_threshold,
            extra_spins,
        )

    return run


# ------------------- Coordenador paralelo: primeiro que terminar ganha -------------------


def treasure_hunt_parallel():
    move_to_center()

    drones = []

    world_size = get_world_size()
    max_slots = max_drones()
    if max_slots < 1:
        max_slots = 1

    i = 0
    while i < max_slots:
        # Direções iniciais: W,N,E,S e rotaciona no segundo bloco de 4
        index_mod = i % 4
        if index_mod == 0:
            base_dir = West
        elif index_mod == 1:
            base_dir = North
        elif index_mod == 2:
            base_dir = East
        else:
            base_dir = South

        if i >= 4:
            start_dir = next_cw(base_dir)
        else:
            start_dir = base_dir

        # alterna preferência de giro para variar o "wall follower"
        if i % 2 == 0:
            prefer_cw = False  # esquerda (bloq CCW, move CW)
        else:
            prefer_cw = True  # direita (bloq CW, move CCW)

        # warmup pequeno e diferente por drone
        warmup = i % 4  # 0..3

        # novos parâmetros simples:
        start_spin = (i // 2) % 4  # 0..3 (muda heading inicial com giros)
        # turn_every: 1 mantém base; 2 ou 3 dá mais reta antes de virar
        remainder = i % 3
        if remainder == 0:
            turn_every = 1
        elif remainder == 1:
            turn_every = 2
        else:
            turn_every = 3

        phase_delay = 0
        phase_turn_every = 0
        phase_flip_preference = False
        stuck_escape_threshold = 0
        extra_spins = 0

        if i >= 3:
            phase_delay = world_size * (i - 2)
            if phase_delay < world_size:
                phase_delay = world_size

            phase_turn_every = turn_every + 1
            if phase_turn_every > 4:
                phase_turn_every = 4

            if i % 2 == 1:
                phase_flip_preference = True

            stuck_escape_threshold = 2 + (i % 3)
            extra_spins = 1 + (i % 2)

        func = make_runner(
            start_dir,
            prefer_cw,
            warmup,
            start_spin,
            turn_every,
            phase_delay,
            phase_turn_every,
            phase_flip_preference,
            stuck_escape_threshold,
            extra_spins,
        )
        d = spawn_drone(func)
        if d != None:
            drones.append(d)
        else:
            break
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
