class Tile:
    def __init__(self) -> None:
        self.possible_states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # 0 is wide brown path
        # 1 is small brown path
        # 2 is grassy area
        # -1 is any type
        self.links = {
            0 : [1, 2, 2, 2],
            1 : [2, 2, 2, 1],
            2 : [2, 2, 1, 2],
            3 : [2, 1, 2, 2],
            4 : [1, 2, 1, 2],
            5 : [2, 1, 2, 1],
            6 : [2, 2, 1, 1],
            7 : [2, 1, 1, 2],
            8 : [1, 1, 2, 2],
            9 : [1, 2, 2, 1],
            10 : [2, 2, 2, 2],
        }

        self.state = None

    def collapse(self, edges):
        # Go through the possible states and prune impossible states
        new_states = []

        # Go through each state
        for state in self.possible_states:
            add = True
            state_edges = self.links[state]

            for i in range(len(edges)):
                if edges[i].isSolved():
                    tile_edges = self.links[edges[i].state]

                    if tile_edges[(i+2)%4] != state_edges[i]:
                        add = False

            if add:
                new_states.append(state)

        self.possible_states = new_states

    def isSolved(self):
        if self.state != None:
            return True

    def solve(self, edge_connections):
        # If the possible states is only 1, then choose that
        if len(self.possible_states) == 1:
            self.setState(self.possible_states[0])
        else:
            self.collapse(edge_connections)

    def setState(self, state):
        self.state = state
        self.possible_states = []

    def removeEntrances(self):
        if 0 in self.possible_states:
            self.possible_states.remove(0)
        if 1 in self.possible_states:
            self.possible_states.remove(1)
        if 2 in self.possible_states:
            self.possible_states.remove(2)
        if 3 in self.possible_states:
            self.possible_states.remove(3)