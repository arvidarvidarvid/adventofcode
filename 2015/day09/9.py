import json
from itertools import permutations

with open('9.txt', 'r') as f:
    my_raw_distances = f.read()


def get_distances(raw_distances):
    distances = {}
    for d in raw_distances.split('\n'):
        l1, _, l2, _, dist = d.split()
        if l1 in distances:
            distances[l1][l2] = dist
        else:
            distances[l1] = {l2: dist}
    return populate_distances(distances)


def populate_distances(distances):
    destinations = get_destinations(distances)
    new_distances = {
        d1: {d2: get_distance(distances, d1, d2)
             for d2 in destinations}
        for d1 in destinations
    }
    for k, v in new_distances.items():
        for k2, v2 in v.items():
            if v2 is None and k2 != k:
                new_distances[k][k2] = get_distance(new_distances, k, k2)

    return new_distances


def print_distances(distances):
    print json.dumps(distances, indent=2)


def get_distance(distances, l1, l2):
    dist = None
    if l1 == l2:
        return None
    if l1 in distances:
        if l2 in distances[l1]:
            if distances[l1][l2] is not None:
                dist = int(distances[l1][l2])
    if l2 in distances:
        if l1 in distances[l2]:
            if distances[l2][l1] is not None:
                dist = int(distances[l2][l1])
    if dist is None:
        raise Exception('No known route')
    return dist


def get_destinations(distances):
    destinations = []
    for k, v in distances.items():
        destinations.append(k)
        for k1, v1 in v.items():
            destinations.append(k1)
    return set(destinations)


def build_route_set(distances):
    destinations = get_destinations(distances)
    cs = permutations(destinations, len(destinations))
    return cs


def get_total_distances_for_routes(distances):
    routes = build_route_set(distances)
    route_distances = {}
    for route in routes:
        this_total = 0
        for i in range(0, len(route)):
            try:
                this_total += get_distance(distances, route[i], route[i+1])
            except IndexError:
                break
        route_distances[route] = this_total
    return route_distances


def find_shortest_route(distances):
    routes = get_total_distances_for_routes(distances)
    best_route = None
    min_so_far = None
    for r, dist in routes.items():
        # For part 2 just make this evaluation a gt instead of lt
        if dist < min_so_far or min_so_far is None:
            min_so_far = dist
            best_route = r
    return (best_route, min_so_far)


distances = get_distances(my_raw_distances)
print find_shortest_route(distances)
