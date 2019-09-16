import random

class Grammar():
    def __init__(self):
        self.terminals = {}
        self.non_terminals = {}

    # TODO: I've added this as a kind of syntax sugar,
    # to make programs more concise
    def nt(self, name, body, weight=1):
        self.add_non_terminal(name, body, weight)

    def add_non_terminal(self, name, body, weight=1):
        for i in range(0, weight):
            self.non_terminals.setdefault(name, []).append(body)

    def add_terminal(self, name, body):
        self.terminals[name] = body

    def run(self, state, depth):
        if self.start_symbol is None:
            raise RuntimeError('The grammars start symbol must be set')

        self.__expand(self.start_symbol, state, depth)

    def __lookup(self, symbol):
        if symbol in self.non_terminals:
            return random.choice(self.non_terminals[symbol])
        else:
            return self.terminals[symbol]

    def expand(self, symbol, state, depth):
        if depth > 0:
            element = self.__lookup(symbol)

            # element is either a list (non-terminal) or a lambda
            if isinstance(element, list):
                for e in element:
                    if isinstance(e, str):
                        self.expand(e, state, depth - 1)
                    else:
                        e(state)
            else:
                element(state)
                
