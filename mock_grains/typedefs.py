"""Convenient type aliases for types used elsewhere in mock_grains"""
from typing import List, Tuple

Point = Tuple[
    float, float
]  # points have their x-value at index 0 and y-value at index 1
Polygon = List[
    Point
]  # the ordering of a polygon indicates how the points are connected
# more formally: for a polygon p, p[i] has an edge with p[i + 1] and p[-1] has an edge with
# p[0]
# polygons must have at least 3 points
Net = Polygon
# TODO: consider making nets or polygons classes: they definitely have check-able invariants
