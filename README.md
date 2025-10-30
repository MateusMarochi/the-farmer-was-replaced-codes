# The Farmer Was Replaced – Códigos

Este repositório reúne scripts em Python que espelham estratégias para o jogo
*The Farmer Was Replaced*. O arquivo [`global.py`](global.py) define os mesmos
nomes de funções, enums e constantes expostos pela API oficial do jogo, mas com
implementações fictícias que apenas preservam as assinaturas documentadas. Isso
permite executar os algoritmos de forma isolada, sem acesso ao cliente do jogo,
para fins de leitura, estudo ou prototipagem rápida.

## Estrutura

- `global.py`: Stubs da API do jogo, incluindo funções utilitárias como
  `move`, `plant`, `trade` e coleções como `Entities`, `Grounds`, `Items`,
  `Unlocks` e `Hats`.
- `bone_farm.py` e `maze_farm.py`: Exemplos de scripts que utilizam as
  assinaturas acima para automatizar tarefas dentro do jogo.

## Como usar

1. Certifique-se de estar com Python 3.12 ou superior instalado.
2. Execute qualquer script diretamente, por exemplo:

   ```bash
   python bone_farm.py
   ```

   As funções definidas em `global.py` não executam ações reais; elas apenas
   emitem um aviso informando que se tratam de stubs. Dessa forma você pode
   depurar a lógica do algoritmo sem interagir com o jogo.

## Referência

A documentação das assinaturas originais encontra-se na wiki oficial do jogo.
As docstrings em `global.py` reproduzem as descrições essenciais para consulta
rápida durante o desenvolvimento dos scripts.
