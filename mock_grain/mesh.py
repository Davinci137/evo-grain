from copy import deepcopy
from typing import Iterator, Mapping, Set

from typedefs import Point


class Mesh(Mapping[Point, Set[Point]]):
    """
    An immutable mapping storing a mesh as an adjacency list: maps vertices to the vertices
    they have edges with.
    """

    def __init__(self, mapping: Mapping[Point, Set[Point]]):
        """
        Construct a new mesh from the provided mapping

        :param mapping: a mapping
        :raises ValueError: if the mesh mapping has any points with a z-value less than 0, or
                            if the mesh mapping has any vertices which are not
                            non-trivially cyclic (cycle of length > 2), or
                            if the mesh mapping is directed: j in mesh[i] but not i in mesh[j],
                            or if the union of value sets is not the same as the set of keys,
                            or if the mesh mapping has no point with a z-value of 0
        """
        values = {v for vs in mapping.values() for v in vs}
        if mapping.keys() != values:
            raise ValueError("There exists a point which is only a key or a value")
        has_z = False
        for point in mapping:
            if len(point) >= 3:
                has_z = True
                if point[2] < 0:
                    raise ValueError("Mesh mapping has point with z-value less than 0")
        if has_z:
            if min(point[2] for point in mapping.keys()) != 0:
                raise ValueError("Mesh mapping has no point with z-value of 0")
        for k, v in ((k, v) for k, vs in mapping.items() for v in vs):
            if k not in mapping[v]:
                raise ValueError("Mesh mapping is directed")
        self.mapping = deepcopy(mapping)

    def __getitem__(self, p: Point) -> Set[Point]:
        return self.mapping[p]

    def __len__(self) -> int:
        return len(self.mapping)

    def __iter__(self) -> Iterator[Point]:
        yield from self.mapping
