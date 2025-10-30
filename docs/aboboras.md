# Abóboras

[Abóboras](objects/pumpkin) crescem como cenouras em solo arado. Plantá-las custa cenouras.

Quando todas as abóboras em um quadrado estão totalmente crescidas, elas se juntam para formar uma abóbora gigante. Infelizmente, as abóboras têm 20% de chance de morrer quando estão totalmente crescidas, então você precisará replantar as mortas se quiser que elas se fundam.

Quando uma abóbora morre, ela deixa para trás uma abóbora morta que não renderá nada quando colhida. Plantar uma nova planta em seu lugar remove automaticamente a abóbora morta, então não há necessidade de colhê-la. `can_harvest()` sempre retorna `False` em abóboras mortas.

O rendimento de uma abóbora gigante depende do tamanho da abóbora.

- Uma abóbora 1x1 rende `1*1*1 = 1` abóbora.
- Uma abóbora 2x2 rende `2*2*2 = 8` abóboras em vez de 4.
- Uma abóbora 3x3 rende `3*3*3 = 27` abóboras em vez de 9.
- Uma abóbora 4x4 rende `4*4*4 = 64` abóboras em vez de 16.
- Uma abóbora 5x5 rende `5*5*5 = 125` abóboras em vez de 25.
- Uma abóbora `n x n` rende `n*n*6` abóboras para `n >= 6`.

É uma boa ideia obter abóboras de tamanho pelo menos 6x6 para obter o multiplicador total.

Isso significa que, mesmo que você plante uma abóbora em cada casa de um quadrado, uma das abóboras pode morrer e impedir que a mega abóbora cresça.
