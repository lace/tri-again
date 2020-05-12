from lacecore import shapes
import numpy as np
from polliwog import Polyline
from . import Scene


def test_example():
    scene = (
        Scene(point_radius=0.1)
        .add_meshes(
            shapes.cube(np.zeros(3), 3.0), shapes.cube(np.array([5.0, 0.0, 0.0]), 1.0)
        )
        .add_lines(
            Polyline(
                np.array([[5.5, 0.5, 0.0], [5.5, 0.75, 0.0], [5.5, 0.5, -0.5]]),
                is_closed=True,
            ),
            Polyline(
                np.array([[1.5, 1.5, 0.0], [1.5, 1.75, 0.0], [1.5, 1.5, -0.5]]),
                is_closed=True,
            ),
        )
        .add_points(np.zeros(3), np.array([5.0, 0.0, 0.0]))
    )
    scene.write("example.dae")
