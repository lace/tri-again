import math
from lacecore import Mesh
import numpy as np
from vg.compat import v2 as vg

# Adapted from https://medium.com/@oscarsc/four-ways-to-create-a-mesh-for-a-sphere-d7956b825db4


def subdivide(mesh, project_to_unit_sphere=False):
    """
    Args:
        project_to_unit_sphere (boolean): When True, project new vertices to the
            unit sphere. This is useful for `sphere()` below.
    """
    triangles = mesh.v[mesh.f]
    new_v = np.concatenate(
        [
            np.average(triangles[:, 0:2], axis=1),  # Midpoint of AB.
            np.average(triangles[:, 1:3], axis=1),  # Midpoint of BC.
            np.average(triangles[:, 0:3:2], axis=1),  # Midpoint of AC.
        ]
    )
    if project_to_unit_sphere:
        new_v = vg.normalize(new_v)
    new_v = np.concatenate([mesh.v, new_v])

    new_f = np.zeros((0, 3), dtype=np.int64)
    for i, (a, b, c) in enumerate(mesh.f):
        # d: First midpoint of AB.
        # e: First midpoint of BC.
        # f: First midpoint of AC.
        d, e, f = mesh.num_v + np.arange(3) * len(triangles) + i
        new_f = np.vstack(
            [
                new_f,
                [a, d, f],
                [d, b, e],
                [e, c, f],
                [d, e, f],
            ]
        )
    return Mesh(v=new_v, f=new_f)


def sphere(center, radius):
    vg.shape.check(locals(), "center", (3,))

    t = (1 + math.sqrt(5)) / 2
    vertices = vg.normalize(
        np.array(
            [
                [-1, t, 0],
                [1, t, 0],
                [-1, -t, 0],
                [1, -t, 0],
                [0, -1, t],
                [0, 1, t],
                [0, -1, -t],
                [0, 1, -t],
                [t, 0, -1],
                [t, 0, 1],
                [-t, 0, -1],
                [-t, 0, 1],
            ]
        )
    )
    faces = np.array(
        [
            [0, 11, 5],
            [0, 5, 1],
            [0, 1, 7],
            [0, 7, 10],
            [0, 10, 11],
            [1, 5, 9],
            [5, 11, 4],
            [11, 10, 2],
            [10, 7, 6],
            [7, 1, 8],
            [3, 9, 4],
            [3, 4, 2],
            [3, 2, 6],
            [3, 6, 8],
            [3, 8, 9],
            [4, 9, 5],
            [2, 4, 11],
            [6, 2, 10],
            [8, 6, 7],
            [9, 8, 1],
        ]
    )
    return (
        subdivide(
            subdivide(Mesh(v=vertices, f=faces), project_to_unit_sphere=True),
            project_to_unit_sphere=True,
        )
        .transform()
        .uniform_scale(radius)
        .translate(center)
        .end()
    )
