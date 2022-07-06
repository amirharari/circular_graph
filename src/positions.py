import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def offset_angle_for(point_count, *, align='point', side='left'):
    side_to_base = {
        'right': 0,
        'top': np.pi / 2,
        'left': np.pi,
        'bottom': 3 * np.pi / 2
    }
    space = np.pi * 2 / point_count / 2
    align_to_offset = {
        'before_point': +space,
        'point': 0,
        'after_point': -space
    }
    return side_to_base[side] + align_to_offset[align]


class NodePositionCalculator:
    def __init__(self, total_nodes, point_size, *, center=(0, 0), spacing=0, offset_angle=0):
        self.total_nodes = total_nodes
        self.point_size = point_size
        self.center = np.array(center)
        self.spacing = spacing
        self.offset_angle = offset_angle

    @property
    def position_radius(self):
        #
        #      *
        #     /|\
        #    / t \
        #   /  |  \
        #  *-------*
        #
        # t = 360 / N
        # sin(t/2) = (point_size/2) / R
        t = 2 * np.pi / self.total_nodes
        radius = (self.point_size + self.spacing) / 2 / np.sin(t / 2)
        return radius

    @property
    def point_radius(self):
        return self.point_size / 2

    @property
    def outter_radius(self):
        return self.position_radius + self.point_radius

    def angles_(self, *, offset=0, count=None):
        if count is None:
            count = self.total_nodes - offset
        angles = self.offset_angle + \
            np.linspace(0, 2 * np.pi, self.total_nodes + 1)[:-1]
        # Take only the desired nodes
        return angles[offset:offset + count]

    def positions_and_angles(self, *, offset=0, count=None, offset_radius=0):
        angles = self.angles_(offset=offset, count=count)
        # Compute unit circle points
        x = np.cos(angles)
        y = np.sin(angles)
        unit_points = np.transpose([x, y])
        # Combine everything together
        positions = np.reshape(self.center, (1, 2)) + \
            (self.position_radius + offset_radius) * unit_points
        return positions, angles

    def positions_to_patches(self, positions, **kwargs):
        return [
            plt.Circle(pt, self.point_radius, **kwargs)
            for pt in positions
        ]

    def arc_patch(self, *, offset, count, offset_radius, **kwargs):
        angles = self.angles(offset=offset, count=count)
        angle_s, angle_e = angles[0], angles[-1]
        radius = self.outter_radius + offset_radius
        return patches.Arc(self.center, radius * 2, radius * 2, theta1=angle_s, theta2=angle_e, **kwargs)

    def make_patches(self):
        positions, _ = self.positions_and_angles()
        return self.positions_to_patches(positions)

    def xbounds(self, *, padding=0):
        d = self.outter_radius + padding
        return np.array([-d, +d]) + self.center[0]

    def ybounds(self, *, padding=0):
        d = self.outter_radius + padding
        return np.array([-d, +d]) + self.center[1]

    def set_bounds(self, ax=None, *, padding=0):
        ax = ax or plt.gca()
        ax.set_xlim(*self.xbounds(padding=padding))
        ax.set_ylim(*self.ybounds(padding=padding))
