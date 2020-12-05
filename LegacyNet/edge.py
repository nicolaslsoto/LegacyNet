import math

from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF, QSizeF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsItem


class Edge(QGraphicsItem):
    Type = QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode, polygon):
        super(Edge, self).__init__()

        self._polygon = polygon

        self.sourcePoint = QPointF()
        self.destPoint = QPointF()

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()
        self.setZValue(2)

    def type(self):
        return Edge.Type

    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QLineF(self.mapFromItem(self.source, 0, 0),
                      self.mapFromItem(self.dest, 0, 0))
        length = line.length()

        self.prepareGeometryChange()

        self.sourcePoint = line.p1()
        self.destPoint = line.p2()

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()

        return QRectF(self.sourcePoint,
                      QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                             self.destPoint.y() - self.sourcePoint.y())).normalized()

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine, Qt.RoundCap,
                            Qt.RoundJoin))
        painter.drawLine(line)
