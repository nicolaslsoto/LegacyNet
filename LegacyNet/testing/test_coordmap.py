import unittest

from PyQt5.QtCore import QPointF

import coordmap


class CoordMapTest(unittest.TestCase):
    def test_reversal(self):
        t = (.6, .5, .4, .3, .2, .1)
        coord = coordmap.coordinate_map(QPointF(50, 50), *t)
        px = coordmap.pixel_map(coord, *t)
        self.assertAlmostEqual(px.x(), 50)
        self.assertAlmostEqual(px.y(), 50)


if __name__ == '__main__':
    unittest.main()
