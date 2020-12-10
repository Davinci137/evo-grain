from typing import Iterator, Set, Mapping

from typedefs import Point


class Mesh(Mapping[Point, Set[Point]]):
    def __init__(self, mapping: Mapping[Point, Set[Point]]):
        """
        Construct a new mesh from the provided mapping

        :param mapping: a mapping
        :raises ValueError:  if the mesh mapping has any points with a z-value less than 0, or
                            if the mesh mapping has any vertices which are not
                            non-trivially cyclic (cycle of length > 2), or
                            if the mesh mapping is directed: j in mesh[i] but not i in mesh[j],
                            or if the union of value sets is not the same as the set of keys
        """
        pass

    def __getitem__(self, p: Point) -> Point:
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator[Point]:
        pass
