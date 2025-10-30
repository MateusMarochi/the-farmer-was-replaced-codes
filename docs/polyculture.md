# Policultura

Você já deve ter notado que, às vezes, as plantas rendem mais quando plantadas juntas. Grama, arbustos, árvores e cenouras rendem mais quando têm a companhia de planta certa. A preferência de companhia é diferente para cada planta individual e não pode ser prevista. Felizmente, a preferência de companhia da planta sob o drone pode ser medida usando `get_companion()`. Ela retorna uma tupla onde o primeiro elemento é o tipo de planta que ela quer como sua companheira e o segundo elemento é a posição onde ela quer sua companheira.

```python
plant_type, (x, y) = get_companion()
```

Por exemplo, se você plantar um arbusto e depois chamar `get_companion()`, ele retornará algo como `(Entities.Carrot, (3, 5))`. Isso significa que este arbusto gostaria de ter cenouras na posição `(3, 5)`. Então, se você plantar cenouras em `(3, 5)` e depois colher o arbusto, ele renderá mais madeira. O estágio de crescimento da cenoura não importa.

A preferência de companhia de uma planta pode ser `Entities.Grass`, `Entities.Bush`, `Entities.Tree` ou `Entities.Carrot`. Cada planta escolhe isso aleatoriamente, mas sempre escolherá uma planta diferente de si mesma. A posição também pode ser qualquer posição a até três movimentos da planta, exceto a posição da própria planta.

Se não houver nenhuma planta sob o drone que tenha preferência por companhia, `get_companion()` retornará `None`.

Antes de a policultura ser desbloqueada, o multiplicador de produção é 5. Ele dobra a cada vez que você o melhora.
