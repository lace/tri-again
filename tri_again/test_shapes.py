from lacecore import Mesh, shapes
import numpy as np
from ._shapes import sphere as create_sphere, subdivide
from . import Scene


def test_subdivide_square():
    cube = shapes.cube(np.zeros(3), 1.0)
    just_a_square = Mesh(v=cube.v[:4], f=cube.f[:2])
    subdivided = subdivide(just_a_square)

    Scene().add_meshes(subdivided).write("subdivided_square.dae")

    np.testing.assert_array_equal(
        subdivided.v,
        np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 1.0],
                [0.0, 0.0, 1.0],
                [0.5, 0.0, 0.0],
                [0.5, 0.0, 0.5],
                [1.0, 0.0, 0.5],
                [0.5, 0.0, 1.0],
                [0.5, 0.0, 0.5],
                [0.0, 0.0, 0.5],
            ]
        ),
    )
    np.testing.assert_array_equal(
        subdivided.f,
        np.array(
            [
                [0, 4, 8],
                [4, 1, 6],
                [6, 2, 8],
                [4, 6, 8],
                [0, 5, 9],
                [5, 2, 7],
                [7, 3, 9],
                [5, 7, 9],
            ]
        ),
    )


def test_subdivide_cube():
    cube = shapes.cube(np.zeros(3), 1.0)
    subdivided = subdivide(cube)

    Scene().add_meshes(subdivided).write("subdivided_cube.dae")


def test_sphere():
    sphere = create_sphere(np.zeros(3), 1.0)
    subdivided = subdivide(sphere)

    Scene().add_meshes(subdivided).write("sphere.dae")
