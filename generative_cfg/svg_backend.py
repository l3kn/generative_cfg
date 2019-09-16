import math

from .vec import Vec2

class SVGBackend():
    def __init__(self, width=800):
        """Takes one argument, the width of the output image in pixels
         the height is calculated based on the bounding box
         of the lines in the image"""
        self.width = width
        self.bottom_left = None
        self.top_right = None
        self.lines = []
        self.thick_lines = []
        self.polygons = []
        self.circles = []

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

    def add_circle(self, center, radius, filled=False, thickness=1.0):
        real_radius = radius + thickness/2;
        self.__merge_point(center + Vec2(real_radius, real_radius))
        self.__merge_point(center - Vec2(real_radius, real_radius))
        self.circles.append((center, radius, filled, thickness))

    def add_line(self, start, end):
        self.__merge_point(start)
        self.__merge_point(end)
        self.lines.append((start, end))

    def add_thick_line(self, start, end, thickness=1.0):
        self.__merge_point(start)
        self.__merge_point(end)
        self.thick_lines.append((start, end, thickness))

    def add_polygon(self, points):
        for point in points:
            self.__merge_point(point)
        self.polygons.append(points)

    def write(self, path):
        # For empty images, default to a size of 1.0 x 1.0
        if not (self.lines or self.thick_lines or self.polygons or self.circles) or self.bottom_left == self.top_right:
            self.bottom_left = Vec2(0.0, 0.0)
            self.top_right = Vec2(1.0, 1.0)

        bb_width = self.top_right.x - self.bottom_left.x
        bb_height = self.top_right.y - self.bottom_left.y
        bb_ratio = bb_height / bb_width

        padding = 20

        width = self.width - 2 * padding
        height = math.ceil(width * bb_ratio)
        scale = width / bb_width

        padding = Vec2(padding, padding)

        with open(path, 'w') as output:
            output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            output.write(f'<svg width="{self.width}" height="{height + 2 * padding.y}" xmlns="http://www.w3.org/2000/svg">\n')
            for (start, end, thickness) in self.thick_lines:
                start = (start - self.bottom_left) * scale + padding
                end = (end - self.bottom_left) * scale + padding
                output.write('<line x1="{:.3f}" y1="{:.3f}" x2="{:.3f}" y2="{:.3f}" stroke="black" stroke-width="{}" stroke-linecap="round" fill="none"/>\n'.format(
                                        start.x,
                                        start.y,
                                        end.x,
                                        end.y,
                                        thickness * scale if thickness else 1.0,
                                    ))

            for (start, end) in self.lines:
                start = (start - self.bottom_left) * scale + padding
                end = (end - self.bottom_left) * scale + padding
                output.write('<line x1="{:.3f}" y1="{:.3f}" x2="{:.3f}" y2="{:.3f}" stroke="black" stroke-width="{}" stroke-linecap="round" fill="none"/>\n'.format(
                                        start.x,
                                        start.y,
                                        end.x,
                                        end.y,
                                        1.0
                                    ))

            for (center, radius, filled, thickness) in self.circles:
                center = (center - self.bottom_left) * scale + padding
                radius = radius * scale
                output.write(f'<circle cx="{center.x}" cy="{center.y}" r="{radius}" stroke="black" stroke-width="{thickness * scale}" fill="{"black" if filled else "none"}"/>\n')

            for points in self.polygons:
                points = map(lambda point: (point - self.bottom_left) * scale + padding, points)
                points_str = " ".join(map(lambda point: "{:.3f},{:.3f}".format(point.x, point.y), points))
                output.write('<polygon points="{}" stroke="black" stroke-width="1" fill="black"/>\n'.format(points_str))

            output.write('</svg>\n')
