"""Classes used to represent grains when interfacing with Open3D"""
from constants import *
from typedefs import *


def mm_net_to_inch_net(net: Net):
    """
    Convert a net where units of points are millimeters to a net where units of points are
    inches

    :param net: a net where units of points are millimeters
    :return: the same net scaled to where units of points are inches
    """
    return [(point[0] * INCHES_PER_MM, point[1] * INCHES_PER_MM) for point in net]


class Grain3D:
    """Represents a 3D grain; used for conversion into Open3D such that a .dxf file is made"""

    pass


class Grain2D:
    """Represents a 2D grain: constant cross-section through entire length"""

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
        self.__outer: float = outer_diameter
        self.__length: float = length
        self.__inhibited: InhibitedEnds = inhibited_ends
        self.__net: Net = net

    # noinspection PyPep8Naming
    def to_openMotor_grain(self):
        """
        Convert this grain to an openMotor grain with corresponding dimensions and geometry

        :return: the resulting openMotor grain
        """
        # TODO
        raise NotImplementedError("Unimplemented!")

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

    @property
    def net(self) -> Net:
        """
        :return: the net representing the internal geometry of the grain
        """
        return self.__net
