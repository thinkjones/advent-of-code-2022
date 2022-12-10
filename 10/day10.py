from collections import defaultdict

INPUT_FILE = '10/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if full_line[0:4] == 'addx':
                results.append('noop')
            results.append(full_line)
    return results

# Click circuit
# Constant tick called cycle
# Figure signal sent by CPU
# Single register X
# addX V takes 2 cycles, X increases by V
# noop - 1 cycle does noting.


def to_ints(source):
    results = []
    for r in source:
        if r == 'noop':
            results.append(0)
        elif r[0:4] == 'addx':
            results.append(int(r.split(' ')[1]))
    return results


def part_one():
    raw_results = fetch_input()
    print(raw_results)
    print(len(raw_results))
    results = to_ints(raw_results)
    print(results)

    #values_required = [20, 60, 100, 140, 180, 220]
    values_required = [20, 60, 100, 140, 180, 220]
    signal_strengths = []
    starting_value = 1
    for v in values_required:
        value = starting_value + sum(results[0:v-1])
        print(f'{v}: {value}')
        signal_strengths.append(value * v)
    print(signal_strengths)
    print(sum(signal_strengths))


def part_two():
    raw_results = fetch_input()
    print(raw_results)
    print(len(raw_results))
    results = to_ints(raw_results)
    print(results)

    print(f'mod: {int(41/40)}')

    screen = ['.' for x in range(0, 240)]
    mid_pos = 1  # middle sprite position
    for idx, op in enumerate(results):
        sprite_pos = [p for p in range(mid_pos - 1, mid_pos + 2)]
        sprite_pos_str = '-'.join([str(s) for s in sprite_pos])
        print(f'# {idx}: {op}: {sprite_pos_str}')

        idx_as_sprite_pos_delta = (int(idx / 40)) * 40
        if (idx - idx_as_sprite_pos_delta) in sprite_pos:
            screen[idx] = '#'
            print('Added')
        if op != 0:
            mid_pos = mid_pos + op

    for x in range(0, int(len(screen) / 40)):
        print(''.join(screen[x * 40: (x + 1) * 40]))
    print(screen)

if __name__ == "__main__":
    #part_one()
    part_two()


