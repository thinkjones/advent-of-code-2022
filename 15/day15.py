import heapq as heap
from collections import defaultdict
import json
from functools import cmp_to_key
from enum import Enum
INPUT_FILE = '15/input.txt'
import math
import re
# Distress Signal
# Packets decoded out of order, re-order packets (input)


def to_key(x, y):
    return f'{x}:{y}'

def sqaure_diff(v1, v2):
    dist = v2 - v1
    return 0 if dist == 0 else pow(dist, 2)

def to_distance(p1, p2):
    x2 = abs(p2.x - p1.x)
    y2 = abs(p2.y - p1.y)
    return x2 + y2

def to_distance_diagonal(p1, p2):
    x2 = sqaure_diff(p1.x, p2.x)
    y2 = sqaure_diff(p1.y, p2.y)
    return math.sqrt(x2 + y2)


class PointType(Enum):
    BEACON = 1
    SENSOR = 2
    NULL = 3

    def __str__(self):
        return self.name[0]

class Point(object):

    @staticmethod
    def from_raw(item):
        values = item.split(',')
        return Point(values[0], values[1])

    def __init__(self, x, y, point_type: PointType=None):
        self.x = int(x)
        self.y = int(y)
        self.point_type = point_type or PointType.NULL

    def to_key(self):
        return to_key(self.x, self.y)

    def __str__(self):
        return f'[{self.point_type.name}:{"{:,}".format(self.x)},{"{:,}".format(self.y)}]'


class BeaconSensor(object):
    def __init__(self, sx, sy, bx, by):
        self.sensor = Point(sx, sy, PointType.SENSOR)
        self.beacon = Point(bx, by, PointType.BEACON)
        # √[(x₂ - x₁)² + (y₂ - y₁)²].
        self.distance = to_distance(self.sensor, self.beacon)

    def determine_no_beacons(self):
        no_beacons = []
        max_distance = math.ceil(self.distance)
        s = self.sensor
        for x in range(s.x - max_distance - 1, s.x + max_distance + 1):
            for y in range(s.y - max_distance - 1, s.y + max_distance + 1):
                curr_distance = to_distance(self.sensor, Point(x, y))
                if curr_distance <= self.distance:
                    no_beacons.append(Point(x, y, PointType.NULL))
        return no_beacons

    def __str__(self):
        return f'[{str(self.sensor)} to {str(self.beacon)} is {str("{:,}".format(self.distance))}]'


