from PyQt5.QtCore import QPointF


# read for info


# from coord to pix
def pixel_map(coordinate, a, d, b, e, c, f):  # this is the order of the params in the file
    # formulas were found by solving
    # x1 = Ax + By + C
    # y1 = Dx + Ey + F
    #
    # for x and y
    x1 = coordinate.x()
    y1 = coordinate.y()
    x = (-(b*f) + (b*y1) + (c*e) - (e * x1))/-(a*e) + (b*d)
    y = (-(d*c) + (d*x1) + (a*f) - (a * y1))/-(a*e) + (b*d)

    return QPointF(x, y)


# from px to coords
def coordinate_map(coordinate, a, d, b, e, c, f):  # this is the order of the params in the file
    return QPointF((a * coordinate.x() + b * coordinate.y() + c),
                   (d * coordinate.x() + e * coordinate.y() + f))
