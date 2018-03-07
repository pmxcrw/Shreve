class Tree(object):

    def __init__(self, root, next_state):
        self.data = [{root: next_state(root)}]
        self.next_state = next_state

    def __getitem__(self, item):
        return self.data[item]

    @property
    def terminal_states(self):
        return set().union(*(set(states) for states in self.data[-1].values()))

    def extend(self):
        new_layer = {state: self.next_state(state) for state in self.terminal_states}
        self.data.extend([new_layer])
