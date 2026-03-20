import math
from typing import Iterator, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Box:
    point: tuple[float, float] #bottom left corner
    size: tuple[float, float]

    def right_x(self):
        return self.point[0] + self.size[0]

    def top_y(self):
        return self.point[1] + self.size[1]

    def get_center(self):
        x = self.point[0] + self.size[0] / 2
        y = self.point[1] + self.size[1] / 2
        return x, y


@dataclass
class Circle:
    center: tuple[float, float] #center point
    radius: float

def distance_check(shape1, shape2):
    if type(shape1) is tuple[float, float]:
        if type(shape2) is tuple[float, float]:
            return math.dist(shape1, shape2)
        elif isinstance(shape2, Circle):
            return math.dist(shape1, shape2.center) - shape2.radius
    if isinstance(shape1, Circle):
        if type(shape2) is tuple[float, float]:
            return math.dist(shape1.center, shape2) - shape1.radius
        elif isinstance(shape2, Circle):
            return math.dist(shape1.center, shape2.center) - shape1.radius - shape2.radius


def get_circles_distance(circle_1_center, circle_1_radius, circle_2_center, circle_2_radius):
    distance = math.dist(circle_1_center, circle_2_center) - (circle_1_radius + circle_2_radius)
    return distance



def manhattan_distance_x_y(p1: Tuple[float, float], p2: Tuple[float, float]):
    return p2[0] - p1[0], p2[1] - p1[1]


def manhattan_distance_to_angle(x, y):
    angle_radians = math.atan2(y, x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def calculate_point_to_circle_distance(point, point2, radius):
    return math.dist(point, point2) - radius


def calculate_direction(distance_x, distance_y):
    parts = abs(distance_x) + abs(distance_y)
    part_size = 1 / parts
    movement_x, movement_y = part_size * distance_x, part_size * distance_y
    return movement_x, movement_y