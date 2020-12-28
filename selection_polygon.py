from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem
from PyQt5 import QtGui
import numpy as np
import math

from edge import Edge
from node import Node


class SelectionPolygon(QGraphicsPolygonItem):
    # NOTE! TRUE POSITIONING OFR ANY GIVEN POLYGON COORD IS self.pos() + node.pos()

    def __init__(self, points, photoviewer):
        super(SelectionPolygon, self).__init__()

        self._photoviewer = photoviewer

        self.id = len(self._photoviewer.selection_polygons)
        self.row = None
        self.col = None

        self._selected = False
        self._nodes = []
        self._edges = []
        self._scene = photoviewer.scene
        self.polygon_points = points

        polygon = QtGui.QPolygonF(self.polygon_points)

        self.setPolygon(polygon)
        self.setPen(QPen(Qt.red, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
        self.setPos(0, 0)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

    def centroid(self):
        sum_point = QPointF(0, 0)
        for point in self.polygon_points:
            sum_point += point

        return QPointF(sum_point.x()/len(self.polygon_points), sum_point.y()/len(self.polygon_points))

    def rotate(self, degrees):
        radians = np.radians(degrees)
        # todo this could be pulled out for all polygons but it would make it ugly, idk if the optimization is needed
        cos_deg = math.cos(radians)
        sin_deg = math.sin(radians)

        origin = self.centroid()

        for point, node in zip(self.polygon_points, self._nodes):
            old_x = point.x()
            point.setX(origin.x() + cos_deg * (point.x() - origin.x()) - sin_deg * (point.y() - origin.y()))
            point.setY(origin.y() + sin_deg * (old_x - origin.x()) + cos_deg * (point.y() - origin.y()))

            node.setPos(point + self.pos())

        for edge in self._edges:
            edge.adjust()

        polygon = QtGui.QPolygonF(self.polygon_points)
        self.setPolygon(polygon)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            p = self.pos()
            self.setPos(QPointF(round(p.x()), round(p.y())))

            for idx in range(0, len(self.polygon_points)):
                self._nodes[idx].setPos(self.polygon_points[idx] + self.pos())

            for edge in self._edges:
                edge.adjust()

        return super(SelectionPolygon, self).itemChange(change, value)

    def update_points_from_nodes(self):
        self.polygon_points = [node.pos() - self.pos() for node in self._nodes]
        polygon = QtGui.QPolygonF(self.polygon_points)

        self.setPolygon(polygon)

    def select(self):
        self._selected = True
        self._photoviewer.add_selected_polygon(self)

        first_node = Node(self)
        first_node.setPos(self.polygon_points[0] + self.pos())

        self._nodes = [first_node]
        self._edges = []

        self._scene.addItem(first_node)

        for idx in range(1, len(self.polygon_points)):
            new_node = Node(self)
            new_node.setPos(self.polygon_points[idx] + self.pos())
            self._scene.addItem(new_node)

            new_edge = Edge(self._nodes[idx - 1], new_node, self)
            self._scene.addItem(new_edge)

            self._nodes.append(new_node)
            self._edges.append(new_edge)

        # connect last edge to first
        new_edge = Edge(self._nodes[len(self._nodes) - 1], self._nodes[0], self)
        self._scene.addItem(new_edge)
        self._edges.append(new_edge)

    def deselect(self):
        self._selected = False

        for edge in self._edges:
            self._scene.removeItem(edge)

        for node in self._nodes:
            self._scene.removeItem(node)

        self._nodes = []
        self._edges = []

    def mousePressEvent(self, event):
        if not self._selected:
            self.select()

        super(SelectionPolygon, self).mousePressEvent(event)

    def adjusted_polygon_points(self):
        return [self.pos() + QPointF(point[0], point[1]) for point in self.polygon_points]
