import copy
import random

from Tile import Tile


class Grid:
    def __init__(self, screen_width, screen_height) -> None:
        self.image_size = 100
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boundary_tile = Tile()
        self.boundary_tile.setState(10)
        self.any_tile = Tile()

        self.setStartEnd()

    def initGrid(self):
        self.grid = []
        for i in range(int(self.screen_height / self.image_size)):
            temp = []
            for j in range(int(self.screen_width / self.image_size)):
                temp.append(Tile())
            self.grid.append(temp)

    def solve(self):
        old_grid = copy.deepcopy(self.grid)

        # Go through each position in the grid and try to simplify the possible end states
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if not self.grid[y][x].isSolved():
                    # Get the edge connections for the current tile and collapse tile
                    self.grid[y][x].solve(self.getEdges(x, y))

        self.fillRandomTile()

    # Gets the edge connections for the current tile
    def getEdges(self, x, y):
        edges = []

        if y == 0:
            edges.append(self.boundary_tile)
        else:
            if not self.grid[y-1][x].isSolved():
                edges.append(self.any_tile)
            else:
                edges.append(self.grid[y-1][x])

        if x == int((self.screen_width / self.image_size) - 1):
            edges.append(self.boundary_tile)
        else:
            if not self.grid[y][x+1].isSolved():
                edges.append(self.any_tile)
            else:
                edges.append(self.grid[y][x+1])

        if y == int((self.screen_height / self.image_size) - 1):
            edges.append(self.boundary_tile)
        else:
            if not self.grid[y+1][x].isSolved():
                edges.append(self.any_tile)
            else:
                edges.append(self.grid[y+1][x])

        if x == 0:
            edges.append(self.boundary_tile)
        else:
            if not self.grid[y][x-1].isSolved():
                edges.append(self.any_tile)
            else:
                edges.append(self.grid[y][x-1])

        return edges

    def fillRandomTile(self):
        # Find out the lowest number of choices
        lowest_position_choices = []
        lowest_choices = 100
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if not tile.isSolved():
                    choices = tile.possible_states
                    if len(choices) < lowest_choices:
                        lowest_choices = len(choices)
                        lowest_position_choices = []
                        lowest_position_choices.append([x, y, choices])
                    elif len(choices) == lowest_choices:
                        lowest_position_choices.append([x, y, choices])

        if len(lowest_position_choices) != 0:
            # Choose a random one from the list
            tile_sel = random.randint(0, len(lowest_position_choices)-1)
            chosen_tile = lowest_position_choices[tile_sel]

            try:
                tile_type = chosen_tile[2][random.randint(0, len(chosen_tile[2])-1)]

                # Place tile at grid position
                self.grid[chosen_tile[1]][chosen_tile[0]].setState(tile_type)
            except:
                self.setStartEnd()

    def setStartEnd(self):
        self.initGrid()
        self.grid, start_x, start_y = self.setEntrance(self.grid)

        end_x = start_x
        end_y = start_y

        while end_x == start_x and end_y == start_y:
            temp_grid = copy.deepcopy(self.grid)
            temp_grid, end_x, end_y = self.setEntrance(self.grid)

        self.grid = temp_grid

        for i in self.grid:
            for j in i:
                j.removeEntrances()

    def setEntrance(self, grid):
        # Start by choosing a random edge and setting it to 0, 1, 2, or 3 depending on how it's facing
        horizontal_edge = random.randint(0, int(self.screen_height / self.image_size) - 1)
        vertical_edge = random.randint(0, int(self.screen_width / self.image_size) - 1)
        if random.randint(0, 1) == 0:
            if random.randint(0, 1) == 0:
                horizontal_edge = 0
            else:
                horizontal_edge = int((self.screen_height - self.image_size) / self.image_size)
        else:
            if random.randint(0, 1) == 0:
                vertical_edge = 0
            else:
                vertical_edge = int((self.screen_width - self.image_size) / self.image_size)

        if horizontal_edge == 0:
            tile_type = 2
        elif horizontal_edge == int((self.screen_height - self.image_size) / self.image_size):
            tile_type = 0
        elif vertical_edge == 0:
            tile_type = 3
        else:
            tile_type = 1

        grid[horizontal_edge][vertical_edge].setState(tile_type)

        return grid, horizontal_edge, vertical_edge

    def isSolved(self):
        for i in self.grid:
            for j in i:
                if not j.isSolved():
                    return False
        return True
