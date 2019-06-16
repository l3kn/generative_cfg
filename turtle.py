import math
import numbers
import random

from vec import Vec2

class RustBackend():
    def __init__(self, series_name, image_name):
        self.lines = [
            'GH name {}'.format(series_name),
            'H name {}'.format(image_name)
        ]
        
    def add_line(self, start, end):
        line = 'L 1 {:.6f},{:.6f};{:6f},{:6f}'.format(start.x, start.y, end.x, end.y)
        self.lines.append(line)

    def add_circle(self, center, radius):
        line = 'C 1 0 {:.6f},{:.6f} {:6f}'.format(center.x, center.y, radius)
        self.lines.append(line)

    def write(self, path):
        with open(path, 'w') as output:
            for line in self.lines:
                output.write(line)
                output.write('\n')

class Turtle():
    def __init__(self, backend):
        self.position = Vec2();
        self.direction = Vec2(0.0, 1.0);
        self.scale = 1.0;
        self.drawing = True
        self.backend = backend
        self.stack = []

    def forward(self, by=1.0):
        new_position = self.position + self.direction * by * self.scale
        if self.drawing:
            self.backend.add_line(self.position, new_position)
        self.position = new_position

    def turn_right(self, angle):
        self.direction = self.direction.rotate(-angle)

    def turn_left(self, angle):
        self.direction = self.direction.rotate(angle)

    def scale_by(self, factor):
        self.scale *= factor

    def circle_left(self, radius=1.0):
        radius = radius * self.scale
        left = self.direction.rotate(90.0)
        center = self.position + left * radius
        backend.add_circle(center, radius)

    def circle_right(self, radius=1.0):
        radius = radius * self.scale
        right = self.direction.rotate(-90.0)
        center = self.position + right * radius
        backend.add_circle(center, radius)

    def __get_state(self):
        return (self.position.clone(), self.direction.clone(), self.scale, self.drawing)

    def __load_state(self, state):
        self.position = state[0]
        self.direction = state[1]
        self.scale = state[2]
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

    def forward_arc(self, step, angle, times):
        for _ in range(0, times):
            self.forward(step)
            self.turn_right(angle)
        

class Grammar():
    def __init__(self):
        self.terminals = {}
        self.non_terminals = {}
        self.start_symbol = None

    def add_non_terminal(self, name, body):
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

    def __expand(self, symbol, state, depth):
        if depth > 0:
            element = self.__lookup(symbol)

            # element is either a list (non-terminal) or a lambda
            if isinstance(element, list):
                for e in element:
                    if isinstance(e, str):
                        self.__expand(e, state, depth - 1)
                    else:
                        e(state)
            else:
                element(state)
                
