import math
import numbers

class Vec2():
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0.0
            self.y = 0.0
        elif len(args) == 1:
            self.x = args[0]
            self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise RuntimeError("Invalid number of arguments")

    def clone(self):
        return Vec2(self.x, self.y)

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def rotate(self, angle):
        "Rotate vector by an angle in degrees"
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)

        x = c * self.x - s * self.y
        y = s * self.x + c * self.y

        return Vec2(x, y)

    def dot(self, other):
        "Dot product"
        return self.x * other.x + self.y * other.j

    def __mul__(self, other):
        if type(other) == type(self):
            return self.dot(other)
        elif isinstance(other, numbers.Real):
            return Vec2(self.x * other, self.y * other)
        else:
            raise TypeError("Multiplication not implemented for Vec2 and %r" % other)

    def __imul__(self, other):
        "In-place multiplication, used by `*=`"
        if isinstance(other, numbers.Real):
            self.x *= other
            self.y *= other
            return self
        else:
            raise TypeError("Multiplication not implemented for Vec2 and %r" % other)

    def __rmul__(self, other):
        "Used e.g. for `4.0 * Vec2(1.0, 2.0)`"
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, numbers.Real):
            return Vec2(self.x / other, self.y / other)
        else:
            raise TypeError("Division not implemented for Vec2 and %r" % other)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        "In-place addition, used by `+=`"
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        "In-place subtraction, used by `-=`"
        self.x -= other.x
        self.y -= other.y
        return self

    def __repr__(self):
        return '({:.3f}, {:.3f})'.format(self.x, self.y)
