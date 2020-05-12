from collada import Collada
from collada.geometry import Geometry
from collada.material import Effect, Material
from collada.scene import GeometryNode, MaterialNode, Node, Scene
from collada.source import FloatSource, InputList
import numpy as np
from ._internal import (
    Line as InternalLine,
    Mesh as InternalMesh,
    Point as InternalPoint,
)


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
    offset = radius * np.eye(3)
    segments = np.repeat(points, 6, axis=0).reshape(-1, 3, 2, 3)
    segments[:, :, 0] = segments[:, :, 0] + offset
    segments[:, :, 1] = segments[:, :, 1] - offset
    return geometry_from_segments(
        collada=collada,
        vertices=segments.reshape(-1, 2, 3),
        edges=np.arange(2 * len(segments)).reshape(-1, 2),
        description=f"{len(points)} points",
        material_id=material_id,
        name=name,
    )


def _geometry_from_mesh(dae, mesh):

    extra_materials = []
    # e
    if mesh.e is not None:
        if e_color is None:
            indices = np.dstack([mesh.e for _ in srcs]).ravel()
            lineset = geometry.createLineSet(indices, input_list, "line_material")
            geometry.primitives.append(lineset)
        else:
            edges_rendered = np.zeros(len(mesh.e), dtype=np.bool)
            for i, this_e_color in enumerate(e_color):
                these_edge_indices = this_e_color["e_indices"]
                this_color = this_e_color["color"]
                material_name = "line_material_{}".format(i)
                indices = np.dstack([mesh.e[these_edge_indices] for _ in srcs]).ravel()
                extra_materials.append(
                    create_material(dae, name=material_name, color=this_color)
                )
                lineset = geometry.createLineSet(indices, input_list, material_name)
                geometry.primitives.append(lineset)
                edges_rendered[these_edge_indices] = True
            edges_remaining = (~edges_rendered).nonzero()
            if len(edges_remaining):
                indices = np.dstack([mesh.e[edges_remaining] for _ in srcs]).ravel()
                lineset = geometry.createLineSet(indices, input_list, "line_material")
                geometry.primitives.append(lineset)

    dae.geometries.append(geometry)
    return geometry, extra_materials


# def add_landmark_points(mesh, coords, radius=DEFAULT_RADIUS):


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
                            points=np.array(
                                [
                                    child.point
                                    for i, child in enumerate(scene.children)
                                    if isinstance(child, InternalPoint)
                                ]
                            ),
                            name=f"polyline_geometry_0",
                            material_id="point_material",
                        ),
                        [
                            create_material(
                                collada, name="point_material", color=(1, 0, 0)
                            )
                        ],
                    )
                ],
            )
        ],
    )
    collada.scenes.append(scene)
    collada.scene = scene
    return collada
