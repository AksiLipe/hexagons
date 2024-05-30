import math
import random
import plotly.express as px
import numpy as np
from itertools import product


def count_dist(map_data, a_idx, b_idx):
    a_data = map_data[a_idx][:3]
    b_data = map_data[b_idx][:3]

    return math.sqrt(sum((a_data - b_data) ** 2))


ALL_MOVEMENTS = np.array([
    [0, 1, -1],
    [1, 0, -1],
    [1, -1, 0],
    [0, -1, 1],
    [-1, 0, 1],
    [-1, 1, 0]
])

PLAIN_TYPE = 1

river_movements = ALL_MOVEMENTS[0:2]

RIVERS_COUNT = 40

MAX_RIVER_LENGTH = 7

RIVER_TYPE = 10

HILLS_COUNT = 10

HILLS_TYPE = 100

ROUTE_TYPE = 1000

types_map = {
    PLAIN_TYPE: "Plain",
    HILLS_TYPE: "Hill",
    RIVER_TYPE: "River",
    ROUTE_TYPE: "Route"
}

vfunc = np.vectorize(types_map.get)


def create_map(max_dist):
    n = max_dist * 2 + 1
    data = np.array([i + (PLAIN_TYPE,) for i in product(range(n), repeat=3)])
    return data


def get_hex_idxs(coords_map, c):
    res = np.where((np.sum(coords_map[:, :3], axis=1) == 3 * c))[0]

    return res


def is_valid_point(point, c):
    return np.all(point >= 0) and np.all(point < 2 * c + 1)


def generate_rivers(map_data, hex_idxs, c):
    river_map = np.copy(map_data)
    for i in range(RIVERS_COUNT):
        length = random.randint(1, MAX_RIVER_LENGTH)
        current_idx = random.choice(hex_idxs)
        current = river_map[current_idx, :3]

        for _ in range(length):
            movement = random.choice(river_movements)
            new_point = current + movement
            if is_valid_point(new_point, c):
                new_point_idx = np.where((river_map[:, :3] == new_point).all(axis=1))[0]

                river_map[new_point_idx, 3] = RIVER_TYPE
                current = new_point
    return river_map


def generate_hills(map_data, hex_idxs, c):
    hills_map = np.copy(map_data)

    for _ in range(HILLS_COUNT):
        random_idx = random.choice(hex_idxs)
        point = hills_map[random_idx, :3]
        hills_map[random_idx, 3] = HILLS_TYPE
        for movement in ALL_MOVEMENTS:
            neighbor_point = point + movement
            if is_valid_point(neighbor_point, c):
                neighbor_point_idx = np.where((hills_map[:, :3] == neighbor_point).all(axis=1))[0]
                hills_map[neighbor_point_idx, 3] = HILLS_TYPE

    return hills_map


def visualize_solve(route_map, route_path):
    for cell_idx in route_path:
        route_map[cell_idx][-1] = ROUTE_TYPE

    return route_map


def show(hex_data, hex_idxs):
    colors = vfunc(hex_data[:, 3])

    fig = px.scatter_3d(
        hex_data,
        x=hex_data[:, 0],
        y=hex_data[:, 1],
        z=hex_data[:, 2],
        hover_name=hex_idxs,
        color=colors,
        color_discrete_sequence=["#387C44", "gray", "#3EA99F", 'maroon'],
    )
    fig.show()


MAX_DIST = 20
np.random.seed(42)
random.seed(42)


def main():
    map_data = create_map(MAX_DIST)
    hexagon_idxs = get_hex_idxs(map_data, MAX_DIST)
    map_data = generate_rivers(map_data, hexagon_idxs, MAX_DIST)
    map_data = generate_hills(map_data, hexagon_idxs, MAX_DIST)

    hexagon_data = map_data[hexagon_idxs]
    show(hexagon_data, hexagon_idxs)


if __name__ == '__main__':
    main()
