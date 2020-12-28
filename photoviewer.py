from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsLineItem
from numpy.linalg import norm
import numpy as np

from selection_polygon import SelectionPolygon


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)

        # all gravestone-denoting polygons
        self.selection_polygons = []

        self.box_creation_mode = False
        self.box_start_point = None
        self._box_graphic = None

        self.line_selection_mode = False
        self.start_line_select = None
        self.line_graphic = None

        self.ctrl_held = False

        # the polygons currently selected for editing
        self.selected_polygons = []
        self.update_selected = None

        self._zoom = 0
        self._empty = True
        self.scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()

        self.scene.addItem(self._photo)
        self.setScene(self.scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def add_selected_polygon(self, polygon):
        self.selected_polygons.append(polygon)

        if self.update_selected is not None:
            self.update_selected()

    def remove_selected_polygon(self, polygon):
        self.selected_polygons.remove(polygon)

        if self.update_selected is not None:
            self.update_selected(self.selected_polygons)

    def has_photo(self):
        return not self._empty

    def pixmap(self):
        return self._photo

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def set_photo(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)

            self.selection_polygons = []
            self.box_creation_mode = False
            self.box_start_point = None
            self._box_graphic = None

            for poly in self.selected_polygons:
                self.remove_selected_polygon(poly)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.has_photo():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def delete_selected(self):
        for selected in self.selected_polygons:
            selected.deselect()
            self.scene.removeItem(selected)
            self.selection_polygons.remove(selected)

        self.selected_polygons = []

    def any_selection_nodes_under_mouse(self):
        for selected in self.selected_polygons:
            for node in selected._nodes:
                if node.isUnderMouse():
                    return True

        return False

    def deselect_all(self):
        for polygon in self.selected_polygons:
            polygon.deselect()
        self.selected_polygons = []
        if self.update_selected is not None:
            self.update_selected()

    def remove_all(self):
        """ Delete all polygons """
        self.deselect_all()
        for polygon in self.selection_polygons:
            self.scene.removeItem(polygon)
        self.selection_polygons.clear()

    def mousePressEvent(self, event):
        if not self._photo.isUnderMouse():
            return
        if self.box_creation_mode:
            photo_click_point = self.mapToScene(event.pos()).toPoint()
            self.box_start_point = photo_click_point

            self._box_graphic = QGraphicsRectItem(0, 0, 1, 1)
            self._box_graphic.setBrush(QBrush(Qt.transparent))
            self._box_graphic.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self._box_graphic.setPos(photo_click_point)
            self.scene.addItem(self._box_graphic)
        elif self.line_selection_mode and self.start_line_select is None:
            photo_click_point = self.mapToScene(event.pos()).toPoint()
            self.start_line_select = photo_click_point
            self.line_graphic = QGraphicsLineItem()
            self.line_graphic.setPen(QPen(Qt.green, 4, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
            self.scene.addItem(self.line_graphic)
        else:
            # this is pretty hacky and ugly but it works well
            if not self.any_selection_nodes_under_mouse() and not self.ctrl_held:
                self.deselect_all()
            super(PhotoViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._photo.isUnderMouse():
            return
        if self.box_creation_mode and self.box_start_point is not None:
            photo_click_point = self.mapToScene(event.pos()).toPoint()
            polygon_coords = [QPointF(self.box_start_point.x(), self.box_start_point.y()),
                              QPointF(self.box_start_point.x(), photo_click_point.y()),
                              QPointF(photo_click_point.x(), photo_click_point.y()),
                              QPointF(photo_click_point.x(), self.box_start_point.y())]
            selection_polygon = SelectionPolygon(polygon_coords, self)
            self.add_selection_polygon(selection_polygon)
            self.scene.removeItem(self._box_graphic)

            self.box_creation_mode = False
            self.box_start_point = None
            self._box_graphic = None
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        elif self.line_selection_mode and self.start_line_select is not None:
            # line select
            self.deselect_all()

            photo_click_point = self.mapToScene(event.pos()).toPoint()
            self.scene.removeItem(self.line_graphic)

            for polygon in self.selection_polygons:
                line = [np.array([photo_click_point.x(), photo_click_point.y()]),
                        np.array([self.start_line_select.x(), self.start_line_select.y()])]
                centroid = polygon.centroid()

                # max node dist from centroid, used for approximations
                max_dist = 0.0
                for point in polygon.polygon_points:
                    # todo manhattan length is a bad approx of euclid. dist, maybe its not worth the inaccuracy
                    dist = (point - centroid).manhattanLength()
                    if dist > max_dist:
                        max_dist = dist

                np_centroid = np.array([centroid.x(), centroid.y()])
                distance_from_line = np.abs(np.cross(line[1] - line[0], line[0] - np_centroid)) / norm(
                    line[0] - line[1])

                if distance_from_line <= max_dist:
                    min_x = min(photo_click_point.x(), self.start_line_select.x()) * .95
                    max_x = max(photo_click_point.x(), self.start_line_select.x()) * 1.05
                    min_y = min(photo_click_point.y(), self.start_line_select.y()) * .95
                    max_y = max(photo_click_point.y(), self.start_line_select.x()) * 1.05
                    if min_x < centroid.x() < max_x and min_y < centroid.y() < max_y:
                        polygon.select()

            self.start_line_select = None
            self.line_graphic = None
        else:
            super(PhotoViewer, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.box_creation_mode and self.box_start_point is not None and self._box_graphic is not None:
            mouse_point = self.mapToScene(event.pos()).toPoint()
            self._box_graphic.setRect(QRectF(0,
                                             0,
                                             mouse_point.x() - self.box_start_point.x(),
                                             mouse_point.y() - self.box_start_point.y()).normalized())
        elif self.line_selection_mode and self.start_line_select is not None and self.line_graphic is not None:
            mouse_point = self.mapToScene(event.pos()).toPoint()
            self.line_graphic.setLine(QLineF(mouse_point, self.start_line_select))
        super(PhotoViewer, self).mouseMoveEvent(event)

    def add_selection_polygon(self, selection_polygon):
        self.selection_polygons.append(selection_polygon)
        self.scene.addItem(selection_polygon)

    def pixmap_width_and_height(self):
        return self._photo.pixmap().width(), self._photo.pixmap().height()
