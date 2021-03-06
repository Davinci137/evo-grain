"""Classes used to represent grains when interfacing with Open3D"""
from abc import ABCMeta, abstractmethod

from constants import *
from mesh import Mesh
from typedefs import *


class Grain(metaclass=ABCMeta):
    """Abstract base class representing the generic grain"""

    __slots__ = ["__outer", "__length", "__inhibited"]

    def __init__(
        self, outer_diameter: float, length: float, inhibited_ends: InhibitedEnds
    ):
        """
        Construct a grain from the provided parameters

        :param outer_diameter: outer diameter of motor
        :param length: length of the grain
        :param inhibited_ends: which ends, if any, are inhibited
        :raises ValueError: if length <= 0, or
                            if outer_diameter <= 0, or
        """
        if length <= 0:
            raise ValueError("Must have positive length")
        if outer_diameter <= 0:
            raise ValueError("Must have positive diameter")
        self.__outer = outer_diameter
        self.__length = length
        self.__inhibited = inhibited_ends

    # noinspection PyPep8Naming
    @abstractmethod
    def to_openMotor_grain(self):
        """
        Convert this grain to an openMotor grain with corresponding dimensions and geometry

        :return: the resulting openMotor grain
        """
        pass

    @property
    def outer_diameter(self) -> float:
        """
        :return: the outer diameter of the grain
        """
        return self.__outer

    @property
    def length(self) -> float:
        """
        :return: the length of the grain
        """
        return self.__length

    @property
    def inhibited_ends(self) -> InhibitedEnds:
        """
        :return: which ends of the grain are inhibited
        """
        return self.__inhibited


class Grain2D(Grain):
    """Represents a 2D grain: constant cross-section through entire length.
    Parametrized such that evolutionary algorithm can more easily generate grains."""

    # TODO: once Grain3D is implemented, this could inherit from it

    __slots__ = ["__outer", "__length", "__inhibited", "__net"]

    def __init__(
        self,
        outer_diameter: float,
        length: float,
        inhibited_ends: InhibitedEnds,
        net: Net,
    ):
        """
        Construct a 2D grain from the provided parameters where net represents the internal
        geometry

        :param outer_diameter: outer diameter of motor
        :param length: length of the grain
        :param inhibited_ends: which ends, if any, are inhibited
        :param net: a net representing the internal geometry of this grain, where each point's
                    dimensions are in inches and the center of the grain is at (0, 0)
        :raises ValueError: if distance to any point in net from (0, 0) is greater than
                            outer_diameter / 2
                            if length <= 0
                            if outer_diameter <= 0
        """
        super().__init__(outer_diameter, length, inhibited_ends)
        if length <= 0:
            raise ValueError("Must have positive length")
        if outer_diameter <= 0:
            raise ValueError("Must have positive diameter")
        outer_rad = outer_diameter / 2
        for point in net:
            d = sum(dist ** 2 for dist in point) ** 0.5
            if d > outer_rad:
                raise ValueError(
                    f"At least one point, {point} in the provided net is further "
                    f"from center than the outer radius, {outer_rad}"
                )
        self.__net: Net = net.copy()

    # noinspection PyPep8Naming
    def to_openMotor_grain(self):
        """
        Convert this grain to an openMotor grain with corresponding dimensions and geometry

        :return: the resulting openMotor grain
        """
        # TODO
        raise NotImplementedError("Unimplemented!")

    @property
    def net(self) -> Net:
        """
        :return: the net representing the internal geometry of the grain
        """
        return self.__net


class Grain3D(Grain):
    """Represents a 3D grain.
    Parametrized such that evolutionary algorithm can more easily generate grains."""

    __slots__ = ["__outer", "__length", "__inhibited", "__mesh"]

    def __init__(
        self,
        outer_diameter: float,
        length: float,
        inhibited_ends: InhibitedEnds,
        mesh: Mesh,
    ):
        """
        Construct a 3D grain from the provided parameters where mesh represents the internal
        geometry
        :param outer_diameter: outer diameter of motor
        :param length: length of the grain
        :param inhibited_ends: which ends, if any, are inhibited
        :param mesh: the mesh mapping points to the points they're connected to;
                     should be non-trivially cyclic (cycle of length > 2) for all vertices
        :raises ValueError: if distance from any point (x, y, z) in net to (0, 0, z) is
                            greater than outer_diameter / 2, or
                            if length <= 0, or
                            if outer_diameter <= 0, or
                            if the maximum z-value of a point in the mesh is not equal to
                            length
        """
        super().__init__(outer_diameter, length, inhibited_ends)
        outer_rad = outer_diameter / 2
        has_z = False
        for point in mesh:
            if len(point) >= 3:
                has_z = True
            d = (point[0] ** 2 + point[1] ** 2) ** 0.5
            if d > outer_rad:
                raise ValueError(
                    f"At least one point, {point}, in the provided mesh is further "
                    f"from center than the outer radius, {outer_rad}"
                )
        if has_z:
            max_z = max(point[2] for point in mesh)
            if max_z != length:
                raise ValueError(
                    f"The maximum z-value of any point, {max_z}, is not equal to the provided "
                    f"length {length}"
                )
        self.__mesh = mesh  # meshes are immutable: no need to copy

    # noinspection PyPep8Naming
    def to_openMotor_grain(self):
        """
        Convert this grain to an openMotor grain with corresponding dimensions and geometry

        :return: the resulting openMotor grain
        """
        # TODO
        raise NotImplementedError("Unimplemented!")

    @property
    def mesh(self) -> Mesh:
        """
        :return: the mesh representing the internal geometry of the grain
        """
        return self.__mesh
