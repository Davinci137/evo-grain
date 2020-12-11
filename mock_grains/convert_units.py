"""Functions for converting nets and meshes from one unit to another"""
from constants import INCHES_PER_MM
from mesh import Mesh
from mock_grains.typedefs import Net


def mm_net_to_inch_net(net: Net):
    """
    Convert a net where units of points are millimeters to a net where units of points are
    inches

    :param net: a net where units of points are millimeters
    :return: the same net scaled to where units of points are inches
    """
    return [(point[0] * INCHES_PER_MM, point[1] * INCHES_PER_MM) for point in net]


def mm_mesh_to_inch_mesh(mesh: Mesh) -> Mesh:
    """
    Convert a mesh where units of points are millimeters to a mesh where units of points are
    inches

    :param mesh: a mesh where units of points are millimeters
    :return: the same mesh scaled to where units of points are inches
    """
    def scale(pt): return tuple(v * INCHES_PER_MM for v in pt)
    return Mesh(
        {scale(k): {scale(v) for v in vs} for k, vs in mesh.items()}
    )
