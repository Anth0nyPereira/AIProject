"""Generic representation of the Game Map."""
import logging
from functools import reduce
from operator import add

from consts import Tiles, TILES

logger = logging.getLogger("Map")
logger.setLevel(logging.DEBUG)


class Map:
    """Representation of a Map."""

    def __init__(self, filename):
        self._map = []
        self._level = filename
        self._keeper = None

        with open(filename, "r") as f:
            for line in f:
                codedline = []
                for c in line.rstrip():
                    assert c in TILES, f"Invalid character '{c}' in map file"
                    tile = TILES[c]
                    codedline.append(tile)

                self._map.append(codedline) #_map é uma lista de listas, cada lista é uma linha do mapa que foi acrescentada ao ler o ficheiro

        self.hor_tiles, self.ver_tiles = (
            max([len(line) for line in self._map]),
            len(self._map),
        )  # X, Y

        # Add extra tiles to make the map a rectangule
        for y, line in enumerate(self._map):
            while len(line) < self.hor_tiles:
                self._map[y].append(Tiles.FLOOR) #mete chão em sitios "vazios" mas de qlqer maneira n vais poder chegar lá provavelmente por causa da parede

    def __str__(self): # vai ficar igual ao ficheiro do mapa
        map_str = ""
        screen = {tile: symbol for symbol, tile in TILES.items()}
        for line in self._map:
            for tile in line:
                map_str += screen[tile]
            map_str += "\n"

        return map_str.strip()

    def __getstate__(self): # retorna o mapa (cada vez que mudas alguma posição o mapa muda)
        return self._map

    def __setstate__(self, state): # definir o "mapa novo" de acordo com a jogada/moviemtnação feita
        self._map = state
        self._keeper = None
        self.hor_tiles, self.ver_tiles = (
            max([len(line) for line in self._map]),
            len(self._map),
        )  # X, Y

    @property
    def size(self):
        """Size of map."""
        return self.hor_tiles, self.ver_tiles

    @property
    def completed(self):
        """Map is completed when there are no empty_goals!"""
        return self.empty_goals == []

    @property
    def on_goal(self):
        """Number of boxes on goal.

           Counts per line and counts all lines using reduce
        """
        return reduce(
            add,
            [
                reduce(lambda a, b: a + int(b is Tiles.BOX_ON_GOAL), l, 0) # a e b são posições numa dada linha do mapa
                for l in self._map # l representa uma linha horizontal do mapa
            ],
        )

    def filter_tiles(self, list_to_filter):
        """Util to retrieve list of coordinates of given tiles.""" # retorna lista onde está o tipo de tile que queres
        return [
            (x, y)
            for y, l in enumerate(self._map)
            for x, tile in enumerate(l)
            if tile in list_to_filter
        ]

    @property
    def keeper(self):   # posição do man no momento (pode estar em cima de um diamante ou de um chão)
        """Coordinates of the Keeper."""
        if self._keeper is None:
            self._keeper = self.filter_tiles([Tiles.MAN, Tiles.MAN_ON_GOAL])[0]

        return self._keeper

    @property
    def boxes(self): # posições das caixas
        """List of coordinates of the boxes."""
        return self.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])

    @property
    def empty_goals(self): # posições dos diamantes (quer esteja o man em cima ou não, mas não devolve caixas que já estejam a verde/no local certo)
        """List of coordinates of the empty goals locations."""
        return self.filter_tiles([Tiles.GOAL, Tiles.MAN_ON_GOAL])

    def checkCorner(self):
        for pos in self.boxes():                    #Para a posição de cada caixa  #self.boxes() retorna um array de posições no formato (x,y)
            xCord = pos.pop()                       #Coordenada de uma caixa em x
            yCord = pos.pop()                       #Coordenada de uma caixa em y
            sidesBlocked = 0                        #Numero de lado bloquados
            dirsTested= 0                           #Direções que foram testadas
            if((self.get_tile((xCord, yCord+1)) == Tiles.WALL) or (self.get_tile((xCord, yCord+1)) == Tiles.BOX) or (self.get_tile((xCord, yCord+1)) == Tiles.BOX_ON_GOAL)):
                #A linha acima verifica de a pos abaixo da caixa é parede / caixa ou caixa em diamante por agora vamos considerar todos estes elementos bloqueantes apesar de que no futuro provavelmente terá que ser repensado para resolver problemas mais complexos
                #Caso seja true incrementar sidesBlocked
                sidesBlocked = sidesBlocked +1
            if ((self.get_tile((xCord, yCord - 1)) == Tiles.WALL) or (
                    self.get_tile((xCord, yCord - 1)) == Tiles.BOX) or (
                    self.get_tile((xCord, yCord - 1)) == Tiles.BOX_ON_GOAL)):
                sidesBlocked = sidesBlocked + 1
            if ((self.get_tile((xCord + 1, yCord)) == Tiles.WALL) or (
                self.get_tile((xCord + 1, yCord)) == Tiles.BOX) or (
                self.get_tile((xCord + 1, yCord)) == Tiles.BOX_ON_GOAL)):
                sidesBlocked = sidesBlocked + 1

            if ((self.get_tile((xCord - 1, yCord)) == Tiles.WALL) or (
                self.get_tile((xCord - 1, yCord)) == Tiles.BOX) or (
                self.get_tile((xCord - 1, yCord)) == Tiles.BOX_ON_GOAL)):
                sidesBlocked = sidesBlocked + 1

            if((dirsTested>=2) and (self.get_tile(pos) != Tiles.BOX_ON_GOAL)):
                return false  #Se existirem caixas bloqueadas sem estarem on goal retorna falso

        return true #Se nenhuma caixa estiver corner blocked return true




    def get_tile(self, pos): # retorna o número que corresponde à tile dada uma posição
        """Retrieve tile at position pos."""
        x, y = pos
        return self._map[y][x] # y é o nr da linha (uma das listas) e o x é o elemento da lista

    def set_tile(self, pos, tile):
        """Set the tile at position pos to tile."""
        x, y = pos
        self._map[y][x] = (
            tile & 0b1110 | self._map[y][x]
        )  # the 0b1110 mask avoid carring ON_GOAL to new tiles

        if (
            tile & Tiles.MAN == Tiles.MAN
        ):  # hack to avoid continuous searching for keeper
            self._keeper = pos

    def clear_tile(self, pos):  # perguntar ao stor
        """Remove mobile entity from pos."""
        x, y = pos
        self._map[y][x] = self._map[y][x] & 0b1  # lesser bit carries ON_GOAL

    def is_blocked(self, pos): # verifica se a posição pode ser ocupada (se está dentro do limite do mapa e se não é uma parede)
        """Determine if mobile entity can be placed at pos."""
        x, y = pos
        if x not in range(self.hor_tiles) or y not in range(self.ver_tiles):
            logger.error("Position out of map")
            return True
        if self._map[y][x] in [Tiles.WALL]:
            logger.debug("Position is a wall")
            return True
        return False


if __name__ == "__main__":
    mapa = Map("levels/2.xsb")
    print(mapa)
    assert mapa.keeper == (11, 8)
    assert mapa.get_tile((4, 2)) == Tiles.WALL
    assert mapa.get_tile((5, 2)) == Tiles.BOX
    assert mapa.get_tile((2, 7)) == Tiles.BOX
    assert mapa.get_tile(mapa.keeper) == Tiles.MAN
    # Fake move:
    mapa.clear_tile(mapa.keeper)
    mapa.set_tile((16, 7), Tiles.MAN)
    mapa.clear_tile((12, 7))
    mapa.set_tile((17, 7), Tiles.BOX)
    assert mapa.keeper == (16, 7)
    assert mapa.get_tile((17, 7)) == Tiles.BOX_ON_GOAL
    assert mapa.on_goal == 1
    assert mapa.boxes == [(5, 2), (7, 3), (5, 4), (7, 4), (2, 7), (17, 7)]
