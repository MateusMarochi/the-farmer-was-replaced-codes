# 🌾🤖 The Farmer Was Replaced – Códigos / Codes

## 🇧🇷 Português

### ✨ Visão geral
Bem-vindo ao repositório que reúne protótipos de automação para o jogo *The Farmer Was Replaced*. Aqui você encontra scripts em Python que recriam estratégias populares de cultivo, caça a tesouros e ordenação de plantações utilizando as assinaturas expostas pela API oficial do jogo. O módulo [`global.py`](global.py) fornece stubs para essas funções, possibilitando executar e depurar os algoritmos sem a necessidade do cliente oficial. 🌱

### 🧰 Pré-requisitos
- Python 3.12 ou superior instalado localmente.
- Ambiente virtual (recomendado) configurado com os requisitos do projeto.

### ▶️ Como executar
1. Escolha um script, por exemplo `bone_farm.py`.
2. Execute com:
   ```bash
   python bone_farm.py
   ```
3. As chamadas da API presentes em `global.py` apenas registram ações simuladas, permitindo compreender o fluxo de decisão de cada algoritmo.

### 🌟 Algoritmos principais
- **`bone_farm.py` – Varredura com Chapéu de Dinossauro 🦖**: percorre o tabuleiro em zigue-zague alternando colunas, usa troca temporária de chapéus para contornar bloqueios e garante o retorno seguro ao ponto inicial. 【F:bone_farm.py†L1-L36】
- **`maze_farm.py` / `maze_farm_2.py` – Caça ao tesouro cooperativa 🧭**: gera labirintos usando substância estranha e lança múltiplos drones com diferentes direções, preferências de giro e aquecimento para explorar paredes opostas em paralelo. O primeiro drone que encontrar o tesouro encerra a rodada. 【F:maze_farm.py†L1-L94】【F:maze_farm_2.py†L1-L96】
- **`maze_farm_3.py` – Caça adaptativa avançada 🚁**: adiciona rotações iniciais e contadores de reta para variar o padrão de wall-following, junto de empurrões pós-bloqueio que ajudam a escapar de becos com mais eficiência. 【F:maze_farm_3.py†L1-L124】
- **`cactus_farm.py` – Ordenação de cactos em malha 🌵**: calcula passes verticais e horizontais que comparam medições entre vizinhos usando `measure` e `swap`, aplicando varreduras repetidas para organizar os cactos por altura enquanto múltiplos drones compartilham o campo. 【F:cactus_farm.py†L1-L195】
- **`polyculture_farm.py` – Policultura cooperativa 🌾🌳🥕**: gerencia uma lista de pedidos de companheiros, alternando sondagens e atendimentos para manter ciclos de grama, árvores, cenouras e arbustos em todo o mapa. 【F:polyculture_farm.py†L1-L93】
- **`polyculture_farm_paralel.py` – Policultura paralela com girassóis 🌞**: distribui drones em pares de colunas, reserva as duas últimas colunas para girassóis e sincroniza as sondagens através de uma referência compartilhada de passos. 【F:polyculture_farm_paralel.py†L1-L141】
- **`pumpkin_farm.py` – Monitoramento de abóboras por coluna 🎃**: mantém estados individuais por tile, mede crescimento, detecta abóboras mortas e só colhe quando o tamanho alvo permanece estável por leituras consecutivas. 【F:pumpkin_farm.py†L1-L126】
- **`pumpkin_farm_2.py` – Implantação modular de megafazenda 🎯**: configura mundos 22x22 ou 32x32, prepara o solo e lança drones especializados (patches, minipatches e girassóis) para construir layouts completos ou compactos. 【F:pumpkin_farm_2.py†L1-L132】
- **`plantacoes.py` – Biblioteca de plantio 🌼**: funções auxiliares que garantem o tipo de solo correto e aplicação de água para diferentes culturas, reutilizadas pelos demais scripts. 【F:plantacoes.py†L1-L34】

