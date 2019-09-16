from generative_cfg import *

backend = SVGBackend()
turtle = Turtle(backend)

grammar = Grammar()

grammar.add_non_terminal('Branch Right', [
    lambda turtle: turtle.forward(1.0),
    lambda turtle: turtle.turn_right(60)
])
grammar.add_non_terminal('Branch Left', [
    lambda turtle: turtle.forward(1.0),
    lambda turtle: turtle.turn_left(60)
])

grammar.add_non_terminal('Root', [
    'Tree',
    lambda turtle: turtle.turn_left(120),
    'Tree',
    lambda turtle: turtle.turn_left(120),
    'Tree',
])

scale = 0.5
grammar.add_non_terminal('Tree', [
    lambda turtle: turtle.store(),
    'Branch Left',
    lambda turtle: turtle.scale(scale),
    'Tree',
    lambda turtle: turtle.restore(),
    lambda turtle: turtle.store(),
    'Branch Right',
    lambda turtle: turtle.scale(scale),
    'Tree',
    lambda turtle: turtle.restore(),
], 8)
grammar.add_non_terminal('Tree', [])

for i in range(0, 5):
    backend = SVGBackend()
    turtle = Turtle(backend)
    grammar.expand('Root', turtle, 10)
    backend.write('flower1_{:02}.svg'.format(i))
