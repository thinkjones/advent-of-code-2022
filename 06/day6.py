from collections import defaultdict

INPUT_FILE = '06/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            results.append(full_line)
    return results[0]


class FiloQueue(object):

    def __init__(self, max_in_queue):
        self.queue = []
        self.max_in_queue = max_in_queue
        self.total_added = 0

    def add(self, value):
        self.queue.append(value)
        self.total_added += 1
        if len(self.queue) > self.max_in_queue:
            self.remove()

    def remove(self):
        return self.queue.pop(0)

    def is_unique(self):
        totals = defaultdict(int)
        for i in self.queue:
            totals[i] += 1
        return len(totals.keys()) == self.max_in_queue and len(self.queue) == self.max_in_queue


def part_one():
    results = fetch_input()
    queue = FiloQueue(4)
    count = 1
    for i in results:
        queue.add(i)
        if queue.is_unique():
            print(f'{count} - {queue.queue} - {queue.is_unique()}')
            break
        count += 1

def part_two():
    results = fetch_input()
    queue = FiloQueue(14)
    count = 1
    for i in results:
        queue.add(i)
        if queue.is_unique():
            print(f'{count} - {queue.queue} - {queue.is_unique()}')
            break
        count += 1

if __name__ == "__main__":
    part_one()
    part_two()
