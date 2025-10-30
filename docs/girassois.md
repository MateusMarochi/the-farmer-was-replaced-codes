# Girassóis

[Girassóis](objects/sunflower) coletam a energia do sol, e você pode colher essa energia.

## Plantio
- Plantar girassóis funciona exatamente como plantar cenouras ou abóboras.
- Eles podem ser medidos mesmo antes de estarem totalmente crescidos.

## Colheita e pétalas
- Colher um girassol crescido rende energia.
- Se houver pelo menos 10 girassóis na fazenda e você colher aquele com o maior número de pétalas, você ganha 5 vezes mais energia.
- A função `measure()` retorna o número de pétalas do girassol sob o drone.
- Girassóis têm entre 7 e 15 pétalas, inclusive.
- Vários girassóis podem compartilhar o maior número de pétalas; nesse caso, qualquer um deles pode ser colhido para obter o bônus.

## Uso de energia pelo drone
- Enquanto houver energia disponível, o drone trabalha duas vezes mais rápido.
- O drone consome 1 ponto de energia a cada 30 ações (movimentos, colheitas, plantios etc.).
- Executar outras instruções de código também consome energia, porém muito menos do que as ações do drone.
- Tudo que é acelerado por melhorias de velocidade também é acelerado pela energia.
- Qualquer ação acelerada pela energia consome energia proporcional ao tempo necessário para executá-la, ignorando melhorias de velocidade.
