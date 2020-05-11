from collada import Collada
from collada.geometry import Geometry
from collada.material import Effect, Material
from collada.scene import GeometryNode, MaterialNode, Node, Scene
from collada.source import FloatSource, InputList
import numpy as np
from ._internal import Mesh as InternalMesh


def create_material(dae, name, color=(1, 1, 1)):
    effect = Effect(
        f"{name}_effect",
        [],
        "lambert",
        diffuse=color,
        specular=(0, 0, 0),
        double_sided=True,
    )
    material = Material(f"{name}_material", name, effect)
    dae.effects.append(effect)
    dae.materials.append(material)
    return MaterialNode(name, material, inputs=[])


def geometry_from_mesh(collada, mesh, material_id="tri_material", name=None):
    vertex_source_name = f"{name}_verts"
    vertex_source = FloatSource(vertex_source_name, mesh.v, ("X", "Y", "Z"))
    geometry = Geometry(collada, name or "geometry0", str(mesh), [vertex_source])
    input_list = InputList()
    input_list.addInput(0, "VERTEX", f"#{vertex_source_name}")
    triset = geometry.createTriangleSet(mesh.f.ravel(), input_list, material_id)
    geometry.primitives.append(triset)
    collada.geometries.append(geometry)
    return geometry


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


def scene_to_collada(scene, name="triagain"):
    """
    Supports per-vertex color, but nothing else.
    """
    collada = Collada()

    nodes = [
        Node(
            "root",
            children=[
                GeometryNode(
                    geometry_from_mesh(collada, child.mesh, name=f"geometry_{i}"),
                    [create_material(collada, name="tri")] if i == 0 else [],
                )
                for i, child in enumerate(scene.children)
                if isinstance(child, InternalMesh)
            ],
        )
    ]
    import pdb

    pdb.set_trace()

    scene = Scene(name, nodes)
    # [
    #     Node(
    #         "node0",
    #         children=[
    #             GeometryNode(
    #                 geometry,
    #                 [
    #                     create_material(collada, name="tri_material"),
    #                     create_material(
    #                         collada, name="line_material", color=(1, 0, 0)
    #                     ),
    #                 ]
    #                 + extra_materials,
    #             )
    #         ],
    #     )
    # ],
    collada.scenes.append(scene)
    collada.scene = scene
    return collada
