from collada import Collada
from collada.geometry import Geometry
from collada.material import Effect, Material
from collada.scene import GeometryNode, MaterialNode, Node, Scene
from collada.source import FloatSource, InputList
from polliwog import Polyline
import numpy as np
from toolz import groupby
import vg
from ._scene_internal import (
    Line as InternalLine,
    Mesh as InternalMesh,
    Point as InternalPoint,
)
from ._color import normalize_color


def create_material(dae, name, color=(1, 1, 1)):
    effect = Effect(
        f"{name}_effect",
        [],
        "lambert",
        diffuse=color,
        specular=(0, 0, 0),
        double_sided=True,
    )
    material = Material(name, name, effect)
    dae.effects.append(effect)
    dae.materials.append(material)
    return MaterialNode(name, material, inputs=[])


def geometry_from_mesh(collada, mesh, material_id="tri_material", name=None):
    vertex_source_name = f"{name}_verts"
    geometry = Geometry(
        collada,
        name or "geometry0",
        str(mesh),
        [FloatSource(vertex_source_name, mesh.v, ("X", "Y", "Z"))],
    )
    input_list = InputList()
    input_list.addInput(0, "VERTEX", f"#{vertex_source_name}")
    triset = geometry.createTriangleSet(mesh.f.ravel(), input_list, material_id)
    geometry.primitives.append(triset)
    collada.geometries.append(geometry)
    return geometry


def geometry_from_segments(
    collada, vertices, edges, description, material_id="polyline_material", name=None
):
    vg.shape.check(locals(), "vertices", (-1, 3))
    vg.shape.check(locals(), "edges", (-1, 2))

    vertex_source_name = f"{name}_verts"
    vertex_source = FloatSource(vertex_source_name, vertices, ("X", "Y", "Z"))
    geometry = Geometry(collada, name, description, [vertex_source])
    input_list = InputList()
    input_list.addInput(0, "VERTEX", f"#{vertex_source_name}")
    lineset = geometry.createLineSet(edges.ravel(), input_list, material_id)
    geometry.primitives.append(lineset)
    collada.geometries.append(geometry)
    return geometry


def geometry_from_polyline(
    collada, polyline, material_id="polyline_material", name=None
):
    if not isinstance(polyline, Polyline):
        raise ValueError("Expected a Polyline")
    return geometry_from_segments(
        collada=collada,
        vertices=polyline.v,
        edges=polyline.e,
        description=str(polyline),
        material_id=material_id,
        name=name,
    )


def geometry_from_points(
    collada, points, radius, material_id="point_material", name=None
):
    vg.shape.check(locals(), "points", (-1, 3))

    offset = radius * np.eye(3)
    segments = np.repeat(points, 6, axis=0).reshape(-1, 3, 2, 3)
    segments[:, :, 0] = segments[:, :, 0] + offset
    segments[:, :, 1] = segments[:, :, 1] - offset

    vertices = segments.reshape(-1, 3)
    edges = np.arange(len(vertices)).reshape(-1, 2)

    return geometry_from_segments(
        collada=collada,
        vertices=vertices,
        edges=edges,
        description=f"{len(points)} points",
        material_id=material_id,
        name=name,
    )


def scene_to_collada(scene, name="triagain"):
    """
    Supports per-vertex color, but nothing else.
    """
    collada = Collada()

    scene = Scene(
        name,
        [
            Node(
                "root",
                children=[
                    GeometryNode(
                        geometry_from_mesh(
                            collada,
                            child.mesh,
                            name=f"mesh_geometry_{i}",
                            material_id="tri_material",
                        ),
                        [create_material(collada, name="tri_material")]
                        if i == 0
                        else [],
                    )
                    for i, child in enumerate(scene.children)
                    if isinstance(child, InternalMesh)
                ]
                + [
                    GeometryNode(
                        geometry_from_polyline(
                            collada,
                            child.polyline,
                            name=f"polyline_geometry_{i}",
                            material_id="polyline_material",
                        ),
                        [
                            create_material(
                                collada, name="polyline_material", color=(1, 0, 0)
                            )
                        ],
                    )
                    for i, child in enumerate(scene.children)
                    if isinstance(child, InternalLine)
                ]
                + [
                    GeometryNode(
                        geometry_from_points(
                            collada,
                            points=np.array([point.point for point in points]),
                            radius=scene.point_radius,
                            name=f"point_geometry_{i}",
                            material_id=f"point_material_{i}",
                        ),
                        [
                            create_material(
                                collada,
                                name=f"point_material_{i}",
                                color=normalize_color(color),
                            )
                        ],
                    )
                    for i, (color, points) in enumerate(
                        groupby(
                            lambda point: point.color,
                            [
                                child
                                for child in scene.children
                                if isinstance(child, InternalPoint)
                            ],
                        ).items()
                    )
                ],
            )
        ],
    )
    collada.scenes.append(scene)
    collada.scene = scene
    return collada
