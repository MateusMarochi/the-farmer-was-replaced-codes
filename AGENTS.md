# Instruções para o agente

- Todos os arquivos de documentação com extensão `.md` devem ser redigidos usando formatação Markdown válida.
- Ao escrever algoritmos em Python, **não** utilizar as seguintes construções:
  - Operadores ternários (`a if cond else b`).
  - Comparações com `is` ou `is not`.
  - Funções ou expressões `lambda`.
  - A instrução `del`.
- Sempre preferir `print` para relatar erros em vez de lançar `ValueError`.
- Formatar todos os arquivos `.py` utilizando o Black antes de concluir o trabalho.
- `from game_api import (...)` só deve ser usado temporariamente para compilar ou testar localmente; remova qualquer import desse tipo no arquivo final.
- Para comentar código em Python, utilize apenas linhas iniciadas por `#`; não empregue strings multilinha (por exemplo, `"""comentário"""`).
