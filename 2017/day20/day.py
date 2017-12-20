import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class Particle(object):

    def __init__(self, id, p, v, a):
        self.id = id
        self.position = p
        self.velocity = v
        self.acceleration = a

    def distance_to_origin(self, position=None):
        if position is None:
            position = self.position
        return sum(map(abs, position))

    def get_next_position(self):
        return list(map(sum, zip(self.position, self.velocity)))

    def get_next_velocity(self):
        return list(map(sum, zip(self.velocity, self.acceleration)))

    def velocity_away_from_origin(self):
        return (self.distance_to_origin(self.get_next_position()) -
                self.distance_to_origin())

    def total_acceleration(self):
        return sum(map(abs, self.acceleration))

    def tick(self):
        self.velocity = self.get_next_velocity()
        self.position = self.get_next_position()
        return self


def get_particles(input):
    particles = []
    for id, row in enumerate(input):
        p, v, a = re.match(r'p=<(.+)>, v=<(.+)>, a=<(.+)>', row).groups()
        particles.append(Particle(id,
                                  p=[int(c.strip()) for c in p.split(',')],
                                  v=[int(c.strip()) for c in v.split(',')],
                                  a=[int(c.strip()) for c in a.split(',')]))
    return particles


def long_term_closest(particles):
    # It is easier to make the comparison when everyone is heading away from
    # origin, lets update until that is the case.
    all_moving_away = False
    while not all_moving_away:
        all_moving_away = True
        for particle in particles:
            particle.tick()
            if particle.velocity_away_from_origin() < 0:
                # It's enough that a single particle is heading towards origin
                # for this to be false
                all_moving_away = False
    # Now that we know that everyone is heading away we can see who is moving
    # away with the lowest acceleration, that will be the one that is long
    # term closest.
    slowest_accelerating = particles[0]
    lowest_velocity = particles[0].total_acceleration()
    for particle in particles:
        if particle.total_acceleration() < lowest_velocity:
            slowest_accelerating = particle
            lowest_velocity = particle.total_acceleration()
    return slowest_accelerating


def resolve_collisions(particles):
    # Let's make the assumption that as soon as everyone is moving away from
    # origin they have passed the collision point. Update until everyone is
    # moving away.
    all_moving_away = False
    while not all_moving_away:
        all_moving_away = True
        for particle in particles:
            particle.tick()
            if particle.velocity_away_from_origin() < 0:
                all_moving_away = False
        # In each step check if there are any collisions, if so remove the
        # colliders. Note that we remove at the end of the full update since we
        # can have 3+-way collisions that would not happen if we removed the
        # first two as they were found.
        to_be_removed = []
        resolved_positions = []
        for i, particle in enumerate(particles):
            if particle.position in resolved_positions:
                continue
            for potential_collider in particles[i + 1:]:
                if particle.position == potential_collider.position:
                    to_be_removed += [particle.id, potential_collider.id]
            resolved_positions.append(particle.position)
        particles = [p for p in particles if p.id not in to_be_removed]
    # Return everyone that is now heading away from origin without having
    # collided.
    return particles


def test():
    test_input_1 = get_input('test_1.input')
    assert long_term_closest(get_particles(test_input_1)).id == 0
    test_input_2 = get_input('test_2.input')
    assert len(resolve_collisions(get_particles(test_input_2))) == 1
    logger.info('Tests passed')


def main():
    input = get_input()
    logger.info('Result 1: %s' % long_term_closest(get_particles(input)).id)
    logger.info('Result 2: %s' % len(resolve_collisions(get_particles(input))))


if __name__ == '__main__':
    test()
    main()
