import random
import math
from fieldpy.simulator import Simulator
from fieldpy.simulator import Node
from typing import Tuple


def grid_generation(simulator: Simulator, width: int, height: int, spacing: float):
    """
    Generate a grid of nodes in the simulator's environment.
    """
    for x in range(0, width):
        for y in range(0, height):
            position = (x * spacing, y * spacing)
            simulator.create_node(position, id = x * height + y)

def deformed_lattice(simulator: Simulator, width: int, height: int, spacing: float, deformation_factor: float):
    """
    Generate a deformed lattice of nodes in the simulator's environment.
    """
    for x in range(0, width):
        for y in range(0, height):
            # Randomly deform the position
            dx = random.uniform(-deformation_factor, deformation_factor)
            dy = random.uniform(-deformation_factor, deformation_factor)
            position = (x * spacing + dx, y * spacing + dy)
            simulator.create_node(position, id = x * height + y)

def random_walk(simulator: Simulator, num_steps: int, step_size: float):
    """
    Perform a random walk and create nodes at each step.
    """
    position = (0.0, 0.0)
    for _ in range(num_steps):
        dx = random.uniform(-step_size, step_size)
        dy = random.uniform(-step_size, step_size)
        position = (position[0] + dx, position[1] + dy)
        simulator.create_node(position)

def random_in_circle(simulator: Simulator, num_nodes: int, radius: float):
    """
    Generate nodes randomly distributed within a circle.
    """
    for index in range(num_nodes):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, radius)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        simulator.create_node((x, y), id = index)

def gaussian_movement(simulator: Simulator, node: Node, mean: Tuple[float, ...], stddev: float):
    """
    Move a node according to a Gaussian distribution.
    """
    new_position = tuple(
        random.gauss(mean[i], stddev) for i in range(len(mean))
    )
    node.update(new_position)
    # next schedule the event
    simulator.schedule_event(1.0, gaussian_movement, simulator, node, mean, stddev)
