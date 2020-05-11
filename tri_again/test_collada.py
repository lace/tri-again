from lacecore import shapes
import numpy as np
from . import Scene


def test_cube():
    scene = Scene().add_mesh(shapes.cube(np.zeros(3), 3.0))
    scene.write("cube.dae")


def test_two_cubes():
    scene = (
        Scene()
        .add_mesh(shapes.cube(np.zeros(3), 3.0))
        .add_mesh(shapes.cube(np.array([5.0, 0.0, 0.0]), 1.0))
    )
    scene.write("two_cubes.dae")
