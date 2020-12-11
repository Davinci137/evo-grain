"""Convenient type aliases for types used elsewhere in mock_grain"""
from typing import List, Tuple, TypeVar

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]
Point = TypeVar("Point", Point2D, Point3D)
# points have their x-value at idx 0, y-value at idx 1, and z-value, if applicable, at idx 2
Polygon = List[
    Point2D
]  # the ordering of a polygon indicates how the points are connected
# more formally: for a polygon p, p[i] has an edge with p[i + 1] and p[-1] has an edge with
# p[0]
# polygons must have at least 3 points
Net = Polygon
# TODO: consider making nets or polygons classes: they definitely have check-able invariants