### 📚 Documentação complementar
A pasta [`docs/`](docs) contém artigos focados em cada estratégia (`aboboras.md`, `cacto.md`, `megafazenda.md`, `polyculture.md`), oferecendo contexto adicional, parâmetros sugeridos e análise de desempenho. 📖

---

## 🇺🇸 English

### ✨ Overview
Welcome to the repository that gathers automation prototypes for *The Farmer Was Replaced*. You will find Python scripts that recreate well-known farming, treasure-hunting, and sorting strategies powered by the public game API. The [`global.py`](global.py) module ships stub implementations so you can run and debug each algorithm without the official client. 🌱

### 🧰 Prerequisites
- Python 3.12 or newer available locally.
- Optional virtual environment with the project requirements.

### ▶️ How to run
1. Pick any script, e.g. `bone_farm.py`.
2. Launch it with:
   ```bash
   python bone_farm.py
   ```
3. The API calls in `global.py` only log simulated actions, letting you inspect every decision step safely.

### 🌟 Highlighted algorithms
- **`bone_farm.py` – Dinosaur Hat sweep 🦖**: snakes through the grid column by column, temporarily swapping hats whenever movement is blocked and always returning to the origin. 【F:bone_farm.py†L1-L36】
- **`maze_farm.py` / `maze_farm_2.py` – Cooperative treasure hunt 🧭**: crafts mazes with Weird Substance and launches multiple drones with distinct starting headings, turn preferences, and warm-ups so that each wall follower covers a different portion until one finds the treasure. 【F:maze_farm.py†L1-L94】【F:maze_farm_2.py†L1-L96】
- **`maze_farm_3.py` – Adaptive treasure hunting 🚁**: enriches the worker with initial spins, straight-run counters, and post-block nudges to break out of dead ends faster while maintaining complementary turn rules. 【F:maze_farm_3.py†L1-L124】
- **`cactus_farm.py` – Grid cactus sorting 🌵**: performs repeated vertical and horizontal sweeps comparing neighbor measurements via `measure` and `swap`, organizing cactus heights while coordinating several drones. 【F:cactus_farm.py†L1-L195】
- **`polyculture_farm.py` – Cooperative polyculture 🌾🌳🥕**: manages companion requests in a shared queue, alternating between probing and fulfilling orders to sustain grass, trees, carrots, and bushes across the map. 【F:polyculture_farm.py†L1-L93】
- **`polyculture_farm_paralel.py` – Parallel polyculture with sunflowers 🌞**: assigns drones to pairs of columns, reserves the two rightmost ones for sunflowers, and synchronizes probe steps through a mutable counter. 【F:polyculture_farm_paralel.py†L1-L141】
- **`pumpkin_farm.py` – Column-based pumpkin monitor 🎃**: tracks growth per tile, detects dead pumpkins, and only harvests once the target size stays stable across consecutive measurements. 【F:pumpkin_farm.py†L1-L126】
- **`pumpkin_farm_2.py` – Modular mega-farm deployment 🎯**: prepares 22x22 or 32x32 worlds and spawns specialized drones (patch, mini-patch, sunflower) to build full or compact layouts automatically. 【F:pumpkin_farm_2.py†L1-L132】
- **`plantacoes.py` – Planting helpers 🌼**: utility routines that ensure proper ground types and hydration for each crop, shared across the repository. 【F:plantacoes.py†L1-L34】

### 📚 Extra reading
Explore the [`docs/`](docs) folder for deep dives on each strategy (`aboboras.md`, `cacto.md`, `megafazenda.md`, `polyculture.md`) with background, tuning advice, and performance notes. 📖

---

## 🤝 Contribuição / Contributing
Pull requests e sugestões são bem-vindas! Abra uma issue descrevendo a ideia ou envie diretamente sua melhoria — lembre-se de manter os exemplos focados no aprendizado e compatíveis com os stubs existentes. 💡
