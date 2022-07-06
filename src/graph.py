import numpy as np


class GraphPoint:
    def __init__(self, xy, angle, index, pc):
        self.xy = xy
        # Gurantee the angle is always in 0-2pi
        self.angle = angle % (2 * np.pi)
        self.index = index
        self.pc = pc

    def offset_xy(self, offset_radius):
        positions, _ = self.pc.positions_and_angles(
            offset=self.index, count=1, offset_radius=offset_radius)
        return positions[0]

    def draw_text(self, text, *, ax, offset_radius, **kwargs):
        position = self.offset_xy(offset_radius + self.pc.point_radius)
        kwargs['verticalalignment'] = 'center'
        # If the text is rotated more than +90 degrees, it becomes hard to
        # read. In this case rotate it by 180 degrees and flip the alignment.
        if np.pi / 2 <= self.angle < 3 * np.pi / 2:
            text_angle = np.pi + self.angle
            kwargs['horizontalalignment'] = 'right'
        else:
            text_angle = self.angle
            kwargs['horizontalalignment'] = 'left'

        ax.text(position[0], position[1], text,
                rotation=np.rad2deg(text_angle), rotation_mode='anchor',
                **kwargs)


def make_points(pc, *, offset=0, count=None):
    positions, angles = pc.positions_and_angles(offset=offset, count=count)
    return [
        GraphPoint(p, a, offset + i, pc)
        for i, (p, a) in enumerate(zip(positions, angles))
    ]
