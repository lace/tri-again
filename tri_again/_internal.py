class Object:
    pass


class Mesh(Object):
    def __init__(self, mesh, name=None):
        self.mesh = mesh
        self.name = name


class Line(Object):
    def __init__(self, polyline, color=None):
        self.polyline = polyline
        self.color = color


class Point(Object):
    def __init__(self, point, name=None, color=None):
        self.point = point
        self.name = name
        self.color = color
