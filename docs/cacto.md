<line-height=50%><size=40px>Cacto</size>
</line-height>
Como outras plantas, <u><link="objects/cactus">cactos</link></u> podem ser cultivados em solo e colhidos como de costume.

No entanto, eles vêm em vários tamanhos e têm um estranho senso de ordem.

Se você colher um cacto totalmente crescido e todos os cactos vizinhos estiverem em ordem, ele também colherá todos os cactos vizinhos recursivamente.

Um cacto é considerado em ordem se todos os cactos vizinhos ao North e East estiverem totalmente crescidos e forem maiores ou iguais em tamanho, e todos os cactos vizinhos ao South e West estiverem totalmente crescidos e forem menores ou iguais em tamanho.

A colheita só se espalhará se todos os cactos adjacentes estiverem totalmente crescidos e em ordem.
Isso significa que, se um quadrado de cactos crescidos estiver ordenado por tamanho e você colher um cacto, ele colherá o quadrado inteiro.

Um cacto totalmente crescido aparecerá marrom se não estiver ordenado. Uma vez ordenado, ele ficará verde novamente.

Você receberá cactos em quantidade igual ao número de cactos colhidos ao quadrado. Então, se você colher n cactos simultaneamente, receberá n**2 Items.Cactus.

O tamanho de um cacto pode ser medido com measure().
É sempre um destes números: 0,1,2,3,4,5,6,7,8,9.

Você também pode passar uma direção para measure(direction) para medir a casa vizinha naquela direção do drone.

Você pode trocar um cacto com seu vizinho em qualquer direção usando o comando swap().
swap(direction) troca o objeto sob o drone com o objeto a uma casa de distância na direction do drone.

<line-height=50%><size=32px>Exemplos</size>
</line-height>
Em cada uma dessas grades, todos os cactos estão em ordem e a colheita se espalhará por todo o campo:
3 4 5    3 3 3    1 2 3    1 5 9
2 3 4    2 2 2    1 2 3    1 3 8
1 2 3    1 1 1    1 2 3    1 3 4

Nesta grade, apenas o cacto inferior esquerdo está em ordem, o que não é suficiente para que a colheita se espalhe:
1 5 3
4 9 7
3 3 2


Se as linhas já estiverem ordenadas, ordenar as colunas não desordenará as linhas.


Se você não está familiarizado com algoritmos de ordenação, pode querer pesquisá-los online e pensar sobre quais poderiam ser adaptados para este problema. Lembre-se que nem todos funcionam porque você só pode trocar cactos vizinhos.
