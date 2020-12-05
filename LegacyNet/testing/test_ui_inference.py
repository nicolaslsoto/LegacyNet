import sys
import unittest

import PyQt5
from PIL import Image
from PyQt5.QtTest import QTest

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.uic.properties import QtWidgets

import tensorflow as tf

from main import Window

app = QApplication(sys.argv)


class InferenceUiTest(unittest.TestCase):
    def test_inference(self):
        window = Window()
        window.image = Image.open("../test_data/graves_small.png")
        window.detect_fn = tf.saved_model.load("../ml/run9/saved_model")
        window.detect_gravestones()
        literal_pts = [(51.26742750406265, 142.48606532812119),
                       (51.26742750406265, 167.80804574489594),
                       (66.45438686013222, 167.80804574489594),
                       (66.45438686013222, 142.48606532812119),
                       (64.48887929320335, 77.39109113812447),
                       (64.48887929320335, 103.09586346149445),
                       (80.54988875985146, 103.09586346149445),
                       (80.54988875985146, 77.39109113812447),
                       (77.37902238965034, 14.716905392706394),
                       (77.37902238965034, 38.48378852009773),
                       (93.71639370918274, 38.48378852009773),
                       (93.71639370918274, 14.716905392706394)]

        # round because we are dealing with floats, 5 digits of precision is good enough
        # do it in code just to be surely consistent, this will never be the bottleneck if we are loading the
        # model in testing
        rounded_pts = {(round(pt[0], 5), round(pt[1], 5)) for pt in literal_pts}

        results = {(round(pt.x(), 5), round(pt.y(), 5))
                   for poly in window.viewer.selection_polygons for pt in poly.polygon_points}

        self.assertEqual(len(results), len(rounded_pts), "results had a different number of points than literal")

        for point in results:
            self.assertIn(point, rounded_pts)
            rounded_pts.remove(point)


if __name__ == '__main__':
    unittest.main()