class BeaconMap(object):
    def __init__(self):
        self.points = defaultdict(str)
        self.min_y = None
        self.max_y = None
        self.min_x = None
        self.max_x = None
        self.bounding_box = None

    def add_beacon_sensor(self, sx, sy, bx, by):
        bs = BeaconSensor(sx, sy, bx, by)
        self.points[bs.sensor.to_key()] = bs

    def setup(self):
        xs = []
        ys = []
        for bs in self.points.values():
            dist = math.ceil(bs.distance)
            xs.append(bs.beacon.x - dist if bs.beacon.x < 1 else bs.beacon.x + dist)
            xs.append(bs.sensor.x - dist if bs.sensor.x < 1 else bs.sensor.x + dist)
            ys.append(bs.beacon.y - dist if bs.beacon.y < 1 else bs.beacon.y + dist)
            ys.append(bs.sensor.y - dist if bs.sensor.y < 1 else bs.sensor.y + dist)
        self.min_x = min(xs)
        self.max_x = max(xs)
        self.min_y = min(ys)
        self.max_y = max(ys)
        # Bounding box
        self.bounding_box = Point(self.min_x, self.min_y), Point(self.max_x, self.max_y)
        return self.bounding_box

    def details(self):
        print(f'Bounding Box: {str(self.bounding_box[0])} -> {str(self.bounding_box[1])}')

    def calculate_map_slow(self):
        results = []
        sensors = [s.sensor.to_key() for s in self.points.values()]
        beacons = [s.beacon.to_key() for s in self.points.values()]
        no_beacons = set()
        idx = 0

        for bs in self.points.values():
            for i in bs.determine_no_beacons():
                no_beacons.add(i.to_key())

        for y in range(self.min_y - 1, self.max_y + 1):
            line = []
            for x in range(self.min_x - 1, self.max_x + 1):
                k = to_key(x, y)
                if k in sensors:
                    line.append('S')
                elif k in beacons:
                    line.append('B')
                elif k in no_beacons:
                    line.append('#')
                else:
                    line.append('.')
            results.append((y, line))
        return results

    def calc_closest_sensor(self, x, y):
        print(f'Analyzing: {x}, {y}')
        distance = math.inf
        closest_sensor = None
        for bs in self.points.values():
            sensor_distance = to_distance(bs.sensor, Point(x, y))
            if distance == math.inf or sensor_distance <= bs.distance:
                distance = sensor_distance
                closest_sensor = bs
        return closest_sensor, distance

    def calculate_map_for_row(self, locate_y=0):
        print('Step 1 Sensors and Beacons')
        results = []
        sensors = [s.sensor.to_key() for s in self.points.values()]
        beacons = [s.beacon.to_key() for s in self.points.values()]
        no_beacons = set()

        # Move along y row
        print('Step 3 Move along y row')
        total_range = self.max_x - self.min_x
        print(f'total_range: {total_range}')
        y_row = ['' for i in range(0, total_range + 2)]
        idx = -1
        for x in range(self.min_x - 1, self.max_x + 1):
            print(idx)
            idx += 1
            k = to_key(x, locate_y)
            print(k)
            closest_sensor, distance_to_sensor = self.calc_closest_sensor(x, locate_y)
            if k in sensors:
                y_row[idx] = 'S'
            elif k in beacons:
                y_row[idx] = 'B'
            elif distance_to_sensor <= closest_sensor.distance:
                y_row[idx] = '#'
            else:
                y_row[idx] = '.'

        return y_row


    def calculate_map_for_row_math(self, locate_y=0):
        print('Step 1 Sensors and Beacons')
        results = []
        sensors = [s.sensor.to_key() for s in self.points.values()]
        beacons = [s.beacon.to_key() for s in self.points.values()]
        no_beacons = set()

        print('Step 2 Find sensors which intersect row')
        lines = []
        for bs in self.points.values():
            vertical_distance_to_sensor = to_distance(Point(bs.sensor.x, locate_y), bs.sensor)
            diff = bs.distance - vertical_distance_to_sensor
            if diff >= 0:
                # line intersects sensor
                lines.append(BeaconSensor(bs.sensor.x - diff, locate_y, bs.sensor.x + diff, locate_y))

        # Sort lines by starting x value
        lines.sort(key=lambda x: x.sensor.x)

        # overlaps
        line_lengths = []
        for i in range(0, len(lines)):
            curr = lines[i]
            if i == 0:
                line_lengths.append(curr.distance)
            else:
                # Did last overlap
                last_line = lines[i-1]
                if curr.sensor.x < last_line.beacon.x:
                    delta = curr.beacon.x - last_line.beacon.x
                    print(f'Calc: ({curr.beacon.x} - {last_line.beacon.x}) = {delta}')
                    line_lengths.append(delta)
                else:
                    line_lengths.append(curr.distance)

        return line_lengths, lines



REGEX_PATTERN = re.compile(r"(Sensor at x=)(-\d*|\d*)(, y=)(-\d*|\d*): closest beacon is at x=(-\d*|\d*), y=(-\d*|\d*)")

def fetch_input():
    results = BeaconMap()
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if full_line != '':
                result = REGEX_PATTERN.findall(full_line)
                match = result[0]
                results.add_beacon_sensor(match[1], match[3], match[4], match[5])
        return results


def part_one_old():
    beacon_map = fetch_input()
    print(f'Total Beacon Sensor Pairs: {len(beacon_map.points)}')
    beacon_map.setup()
    print(f'BB: {str(beacon_map.bounding_box[0])} -> {str(beacon_map.bounding_box[1])}')
    map = beacon_map.calculate_map_old()
    for (row, m) in map:
        txt = ''.join(m)
        print(f'{row} \t {txt}')

    print('\n\n')
    row_10 = [m for (row, m) in map if row == 10]
    print(row_10)
    occupied = [i for i in row_10[0] if i == '#']
    print(len(occupied))

def part_one():
    beacon_map = fetch_input()
    print(f'Total Beacon Sensor Pairs: {len(beacon_map.points)}')
    beacon_map.setup()
    print(f'BB: {str(beacon_map.bounding_box[0])} -> {str(beacon_map.bounding_box[1])}')
    line_lengths, lines = beacon_map.calculate_map_for_row_math(10)
    lines_raw = [str(s) for s in lines]
    print(f'*** {10} ')
    print(f'{lines_raw} ')
    print(f'line_lengths: {["{:,}".format(s) for s in line_lengths]} ')
    total_dist = sum([bs.distance for bs in lines])
    print(f'total_dist: {sum(line_lengths)} ')


if __name__ == "__main__":
    part_one()

