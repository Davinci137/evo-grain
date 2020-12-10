"""Tests for mock_grains module"""
import unittest

import grain
from constants import InhibitedEnds
from mock_grains.mesh import Mesh
from typedefs import *


def _tri_prism_mesh_map(top_z: float) -> Dict[Point, Set[Point]]:
    p1_t = (-2, -1.75, 0)
    p2_t = (-2, -1.75, top_z)
    p3_t = (2, -1.75, top_z)
    p4_t = (-2, -1.75, 0)
    p5_t = (0, 1.714, 0)
    p6_t = (0, 1.714, top_z)
    return {
            p1_t: {p2_t, p3_t, p5_t},
            p2_t: {p1_t, p4_t, p6_t},
            p3_t: {p1_t, p4_t, p5_t},
            p4_t: {p2_t, p3_t, p6_t},
            p5_t: {p1_t, p3_t, p6_t},
            p6_t: {p2_t, p4_t, p5_t},
        }


TRIANGLE_NET: Net = [(0, 0), (1, 0), (1, 1)]
SQUARE_NET: Net = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
TRIANGULAR_PRISM_MESH: Mesh = Mesh(_tri_prism_mesh_map(10))


class MeshTest(unittest.TestCase):
    def test_make_valid(self):
        mesh = TRIANGULAR_PRISM_MESH
        p1_t = (-2, -1.75, 0)
        self.assertEqual({(-2, -1.75, 10), (2, -1.75, 0), (0, 1.714, 0)}, mesh[p1_t])
        self.assertEqual(6, len(mesh))
        for point in mesh:
            self.assertTrue(point in mesh)

    def test_make_valid_2D(self):
        mapping = {
            (1, 0): {(0, 1), (0, -1)},
            (0, 1): {(-1, 0), (1, 0)},
            (-1, 0): {(0, -1), (0, 1)},
            (0, -1): {(-1, 0), (1, 0)},
        }
        mesh = Mesh(mapping)
        for expected, actual in zip(mapping.values(), mesh.values()):
            self.assertEqual(expected, actual)
        self.assertEqual(6, len(mesh))
        for point in mesh:
            self.assertTrue(point in mesh)

    def test_make_invalid_directed(self):
        digraph = {
            (1, 0): {(0, 1), (0, -1)},
            (0, 1): {(-1, 0)},
            (-1, 0): {(0, -1)},
            (0, -1): {(1, 0)},
        }
        self.assertRaises(ValueError, lambda: Mesh(digraph))

    def test_make_invalid_negative_z(self):
        self.assertRaises(ValueError, lambda: Mesh(_tri_prism_mesh_map(top_z=-10)))

    def test_make_invalid_different_keys_values(self):
        different = {
            (1, 0): {(0, 1), (4, -1)},
            (0, 1): {(-1, 0), (1, 0)},
            (-1, 0): {(0, -1), (0, 1)},
            (0, -1): {(-1, 0), (1, 0)},
        }
        self.assertRaises(ValueError, lambda: Mesh(different))


class Grain2DTest(unittest.TestCase):
    def test_make_simple(self):
        exp_od = 3
        exp_length = 10
        exp_inhibited = InhibitedEnds.NEITHER
        exp_net = TRIANGLE_NET
        self.check_properties(exp_od, exp_length, exp_inhibited, exp_net)

    def test_make_complex(self):
        exp_od = 4
        exp_length = 5.1
        exp_inhibited = InhibitedEnds.BOTH
        exp_net = SQUARE_NET
        self.check_properties(exp_od, exp_length, exp_inhibited, exp_net)

    def test_make_invalid_net(self):
        too_far: Net = SQUARE_NET
        self.assertRaises(
            ValueError, lambda: grain.Grain2D(1, 10, InhibitedEnds.BOTH, too_far)
        )

    def test_make_invalid_diameter(self):
        self.assertRaises(
            ValueError, lambda: grain.Grain2D(0, 1, InhibitedEnds.BOTTOM, TRIANGLE_NET)
        )
        self.assertRaises(
            ValueError,
            lambda: grain.Grain2D(-20, 1, InhibitedEnds.BOTTOM, TRIANGLE_NET),
        )

    def test_make_invalid_length(self):
        self.assertRaises(
            ValueError, lambda: grain.Grain2D(3, 0, InhibitedEnds.TOP, TRIANGLE_NET)
        )
        self.assertRaises(
            ValueError, lambda: grain.Grain2D(3, -1, InhibitedEnds.TOP, TRIANGLE_NET)
        )

    def test_convert_to_openMotor(self):
        raise NotImplementedError

    def check_properties(self, exp_od, exp_length, exp_inhibited, exp_net):
        actual = grain.Grain2D(exp_od, exp_length, exp_inhibited, exp_net)
        self.assertEqual(exp_od, actual.outer_diameter)
        self.assertEqual(exp_length, actual.length)
        self.assertEqual(exp_inhibited, actual.inhibited_ends)
        self.assertEqual(exp_net, actual.net)


class ConvertNetUnitTest(unittest.TestCase):
    def test_convert_net_unit(self):
        expected: Net = [(0, 0), (1 / 25.4, 0), (1 / 25.4, 1 / 25.4)]
        actual = grain.mm_net_to_inch_net(TRIANGLE_NET)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(actual)):
            for j in range(2):  # check x and y coordinates
                self.assertAlmostEqual(expected[i][j], actual[i][j])


class Grain3DTest(unittest.TestCase):
    def test_make_simple(self):
        exp_od = 6
        exp_length = 10
        exp_inhibited = InhibitedEnds.NEITHER
        exp_mesh = TRIANGULAR_PRISM_MESH
        self.check_properties(exp_od, exp_length, exp_inhibited, exp_mesh)

    def test_make_complex(self):
        raise NotImplementedError

    def check_properties(self, exp_od, exp_length, exp_inhibited, exp_mesh):
        actual = grain.Grain3D(exp_od, exp_length, exp_inhibited, exp_mesh)
        self.assertEqual(exp_od, actual.outer_diameter)
        self.assertEqual(exp_length, actual.length)
        self.assertEqual(exp_inhibited, actual.inhibited_ends)
        self.assertEqual(exp_mesh, actual.mesh)


if __name__ == "__main__":
    unittest.main()
