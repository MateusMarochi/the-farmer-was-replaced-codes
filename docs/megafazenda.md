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

## Aguardando Outro Drone

Use a função `wait_for(drone)` para aguardar que outro drone termine. Você recebe o identificador `drone` quando o gera. `wait_for(drone)` retorna o valor de retorno da função que o outro drone estava executando.

```python
def get_entity_type_in_direction(direction):
    move(direction)
    return get_entity_type()

def zero_arg_wrapper():
    return get_entity_type_in_direction(North)

drone = spawn_drone(zero_arg_wrapper)
print(wait_for(drone))
```

Lembre-se de que gerar drones leva tempo, então não é uma boa ideia criar um novo drone para cada tarefa pequena.

Você pode usar `has_finished(drone)` para verificar se o drone terminou sem precisar esperar.

## Sem Memória Compartilhada

Cada drone possui sua própria memória e não pode ler ou escrever diretamente as variáveis globais de outro drone.

```python
x = 0

def increment():
    global x
    x += 1

wait_for(spawn_drone(increment))
print(x)
```

Esse código imprimirá `0`, porque o novo drone incrementou sua própria cópia da variável global `x`, o que não afeta o valor de `x` do primeiro drone.

## Condições de Corrida

Vários drones podem interagir com a mesma casa da fazenda ao mesmo tempo. Se dois drones interagirem com a mesma casa durante o mesmo tick, ambas as interações ocorrerão, mas os resultados podem variar de acordo com a ordem das interações.

Imagine que os drones 0 e 1 estejam sobre a mesma árvore quase totalmente crescida. Se o drone 0 chamar `use_item(Items.Fertilizer)` enquanto o drone 1 chama `harvest()`, a ordem de execução importa. Se as ações ocorrerem exatamente no mesmo tick, a árvore será fertilizada primeiro e colhida depois, garantindo que você receba madeira. Contudo, se o drone 1 for um pouco mais rápido, a árvore será colhida antes de ser fertilizada, e você não receberá a madeira. Esse cenário é chamado de **condição de corrida**, um problema comum em programação paralela em que o resultado depende da ordem das operações.

Também é possível que vários drones executem o mesmo trecho de código simultaneamente na mesma posição:

```python
if get_water() < 0.5:
    use_item(Items.Water)
```

Se vários drones executarem esse código ao mesmo tempo, todos avaliarão a condição como verdadeira antes que qualquer um aplique água, resultando em desperdício. No instante em que o primeiro drone chega à segunda linha, `get_water()` pode não ser mais menor que `0.5`, porque outro drone já regou a plantação.
