from ._internal import Line, Mesh, Point


class Scene:
    def __init__(self):
        self.children = []

    def add_mesh(self, mesh):
        self.children.append(Mesh(mesh=mesh))
        return self

    def add_line(self, polyline, color=None):
        self.children.append(Line(polyline=polyline, color=color))
        return self

    def add_point(self, point, name=None, color=None):
        self.children.append(Point(point=point, name=name, color=color))
        return self

    def write(self, filename):
        from ._collada import scene_to_collada

        dae = scene_to_collada(self)
        dae.write(filename)
