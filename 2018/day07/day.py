import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_dependency_pairs(puzzle_input):
    pattern = r'Step ([A-Z]+) must be finished before step ([A-Z]+) can begin.'
    dependencies = []
    for line in puzzle_input:
        groups = re.match(pattern, line)
        dependencies.append((groups[1], groups[2]))
    return dependencies


def dependency_pairs_to_dependency_tree(pairs):
    tree = {}
    for pair in pairs:
        if pair[0] not in tree:
            tree[pair[0]] = []
        if pair[1] not in tree:
            tree[pair[1]] = [pair[0]]
        else:
            tree[pair[1]].append(pair[0])
    return tree


def next_to_resolve(tree, n=1):
    ready_to_resolve = []
    for k, v in tree.items():
        if v == []:
            ready_to_resolve.append(k)
    if ready_to_resolve != []:
        return sorted(ready_to_resolve)[0:n]
    else:
        return []


def resolve_in_tree(tree, to_resolve):
    for k, v in tree.items():
        if to_resolve in v:
            v.remove(to_resolve)
    tree[to_resolve] = [123]
    return tree


def p1(puzzle_input):

    pairs = get_dependency_pairs(puzzle_input)
    tree = dependency_pairs_to_dependency_tree(pairs)
    all_steps = [k for k, v in tree.items()]

    resolve_order = ''

    while len(resolve_order) < len(all_steps):
        to_resolve = next_to_resolve(tree, n=1)[0]
        tree = resolve_in_tree(tree, to_resolve)
        resolve_order += to_resolve

    return resolve_order


def p2(puzzle_input, workers=5, base_solve_time=60):

    pairs = get_dependency_pairs(puzzle_input)
    tree = dependency_pairs_to_dependency_tree(pairs)
    all_steps = [k for k, v in tree.items()]

    resolve_order = ''
    time = 0

    in_processing = []
    worker_progress = {}
    for worker in range(workers):
        worker_progress[worker] = {'item': None, 'seconds_spent': 0}

    while len(resolve_order) < len(all_steps):

        # Try to assign new ready work items to free workers
        to_resolve = next_to_resolve(tree, n=5)
        for item in to_resolve:
            if item not in in_processing:
                for worker, progress in worker_progress.items():
                    if progress['item'] is None:
                        worker_progress[worker]['item'] = item
                        worker_progress[worker]['seconds_spent'] = 0
                        in_processing.append(item)
                        break

        # Add time to each progressing item
        for worker, progress in worker_progress.items():
            if progress['item'] is not None:
                worker_progress[worker]['seconds_spent'] += 1

        # Resolve finished work items
        for worker, progress in worker_progress.items():
            if progress['item'] is not None:
                item = progress['item']
                seconds = progress['seconds_spent']
                if seconds >= (ord(item) - 64 + base_solve_time):
                    tree = resolve_in_tree(tree, item)
                    resolve_order += item
                    worker_progress[worker]['item'] = None
                    worker_progress[worker]['seconds_spent'] = 0
                    in_processing.remove(item)

        time += 1

    return time


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 'CABDFE'
    assert p2(test_input_p1, workers=2, base_solve_time=0) == 15
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
