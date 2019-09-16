from generative_cfg import *

backend = SVGBackend()
turtle = Turtle(backend)

# My coordinate system is reversed,
# turn the turtle around so it faces "up"
turtle.turn_right(180.0)

grammar = Grammar()

grammar.add_non_terminal('S', [
    lambda turtle: turtle.forward(1),
    lambda turtle: turtle.turn_right(5),
    lambda turtle: turtle.scale(0.99),
    'S'
])

grammar.expand('S', turtle, 300)
backend.write('spiral.svg')
