import math
from collections import defaultdict

INPUT_FILE = '09/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            results.append(JourneyStep(full_line.split(' ')))
    return results


class JourneyStep(object):
    def __init__(self, items):
        self.direction = items[0]
        self.distance = int(items[1])

    def get_steps(self):
        x_delta = 0
        y_delta = 0
        if self.direction == 'L':
            x_delta = -1
        elif self.direction == 'R':
            x_delta = 1
        elif self.direction == 'U':
            y_delta = 1
        elif self.direction == 'D':
            y_delta = -1
        return [Point(x_delta,y_delta) for i in range(0, self.distance)]

    def __str__(self):
        return f'{self.direction}-{self.distance}'


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_touching(self, point):
        x_dist = abs(point.x - self.x)
        y_dist = abs(point.y - self.y)
        distance = math.sqrt((x_dist * x_dist) + (y_dist * y_dist))
        return distance, distance < 2

    def delta(self, head):
        delta_x = 0
        delta_y = 0
        if self.y == head.y and self.x != head.x:
            delta_x = 1 if head.x > self.x else -1
        if self.x == head.x and self.y != head.y:
            delta_y = 1 if head.y > self.y else -1
        if delta_x == 0 and delta_y == 0:
            # diagonal needed
            delta_x = 1 if head.x > self.x else -1
            delta_y = 1 if head.y > self.y else -1
        return Point(delta_x, delta_y)


    def __str__(self):
        return f'({self.x},{self.y})'


def move_around_map(steps):
    head_positions = []
    tail_positions = []

    current_head_pos = Point(0, 0)
    current_tail_pos = Point(0, 0)

    head_positions.append(current_head_pos)
    tail_positions.append(current_tail_pos)

    distance = 0
    is_touching = True
    for i in steps:
        for step in i.get_steps():
            print(f'head: {str(current_head_pos)}, tail: {str(current_tail_pos)}, distance: {distance}, is_touching: {is_touching} ')
            current_head_pos = Point(current_head_pos.x + step.x, current_head_pos.y + step.y)
            head_positions.append(current_head_pos)
            distance, is_touching = current_head_pos.is_touching(current_tail_pos)
            if not is_touching:
                tail_delta = current_tail_pos.delta(current_head_pos)
                current_tail_pos = Point(current_tail_pos.x + tail_delta.x, current_tail_pos.y + tail_delta.y)
                tail_positions.append(current_tail_pos)

    return head_positions, tail_positions


def move_around_map_x_nots(steps):
    current_snake_positions = [Point(0, 0) for x in range(0, 10)]
    tail_positions = [current_snake_positions[-1]]
    for i in steps:
        print(i)
        for step in i.get_steps():
            print(f'{step}: {[str(c) for c in current_snake_positions]}')
            for idx, snake_item in enumerate(current_snake_positions):
                is_tail = idx == len(current_snake_positions) - 1
                current_head_pos = current_snake_positions[0]
                if idx == 0:
                    # Head
                    current_head_pos = Point(current_head_pos.x + step.x, current_head_pos.y + step.y)
                    current_snake_positions[0] = current_head_pos
                else:
                    # Non head
                    last_position = current_snake_positions[idx - 1]
                    current_pos = current_snake_positions[idx]
                    distance, is_touching = last_position.is_touching(current_pos)
                    if not is_touching:
                        tail_delta = current_pos.delta(last_position)
                        current_pos = Point(current_pos.x + tail_delta.x, current_pos.y + tail_delta.y)
                        if is_tail:
                            tail_positions.append(current_pos)
                    current_snake_positions[idx] = current_pos
    return tail_positions


def part_one():
    steps = fetch_input()
    head_positions, tail_positions = move_around_map(steps)
    unique_tail_positions = set([str(x) for x in tail_positions])
    print(len(unique_tail_positions))


def part_two():
    steps = fetch_input()
    print(steps)
    tail_positions = move_around_map_x_nots(steps)
    unique_tail_positions = set([str(x) for x in tail_positions])
    print(len(unique_tail_positions))


if __name__ == "__main__":
    #part_one()
    part_two()


