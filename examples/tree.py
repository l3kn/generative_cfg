from generative_cfg import *

backend = SVGBackend()
turtle = Turtle(backend)

grammar = Grammar()

arc_right_segment = [
    lambda turtle: turtle.forward(0.1),
    lambda turtle: turtle.turn_right(5)
]
arc_left_segment = [
    lambda turtle: turtle.forward(0.1),
    lambda turtle: turtle.turn_left(5)
]

grammar.add_non_terminal('Arc Left', arc_left_segment * 7)
grammar.add_non_terminal('Arc Left', arc_left_segment * 10)
grammar.add_non_terminal('Arc Left', arc_left_segment * 13)
grammar.add_non_terminal('Arc Right', arc_right_segment * 7)
grammar.add_non_terminal('Arc Right', arc_right_segment * 10)
grammar.add_non_terminal('Arc Right', arc_right_segment * 13)

scale = 0.6
grammar.add_non_terminal('Tree', [
    lambda turtle: turtle.store(),
    'Arc Left',
    lambda turtle: turtle.scale(scale),
    'Tree',
    lambda turtle: turtle.restore(),
    'Arc Right',
    lambda turtle: turtle.scale(scale),
    'Tree',
])

grammar.expand('Tree', turtle, 10)
backend.write('tree.svg')
