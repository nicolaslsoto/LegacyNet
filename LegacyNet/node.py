from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QRadialGradient, QColor, QBrush, QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QStyle


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, polygon):
        super(Node, self).__init__()

        self._polygon = polygon

        self.edgeList = []
        self.newPos = QPointF()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(5)

    def type(self):
        return Node.Type

    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-5, -5, 10, 10)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)

        gradient = QRadialGradient(0, 0, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setColorAt(1, QColor(QtCore.Qt.yellow).lighter(120))
            gradient.setColorAt(0, QColor(QtCore.Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-5, -5, 10, 10)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            p = self.pos()
            self.setPos(QPointF(round(p.x()), round(p.y())))
            for edge in self.edgeList:
                edge.adjust()

        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        self._polygon.update_points_from_nodes()
        super(Node, self).mouseReleaseEvent(event)
