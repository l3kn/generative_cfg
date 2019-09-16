import math
import numbers
import random

from .vec import Vec2

class Turtle():
    def __init__(self, backend):
        self.position = Vec2();
        self.direction = Vec2(0.0, -1.0);

        self.__scale = 1.0;
        self.drawing = True
        self.backend = backend

        # Used to (re)store the turtles state
        self.stack = []

    def forward(self, by=1.0):
        new_position = self.position + self.direction * by * self.__scale

        if self.drawing:
            self.backend.add_line(self.position, new_position)

        self.position = new_position

    def draw_circle(self, radius=1.0):
        radius = radius * self.__scale;
        self.backend.add_circle(self.position, radius, False, 1.0)

    def draw_filled_circle(self, radius=1.0):
        radius = radius * self.__scale;
        self.backend.add_circle(self.position, radius, True, 1.0)

    def turn_right(self, angle):
        self.direction = self.direction.rotate(-angle)

    def turn_left(self, angle):
        self.direction = self.direction.rotate(angle)

    def scale(self, factor):
        self.__scale *= factor

    def __get_state(self):
        return (
            self.position.clone(),
            self.direction.clone(),
            self.__scale,
            self.drawing,
       )

    def __load_state(self, state):
        (
            self.position,
            self.direction,
            self.__scale,
            self.drawing,
       ) = state

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
