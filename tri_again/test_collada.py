from lacecore import shapes
import numpy as np
from polliwog import Polyline
from . import Scene


def test_two_cubes():
    scene = (
        Scene()
        .add_mesh(shapes.cube(np.zeros(3), 3.0))
        .add_mesh(shapes.cube(np.array([5.0, 0.0, 0.0]), 1.0))
        .add_line(
            Polyline(
                np.array([[5.5, 0.5, 0.0], [5.5, 0.75, 0.0], [5.5, 0.5, -0.5]]),
                is_closed=True,
            )
        )
        .add_line(
            Polyline(
                np.array([[1.5, 1.5, 0.0], [1.5, 1.75, 0.0], [1.5, 1.5, -0.5]]),
                is_closed=True,
            )
        )
    )
    scene.write("two_cubes.dae")
