# Cacto

Como outras plantas, [cactos](objects/cactus) podem ser cultivados em solo e colhidos normalmente.

No entanto, eles aparecem em vários tamanhos e têm um curioso senso de ordem.

## Colheita em cadeia

Se você colher um cacto totalmente crescido e todos os cactos vizinhos estiverem em ordem, ele também colherá todos os cactos vizinhos recursivamente.

Você receberá cactos em quantidade igual ao número de cactos colhidos ao quadrado. Portanto, se você colher `n` cactos simultaneamente, receberá `n**2` `Items.Cactus`.

## Critério de ordem

Um cacto é considerado **em ordem** quando atende às seguintes condições:

- Os vizinhos ao norte e a leste estão totalmente crescidos e têm tamanho **maior ou igual**.
- Os vizinhos ao sul e a oeste estão totalmente crescidos e têm tamanho **menor ou igual**.

A colheita só se espalhará se todos os cactos adjacentes estiverem totalmente crescidos e em ordem. Isso significa que, se um bloco de cactos crescidos estiver ordenado por tamanho e você colher um deles, todo o bloco será colhido.

Um cacto totalmente crescido aparecerá marrom se estiver fora de ordem. Assim que for ordenado, ele ficará verde novamente.

## Medir e trocar

- Meça o tamanho de um cacto com `measure()`.
- Os tamanhos possíveis são `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8` e `9`.
- Passe uma direção para `measure(direction)` para medir o vizinho naquela direção.
- Troque um cacto com o vizinho em qualquer direção usando `swap(direction)`, que troca o objeto sob o drone com o objeto a uma casa de distância.

## Exemplos de grades ordenadas

Todos os cactos em cada grade abaixo estão em ordem, então a colheita se espalhará por toda a área.

```
3 4 5    3 3 3    1 2 3    1 5 9
2 3 4    2 2 2    1 2 3    1 3 8
1 2 3    1 1 1    1 2 3    1 3 4
```

Na grade abaixo, apenas o cacto inferior esquerdo está em ordem, o que não é suficiente para que a colheita se espalhe.

```
1 5 3
4 9 7
3 3 2
```

Se as linhas já estiverem ordenadas, ordenar as colunas não desordenará as linhas.

Se você não está familiarizado com algoritmos de ordenação, pesquise quais podem ser adaptados para este problema. Lembre-se de que nem todos funcionam, pois é possível apenas trocar cactos vizinhos.
