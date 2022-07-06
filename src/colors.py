import itertools

import numpy as np


DEFAULT_CYCLE_COLORS = [
    [0.5, 0.5, 0],
    [0, 0.5, 0.5],
    [0.5, 0, 0.5],
    [0.75, 0.25, 0],
    [0.75, 0, 0.25],
    [0, 0.75, 0.25],
    [0.25, 0.75, 0],
    [0, 0.25, 0.75],
    [0.25, 0, 0.75],
]


def default_color_cycle():
    '''Returns a cycling iterator of colors.'''
    return make_color_cycle(DEFAULT_CYCLE_COLORS)


def make_color_cycle(colors):
    '''Returns a cycling iterator from a list of colors.'''
    colors = np.array(colors, dtype=np.float)
    if colors.ndim != 2 or colors.shape[1] != 3:
        raise ValueError('colors should be a 2D array of colors (Nx3)')
    return itertools.cycle(colors)


def color_range(base_color, count, *, start=0.2, stop=1):
    '''Returns a gradient from black-ish up to a specific color.'''
    if count == 1:
        return np.array([base_color])
    return np.reshape(np.linspace(start, stop, count), (-1, 1)) * np.reshape(base_color, (1, -1))
