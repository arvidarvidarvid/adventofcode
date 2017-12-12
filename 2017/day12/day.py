import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def pipe_set(inputs):
    connections = []
    for input in inputs:
        source, destinations = input.split('<->')
        source = int(source.strip())
        destinations = [int(d.strip()) for d in destinations.split(',')]
        connections.append([source] + destinations)
    return connections


def get_connected_to(pipes, node):
    connected = [node]
    for i in [1, 2]:
        for pipe in pipes:
            if pipe[0] in connected:
                connected += pipe
    return sorted(list(set(connected)))


def get_groups(input):
    groups = 0
    flat = []
    pipes = pipe_set(input)
    for i in tqdm.tqdm(range(0, len(input))):
        g = get_connected_to(pipes, i)
        if g[0] not in flat:
            flat = list(set(flat + g))
            groups += 1
    return groups


def test():
    test_input = get_input('test.input')
    pipes = pipe_set(test_input)
    assert len(get_connected_to(pipes, 0)) == 6
    assert get_groups(test_input) == 2
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1: %s' % len(get_connected_to(pipe_set(input), 0)))
    logger.info('Result 2: %s' % get_groups(input))


if __name__ == '__main__':
    test()
    main()
