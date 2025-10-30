# Megafazenda

Este desbloqueio incrivelmente poderoso lhe dá acesso a vários drones.

Como antes, você ainda começa com apenas um drone. Drones adicionais devem primeiro ser gerados e desaparecerão após o término do programa. Cada drone executa seu próprio programa separado. Novos drones podem ser gerados usando a função `spawn_drone(function)`.

```python
def drone_function():
    move(North)
    do_a_flip()

spawn_drone(drone_function)
```

Isso gera um novo drone na mesma posição que o drone que executou o comando `spawn_drone(function)`. O novo drone então começa a executar a função especificada. Depois de terminar, ele desaparecerá automaticamente.

Drones não colidem entre si.

Use `max_drones()` para obter o número máximo de drones que podem existir simultaneamente. Use `num_drones()` para obter o número de drones que já estão na fazenda.

## Exemplo

```python
def harvest_column():
    for _ in range(get_world_size()):
        harvest()
        move(North)

while True:
    if spawn_drone(harvest_column):
        move(East)
```

Isso fará com que seu primeiro drone se mova horizontalmente e gere mais drones. Os drones gerados se moverão verticalmente e colherão tudo em seu caminho.

Se todos os drones disponíveis já tiverem sido gerados, `spawn_drone()` não fará nada e retornará `None`.

Aqui está outro exemplo que passa uma direção diferente para cada drone:

```python
for direction in [North, East, South, West]:
    def task():
        move(direction)
        do_a_flip()
    spawn_drone(task)
```

## Todos os Drones São Iguais

Não existe um drone "principal" especial. Todos os drones podem gerar outros drones, e todos contam para o limite de drones. Todos os drones desaparecem quando terminam. Se o primeiro drone terminar seu programa mais cedo, outro drone se tornará aquele cuja execução é visualizada com destaques de código. Todos os drones podem acionar breakpoints e, quando um drone aciona um breakpoint, o destaque de código muda para aquele drone.
