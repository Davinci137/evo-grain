"""Functions for converting nets to meshes"""
from typing import Dict, Set

from mock_grains.mesh import Mesh
from mock_grains.typedefs import Net, Point3D


def net_to_2D_mesh(net: Net) -> Mesh:
    """
    Convert a net to its equivalent mesh representation, where points are 2D

    :param net: net to convert
    :return: the equivalent 2D mesh representation to this net
    """
    n = len(net)
    mapping = {net[i]: {net[i - 1], net[(i + 1) % n]} for i in range(n)}
    return Mesh(mapping)


def net_to_3D_mesh(net: Net, length: float) -> Mesh:
    """
    Convert a net to its equivalent mesh representation, where points are 3D

    :param net: net to convert
    :param length: length of grain
    :return: the equivalent 3D mesh representation to this net
    """
    mesh_2d = net_to_2D_mesh(net)
    mesh_3d_map: Dict[Point3D, Set[Point3D]] = {}
    for u, adjacent in mesh_2d.items():
        bottom_u = (u[0], u[1], 0)
        top_u = (u[0], u[1], length)
        mesh_3d_map[bottom_u] = {top_u} | {(v[0], v[1], 0) for v in adjacent}
        mesh_3d_map[top_u] = {bottom_u} | {(v[0], v[1], length) for v in adjacent}
    return Mesh(mesh_3d_map)
