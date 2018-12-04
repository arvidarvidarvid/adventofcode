"""
from copy import deepcopy
import itertools
import math
import numpy as np
import tqdm
"""
from datetime import datetime, timedelta
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_line(line):
    date_part = line[1:17]
    _datetime = datetime.strptime(date_part, '%Y-%m-%d %H:%M')
    event_part = line[18:]
    if 'Guard' in line:
        event_type = 'shift_starts'
        pattern = r'Guard #(\d+) begins shift'
        gid = int(re.match(pattern, event_part.strip()).groups()[0])
    elif 'falls asleep' in line:
        gid = None
        event_type = 'falls_asleep'
    elif 'wakes up' in line:
        gid = None
        event_type = 'wakes_up'
    return (_datetime, event_type, gid)


def create_shift_blocks(events):
    gid = None
    blocks = []
    current_block = None
    for event in events:
        if event[1] == 'shift_starts':
            if current_block is not None:
                blocks.append(current_block)
                current_block = []
            else:
                current_block = []
            gid = event[2]
        else:
            current_block.append((event[0], event[1], gid))
    blocks.append(current_block)
    return blocks


def block_to_minutes_slept(block):
    pairs = int(len(block) / 2)
    sleep_minutes = []
    for pair in range(pairs):
        start_min = block[pair*2][0].minute
        stop_min = block[pair*2+1][0].minute
        for minute in range(start_min, stop_min):
            sleep_minutes.append(minute)
    return sleep_minutes


def guard_minutes_slept_dict(blocks):
    guard_sleep_minutes = {}
    for block in blocks:
        if block == []:
            continue
        gid = block[0][2]
        if gid not in guard_sleep_minutes:
            guard_sleep_minutes[gid] = block_to_minutes_slept(block)
        else:
            guard_sleep_minutes[gid] += block_to_minutes_slept(block)
    return guard_sleep_minutes


def minutes_to_minute_groups(minutes):
    minute_groups = {}
    for minute in minutes:
        if minute not in minute_groups:
            minute_groups[minute] = 1
        else:
            minute_groups[minute] += 1
    return minute_groups


def most_occuring_min_in_groups(minute_groups):
    most_occuring_min = None
    most_occuring_count = 0
    for _min, count in minute_groups.items():
        if count > most_occuring_count:
            most_occuring_min = _min
            most_occuring_count = count
    return most_occuring_min


def p1(puzzle_input):

    events = [parse_line(line) for line in puzzle_input]
    events = sorted(events, key=lambda x: x[0].timestamp())
    assert len(puzzle_input) == len(events)

    blocks = create_shift_blocks(events)
    guard_sleep_minutes = guard_minutes_slept_dict(blocks)

    most_sleepy_gid = None
    most_sleepy_minutes = 0
    for gid, minutes in guard_sleep_minutes.items():
        if len(minutes) > most_sleepy_minutes:
            most_sleepy_gid = gid
            most_sleepy_minutes = len(minutes)

    minute_groups = minutes_to_minute_groups(
        guard_sleep_minutes[most_sleepy_gid])

    most_occuring_min = most_occuring_min_in_groups(minute_groups)

    return most_occuring_min * most_sleepy_gid


def p2(puzzle_input):
    events = [parse_line(line) for line in puzzle_input]
    events = sorted(events, key=lambda x: x[0].timestamp())
    assert len(puzzle_input) == len(events)

    blocks = create_shift_blocks(events)
    guard_sleep_minutes = guard_minutes_slept_dict(blocks)

    guard_top_minute_slept_counts = []

    for guard, minutes in guard_sleep_minutes.items():
        minute_groups = minutes_to_minute_groups(minutes)
        most_occuring = most_occuring_min_in_groups(minute_groups)
        occuring_count = minute_groups[most_occuring]
        guard_top_minute_slept_counts.append(
            (occuring_count, most_occuring, guard))

    most_commonly_sleepy_guard = sorted(guard_top_minute_slept_counts,
                                        key=lambda x: x[0], reverse=True)[0]

    return most_commonly_sleepy_guard[1] * most_commonly_sleepy_guard[2]


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 240
    test_input_p2 = get_input('test_p1.input')
    assert p2(test_input_p2) == 4455
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
