import math
import numbers
import random

from vec import Vec2

class Turtle():
    def __init__(self, backend):
        self.position = Vec2();
        self.direction = Vec2(0.0, -1.0);
        self.__scale = 1.0;
        self.drawing = True
        self.backend = backend
        self.stack = []

    def forward(self, by=1.0):
        new_position = self.position + self.direction * by * self.__scale
        if self.drawing:
            self.backend.add_line(self.position, new_position)
        self.position = new_position

    def turn_right(self, angle):
        self.direction = self.direction.rotate(-angle)

    def turn_left(self, angle):
        self.direction = self.direction.rotate(angle)

    def scale(self, factor):
        self.__scale *= factor

    def __get_state(self):
        return (self.position.clone(), self.direction.clone(), self.__scale, self.drawing)

    def __load_state(self, state):
        self.position = state[0]
        self.direction = state[1]
        self.__scale = state[2]
        self.drawing = state[3]

    def store(self):
        self.stack.append(self.__get_state())

    def restore(self):
        self.__load_state(self.stack.pop())

    def nothing(self):
        pass

    def pen_up(self):
        self.drawing = False

    def pen_down(self):
        self.drawing = True

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
                
