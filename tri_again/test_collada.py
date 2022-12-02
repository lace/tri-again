from lacecore import shapes
import numpy as np
from polliwog import Polyline
import pytest
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
        .add_points(
            np.array([0.0, 0.0, 0.3]), np.array([5.0, 0.0, 0.1]), color="SaddleBrown"
        )
        .add_points(
            np.array([0.0, 0.0, 0.6]), np.array([5.0, 0.0, 0.2]), color="SeaGreen"
        )
    )
    scene.write("example.dae")


def test_error():
    with pytest.raises(ValueError, match="Expected a Polyline"):
        Scene().add_lines("not-a-polyline").write("other.dae")

    with pytest.raises(ValueError, match="Expected filename to end with .dae"):
        Scene().write("other.usdz")

    with pytest.raises(
        ValueError,
        match="When more than one point is provided, expected `name` to be None",
    ):
        Scene().add_points(np.arange(9).reshape(-1, 3), name="foobar")
