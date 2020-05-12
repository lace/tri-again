from ._scene_internal import Line, Mesh, Point


class Scene:
    def __init__(self, point_radius=1.0):
        self.point_radius = point_radius
        self.children = []

    def add_meshes(self, *meshes):
        for mesh in meshes:
            self.children.append(Mesh(mesh=mesh))
        return self

    def add_lines(self, *polylines, color="red"):
        for polyline in polylines:
            self.children.append(Line(polyline=polyline, color=color))
        return self

    def add_points(self, *points, name=None, color="red"):
        if len(points) > 0 and name is not None:
            raise ValueError(
                "When more than one point is provided, expected `name` to be None"
            )
        for point in points:
            self.children.append(Point(point, name=name, color=color))
        return self

    def write(self, filename):
        import os
        from ._collada import collada_from_scene

        _, extension = os.path.splitext(filename)
        if extension != ".dae":
            raise ValueError("Expected filename to end with .dae")

        dae = collada_from_scene(self)
        dae.write(filename)
