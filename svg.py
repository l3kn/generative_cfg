import math

from vec import Vec2

class SVGBackend():
    def __init__(self, width=800):
        """Takes one argument, the width of the output image in pixels
         the height is calculated based on the bounding box
         of the lines in the image"""
        self.width = width
        self.bottom_left = None
        self.top_right = None
        self.lines = []

    def __merge_point(self, point):
        "Include a point in the bounding box used to scale the svg image"
        if self.bottom_left is None:
            self.bottom_left = point.clone()
            self.top_right = point.clone()
        else:
            self.bottom_left.x = min(self.bottom_left.x, point.x)
            self.bottom_left.y = min(self.bottom_left.y, point.y)
            self.top_right.x = max(self.top_right.x, point.x)
            self.top_right.y = max(self.top_right.y, point.y)
            
    def add_line(self, start, end):
        self.__merge_point(start)
        self.__merge_point(end)
        self.lines.append((start, end))

    def write(self, path):
        # For empty images, default to a size of 1.0 x 1.0
        if not self.lines or self.bottom_left == self.top_right:
            self.bottom_left = Vec2(0.0, 0.0)
            self.top_right = Vec2(1.0, 1.0)

        bb_width = self.top_right.x - self.bottom_left.x
        bb_height = self.top_right.y - self.bottom_left.y
        bb_ratio = bb_height / bb_width

        padding = 20
        
        width = self.width - 2 * padding
        height = math.ceil(width * bb_ratio)
        scale = width / bb_width

        with open(path, 'w') as output:
            output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            output.write(f'<svg width="{self.width}" height="{height + 2 * padding}" xmlns="http://www.w3.org/2000/svg">\n')
            for (start, end) in self.lines:
                start = (start - self.bottom_left) * scale
                end = (end - self.bottom_left) * scale
                output.write('<line x1="{:.3f}" y1="{:.3f}" x2="{:.3f}" y2="{:.3f}" stroke="black" stroke-width="1" fill="none"/>\n'.format(
                                        start.x + padding,
                                        start.y + padding,
                                        end.x + padding,
                                        end.y + padding
                                    ))
            output.write('</svg>\n')
