import heapq as heap
from collections import defaultdict
import json
from functools import cmp_to_key
from enum import Enum
INPUT_FILE = '14/input.txt'
import math

# Distress Signal
# Packets decoded out of order, re-order packets (input)


class Point(object):

    @staticmethod
    def from_raw(item):
        values = item.split(',')
        return Point(values[0], values[1])

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f'[{self.x},{self.y}]'

    def down(self):
        return Point(self.x, self.y + 1)

    def down_left(self):
        return Point(self.x - 1, self.y + 1)

    def down_right(self):
        return Point(self.x + 1, self.y + 1)


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

    def __str__(self):
        return 'H' if self.value == 1 else 'V'


class Line(object):
    def __init__(self, start: Point, end: Point, is_sand=False):
        self.is_sand = is_sand
        flip = False  # Check increasing in correct direction
        if start.x == end.x and abs(start.y) != abs(end.y):
            self.orientation = Orientation.VERTICAL
            flip = end.y < start.y
        elif start.y == end.y and abs(start.x) != abs(end.x):
            self.orientation = Orientation.HORIZONTAL
            flip = end.x < start.x
        else:
            self.orientation = Orientation.HORIZONTAL

        self.start = start if not flip else end
        self.end = end if not flip else start

    def __str__(self):
        return f'{self.orientation}:{str(self.start)} -> {str(self.end)}'


class RockMap(object):
    def __init__(self):
        self.rocks: list[Line] = []
        self.max_y = None
        self.min_x = None
        self.max_x = None
        self.bounding_box = None

    def add_line(self, line: Line):
        self.rocks.append(line)

    def next_point(self, point):
        pos = point.down()
        if not self.intersects(pos):
            return pos

        pos = point.down_left()
        if not self.intersects(pos):
            return pos

        pos = point.down_right()
        if not self.intersects(pos):
            return pos

        return None # Nowhere to go

    def any_rock_below_me(self, point):
        for r in [a for a in self.rocks if not a.is_sand and a.end.y > point.y]:
            # potential to be in way
            if r.start.x <= point.x <= r.end.x:
                return True
        return False

    def add_sand(self, start: Point):
        self.rocks.append(Line(Point(start.x, start.y), Point(start.x, start.y), is_sand=True))

    def add_sand_journey(self, start: Point):
        current_point = Point(start.x, start.y)
        finished = False
        while not finished:
            next_point = self.next_point(current_point)
            if next_point is None:
                # Resting place
                self.add_sand(current_point)
                finished = True
            else:
                current_point = next_point

            if not self.any_rock_below_me(current_point):
                return None
        return current_point

    def calculate_dimensions(self):
        for l in self.rocks:
            xs = [l.start.x, l.end.x]
            ys = [l.start.y, l.end.y]
            min_x = min(xs)
            max_x = max(xs)
            max_y = max(ys)
            if self.min_x is None or min_x < self.min_x:
                self.min_x = min_x
            if self.max_x is None or max_x > self.max_x:
                self.max_x = max_x
            if self.max_y is None or max_y > self.max_y:
                self.max_y = max_y

        # Bounding box
        self.bounding_box = Point(self.min_x, 0), Point(self.max_x, self.max_y)
        return self.bounding_box

    def intersects_point(self, line, point):
        if line.orientation == Orientation.HORIZONTAL:
            return line.start.y == point.y and line.start.x <= point.x <= line.end.x
        elif line.orientation == Orientation.VERTICAL:
            return line.start.x == point.x and line.start.y <= point.y <= line.end.y
        else:
            raise ValueError('Shouldn\'t reach here')

    def intersects(self, point):
        result = False
        for r in self.rocks:
            result = self.intersects_point(r, point)
            if result:
                return True
        return result

    def details(self):
        for r in self.rocks:
            print(str(r))
        print(f'Bounding Box: {str(self.bounding_box[0])} -> {str(self.bounding_box[1])}')
        total_sand = len([s for s in self.rocks if s.is_sand is True])
        print(f'Total Sand: {total_sand}')


def fetch_input():
    results = RockMap()
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if full_line != '':
                items = full_line.split(' -> ')
                for i in range(0, len(items) - 1):
                    results.add_line(Line(Point.from_raw(items[i]), Point.from_raw(items[i + 1])))
        results.calculate_dimensions()
    return results


def part_one():
    rock_map = fetch_input()
    print(len(rock_map.rocks))
    rock_map.details()

    finished = False
    while not finished:
        journey = rock_map.add_sand_journey(Point(500,0))
        print(journey)
        finished = journey is None
    rock_map.details()


if __name__ == "__main__":
    part_one()

