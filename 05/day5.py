from collections import defaultdict

INPUT_FILE = '05/input.txt'


def fetch_input():
    stacks = []
    operations = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if full_line.startswith('move'):
                operations.append(full_line)
            else:
                stacks.append(full_line)
    return stacks, operations


class LifoQueue(object):

    def __init__(self, stack_key, init_array):
        self.stack_key = stack_key
        self.queue = []
        for item in init_array:
            self.add(item)

    def add(self, value):
        self.queue.insert(0, value)

    def remove(self):
        return self.queue.pop(0)


class ParseStacksInput(object):

    def __init__(self, raw_stacks):
        self.raw_stacks = raw_stacks
        self.x_axis = self.find_x_axis()
        self.stack_list = self.find_stack_list()
        self.stack_data = [i for i in raw_stacks if not (i.startswith(' 1') or i == '')]

    def find_x_axis(self):
        return [i for i in self.raw_stacks if i.startswith(' 1')][0]

    def find_stack_list(self):
        return [int(v) for v in self.x_axis.split(' ') if v is not '']

    def find_stack_char_index(self, stack_no):
        return self.x_axis.find(str(stack_no))

    def to_lifo_queues(self):
        lifo_queues = []
        for stack_id in self.stack_list:
            stack_key = int(stack_id)
            idx = self.find_stack_char_index(stack_id)
            print(f'{stack_key}-{idx}')
            stack_res = []
            for row in self.stack_data:
                if len(row) >= idx and row[idx] is not '' and row[idx] is not ' ':
                    stack_res.append(row[idx])
            stack_res.reverse()
            this_queue = LifoQueue(stack_key, stack_res)
            lifo_queues.append(this_queue)
        return lifo_queues


class ParseOperationsInput(object):

    def __init__(self, raw_operations):
        self.raw_operations = raw_operations
        self.operations = [self.to_operation(v) for v in raw_operations]

    def to_operation(self, operation: str):
        # move 1 from 2 to 6
        from_idx = operation.find('from')
        to_idx = operation.find('to')
        total = int(operation[4: from_idx])
        from_val = int(operation[from_idx + 4: to_idx])
        to_val = int(operation[to_idx + 2:])
        return total, from_val, to_val


def part_one():
    # Part 1
    print('Day 5 - Part 1')
    rs, ro = fetch_input()

    # Parse stacks
    stack_parser = ParseStacksInput(rs)
    lqs = stack_parser.to_lifo_queues()
    print(len(lqs))
    stacks = {}
    for val in lqs:
        print(f'{val.stack_key} - {val.queue}')
        stacks[val.stack_key] = val
    print(stacks.keys())

    # Parse operations
    operation_parser = ParseOperationsInput(ro)

    # Execute
    for op in operation_parser.operations:
        source = stacks[op[1]]
        dest = stacks[op[2]]
        for moves in range(0, op[0]):
            take = source.remove()
            dest.add(take)

    # Print Final Stacks
    print(''.join([s.queue[0] for s in lqs]))


def part_two():
    # Part 2
    print('Day 5 - Part 2')
    rs, ro = fetch_input()

    # Parse stacks
    stack_parser = ParseStacksInput(rs)
    lqs = stack_parser.to_lifo_queues()
    print(len(lqs))
    stacks = {}
    for val in lqs:
        print(f'{val.stack_key} - {val.queue}')
        stacks[val.stack_key] = val
    print(stacks.keys())

    # Parse operations
    operation_parser = ParseOperationsInput(ro)

    # Execute
    for op in operation_parser.operations:
        temp_queue = LifoQueue('temp', [])
        source = stacks[op[1]]
        dest = stacks[op[2]]

        # Move to temp
        for moves in range(0, op[0]):
            take = source.remove()
            temp_queue.add(take)

        # Move to dest
        for moves in range(0, op[0]):
            take = temp_queue.remove()
            dest.add(take)

    # Print Final Stacks
    print(''.join([s.queue[0] for s in lqs]))


if __name__ == "__main__":
    part_one()
    part_two()
