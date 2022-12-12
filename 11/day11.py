import math
from collections import defaultdict
import decimal
from fractions import Fraction
INPUT_FILE = '11/input.txt'


def create_lambda(operator, arg0):
    if operator == '+':
        return lambda x: x + int(arg0)
    elif operator == '*' and arg0 == 'old':
        return lambda x: x * x
    elif operator == '*' and arg0 != 'old':
        return lambda x: x * int(arg0)


def fetch_input(worry_divider=3):
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        current_monkey = None
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            print(full_line)
            if 'Monkey' in full_line:
                monkey_id = full_line.split(' ')[1].split(':')[0]
                current_monkey = Monkey(monkey_id, [], None, None, None, None, worry_divider=worry_divider)
            elif 'Starting items:' in full_line:
                items_raw = full_line.split(': ')
                current_monkey.items = [int(s) for s in items_raw[1].split(',')]
            elif 'Test: divisible by ' in full_line:
                items_raw = full_line.split('Test: divisible by ')
                current_monkey.test_denominator = int(items_raw[1])
            elif 'Operation: new = old + ' in full_line:
                items_raw = full_line.split('Operation: new = old + ')
                current_monkey.operation_lambda = create_lambda('+', items_raw[1])
            elif 'Operation: new = old * ' in full_line:
                items_raw = full_line.split('Operation: new = old * ')
                current_monkey.operation_lambda = create_lambda('*', items_raw[1])
            elif 'If true: throw to monkey' in full_line:
                items_raw = full_line.split('If true: throw to monkey ')
                current_monkey.monkey_true = int(items_raw[1])
            elif 'If false: throw to monkey' in full_line:
                items_raw = full_line.split('If false: throw to monkey ')
                current_monkey.monkey_false = int(items_raw[1])
                results.append(current_monkey)
    return results


class Monkey(object):
    def __init__(self, monkey_id, items, operation_lambda, test_denominator, monkey_true, monkey_false, worry_divider=3,
                 worry_modulo=None):
        self.id = int(monkey_id)
        self.items = items
        self.worry_divider = worry_divider
        self.worry_modulo = worry_modulo
        self.operation_lambda = operation_lambda
        self.test_denominator = test_denominator
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false

    def inspect_and_pop(self):
        if len(self.items) == 0:
            return None, None

        item = self.items.pop()
        new_worry_level = self.operation_lambda(item)
        new_bored_level = new_worry_level
        if self.worry_divider > 1:
            new_bored_level = new_worry_level / self.worry_divider
            print(new_bored_level)
        if self.worry_modulo:
            new_bored_level = new_bored_level % self.worry_modulo

        test_result = (new_bored_level % self.test_denominator) == 0
        return new_bored_level, self.monkey_true if test_result else self.monkey_false

    def __str__(self):
        return f'Monkey: {str(self.id)}: \n\tStarting Items: {[str(s) for s in self.items]}\n\toperation_lambda: {self.operation_lambda(2)}\n\ttest_denominator: {self.test_denominator}\n\tTrue go to {str(self.monkey_true)}\n\tTrue go to {str(self.monkey_false)}'


def part_one():
    raw_results = fetch_input()
    monkey_dict = {m.id: m for m in raw_results}
    print(monkey_dict)

    inspect_dict = {m.id: 0 for m in raw_results}

    for round_val in range(0, 20):
        print(f'After Round {round_val}, the monkeys are holding items with these worry levels:')
        for monkey in raw_results:
            for item_idx in range(0, len(monkey.items)):
                inspect_dict[monkey.id] += 1
                new_bored_level, new_monkey_id = monkey.inspect_and_pop()
                monkey_dict[new_monkey_id].items.append(new_bored_level)

        for monkey in raw_results:
            m_items = ', '.join([str(s) for s in monkey.items])
            print(f'Monkey {monkey.id}: {m_items}')

    for monkey in raw_results:
        print(f'Monkey {str(monkey.id)} inspected items {str(inspect_dict[monkey.id])} times.')

    vs = list(inspect_dict.values())
    vs.sort(reverse=True)
    print(f'Top: {vs[0]}, Next Top: {vs[1]}, Monkey Busniess: {vs[0] * vs[1]}')


def part_two():
    raw_results = fetch_input(worry_divider=1)
    monkey_dict = {m.id: m for m in raw_results}
    print(monkey_dict)

    inspect_dict = {m.id: 0 for m in raw_results}

    cycle_Length = math.prod([v.test_denominator for v in raw_results])
    print(f'cycle_Length: {cycle_Length}')

    for round_val in range(0, 10000):
        print(f'After Round {round_val}, the monkeys are holding items with these worry levels:')
        for monkey in raw_results:
            # Had to use this - https://www.reddit.com/r/adventofcode/comments/zizi43/2022_day_11_part_2_learning_that_it_was_that/
            monkey.worry_modulo = cycle_Length
            for item_idx in range(0, len(monkey.items)):
                inspect_dict[monkey.id] += 1
                new_bored_level, new_monkey_id = monkey.inspect_and_pop()
                monkey_dict[new_monkey_id].items.append(new_bored_level)

    for monkey in raw_results:
        print(f'Monkey {str(monkey.id)} inspected items {str(inspect_dict[monkey.id])} times.')

    vs = list(inspect_dict.values())
    vs.sort(reverse=True)
    print(f'Top: {vs[0]}, Next Top: {vs[1]}, Monkey Busniess: {vs[0] * vs[1]}')



if __name__ == "__main__":
    part_two()
    #print(modular_square(300, 300))


