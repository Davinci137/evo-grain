"""Tests for mock_grains module"""
import pprint
import unittest
from typing import Dict, Set

import grain
from constants import InhibitedEnds
from grain import Grain2D, Grain3D
from mesh import Mesh
from typedefs import *


def _tri_prism_mesh_map(top_z: float, bottom_z: float = 0) -> Dict[Point, Set[Point]]:
    p1_t = (-2, -1.75, bottom_z)
    p2_t = (-2, -1.75, top_z)
    p3_t = (2, -1.75, bottom_z)
    p4_t = (2, -1.75, top_z)
    p5_t = (0, 1.714, bottom_z)
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
        self.assertEqual(4, len(mesh))
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

    def test_make_invalid_no_zero_z(self):
        no_zero_z = _tri_prism_mesh_map(10, 1)
        self.assertRaises(ValueError, lambda: Mesh(no_zero_z))


class ConvertNetUnitsTest(unittest.TestCase):
    def test_convert_net_units(self):
        expected: Net = [(0, 0), (1 / 25.4, 0), (1 / 25.4, 1 / 25.4)]
        actual = grain.mm_net_to_inch_net(TRIANGLE_NET)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(actual)):
            for j in range(2):  # check x and y coordinates
                self.assertAlmostEqual(expected[i][j], actual[i][j])


# noinspection SpellCheckingInspection
class ConvertMeshUnitsTest(unittest.TestCase):
    def test_convert_mesh_units(self):
        init = _tri_prism_mesh_map(5)
        actual = grain.mm_mesh_to_inch_mesh(Mesh(init))

        def scale_point(point, factor):
            return tuple(val * factor for val in point)

        mm_to_inch = 1 / 25.4
        scaled = Mesh(
            {
                scale_point(k, mm_to_inch): {
                    scale_point(v, mm_to_inch) for v in init[k]
                }
                for k in init
            }
        )
        self.assertEqual(len(scaled), len(actual))
        # Sort keys and check for almost equal
        # Sort corresponding values and check for almost equal
        exp_keys = sorted(scaled.keys())
        actual_keys = sorted(actual.keys())
        for i in range(len(actual)):
            self.assertAlmostEqual(exp_keys[i], actual_keys[i])
            self.assertEqual(len(scaled[exp_keys[i]]), len(actual[actual_keys[i]]))
            exp_vals = sorted(scaled[exp_keys[i]])
            actual_vals = sorted(actual[actual_keys[i]])
            for j in range(len(exp_vals)):
                self.assertAlmostEqual(exp_vals[j], actual_vals[j])


class ConvertNetToMeshTest(unittest.TestCase):
    def test_convert_net_to_mesh(self):
        exp = {
            (1, 0): {(1, -1), (1, 1)},
            (1, 1): {(1, 0), (0, 1)},
            (0, 1): {(1, 1), (-1, 1)},
            (-1, 1): {(0, 1), (-1, 0)},
            (-1, 0): {(-1, 1), (-1, -1)},
            (-1, -1): {(-1, 0), (0, -1)},
            (0, -1): {(-1, -1), (1, -1)},
            (1, -1): {(0, -1), (1, 0)},
        }
        self.assertEqual(exp, grain.net_to_2D_mesh(SQUARE_NET))


class ConvertNetTo3DMeshTest(unittest.TestCase):
    def test_convert_net_to_mesh_3D(self):
        exp_length = 5
        exp = {(1, 0, 0): {(1, 1, 0), (1, 0, 5), (1, -1, 0)},
               (1, 0, exp_length): {(1, 0, 0), (1, -1, exp_length), (1, 1, exp_length)},
               (1, 1, 0): {(1, 0, 0), (0, 1, 0), (1, 1, exp_length)},
               (1, 1, exp_length): {(1, 1, 0), (1, 0, exp_length), (0, 1, exp_length)},
               (0, 1, 0): {(-1, 1, 0), (1, 1, 0), (0, 1, exp_length)},
               (0, 1, exp_length): {(0, 1, 0), (-1, 1, exp_length), (1, 1, exp_length)},
               (-1, 1, 0): {(-1, 0, 0), (0, 1, 0), (-1, 1, exp_length)},
               (-1, 1, exp_length): {(-1, 1, 0), (0, 1, exp_length), (-1, 0, exp_length)},
               (-1, 0, 0): {(-1, 1, 0), (-1, 0, exp_length), (-1, -1, 0)},
               (-1, 0, exp_length): {(-1, 0, 0), (-1, 1, exp_length), (-1, -1, exp_length)},
               (-1, -1, 0): {(-1, 0, 0), (-1, -1, exp_length), (0, -1, 0)},
               (-1, -1, exp_length): {(0, -1, exp_length), (-1, 0, exp_length), (-1, -1, 0)},
               (0, -1, 0): {(0, -1, exp_length), (1, -1, 0), (-1, -1, 0)},
               (0, -1, exp_length): {(1, -1, exp_length), (-1, -1, exp_length), (0, -1, 0)},
               (1, -1, 0): {(1, 0, 0), (1, -1, exp_length), (0, -1, 0)},
               (1, -1, exp_length): {(0, -1, exp_length), (1, 0, exp_length), (1, -1, 0)}
               }
        self.assertEqual(exp, grain.net_to_3D_mesh(SQUARE_NET, exp_length))


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
            ValueError, lambda: Grain2D(1, 10, InhibitedEnds.BOTH, too_far)
        )

    def test_make_invalid_diameter(self):
        self.assertRaises(
            ValueError, lambda: Grain2D(0, 1, InhibitedEnds.BOTTOM, TRIANGLE_NET)
        )
        self.assertRaises(
            ValueError, lambda: Grain2D(-20, 1, InhibitedEnds.BOTTOM, TRIANGLE_NET),
        )

    def test_make_invalid_length(self):
        self.assertRaises(
            ValueError, lambda: Grain2D(3, 0, InhibitedEnds.TOP, TRIANGLE_NET)
        )
        self.assertRaises(
            ValueError, lambda: Grain2D(3, -1, InhibitedEnds.TOP, TRIANGLE_NET)
        )

    def test_convert_to_openMotor(self):
        raise NotImplementedError

    def check_properties(self, exp_od, exp_length, exp_inhibited, exp_net):
        actual = Grain2D(exp_od, exp_length, exp_inhibited, exp_net)
        self.assertEqual(exp_od, actual.outer_diameter)
        self.assertEqual(exp_length, actual.length)
        self.assertEqual(exp_inhibited, actual.inhibited_ends)
        self.assertEqual(exp_net, actual.net)


class Grain3DTest(unittest.TestCase):
    def test_make_simple(self):
        exp_od = 6
        exp_length = 10
        exp_inhibited = InhibitedEnds.NEITHER
        exp_mesh = TRIANGULAR_PRISM_MESH
        self.check_properties(exp_od, exp_length, exp_inhibited, exp_mesh)

    def test_make_complex(self):
        exp_od = 4
        exp_length = 5
        exp_inhibited = InhibitedEnds.TOP
        exp_mesh: Mesh = grain.net_to_3D_mesh(SQUARE_NET, exp_length)
        self.check_properties(exp_od, exp_length, exp_inhibited, exp_mesh)

    def test_make_invalid_mesh_length(self):  # mesh is invalid for length
        self.assertRaises(
            ValueError,
            lambda: Grain3D(6, 9, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )
        self.assertRaises(
            ValueError,
            lambda: Grain3D(6, 11, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )

    def test_make_invalid_mesh_radius(self):  # mesh is invalid for outer diameter
        self.assertRaises(
            ValueError,
            lambda: Grain3D(2, 10, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )

    def test_make_invalid_diameter(self):
        self.assertRaises(
            ValueError,
            lambda: Grain3D(0, 10, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )
        self.assertRaises(
            ValueError,
            lambda: Grain3D(-1, 10, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )

    def test_make_invalid_length(self):
        self.assertRaises(
            ValueError,
            lambda: Grain3D(6, 0, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )
        self.assertRaises(
            ValueError,
            lambda: Grain3D(6, -2, InhibitedEnds.BOTTOM, TRIANGULAR_PRISM_MESH),
        )

    def test_convert_to_openMotor(self):
        raise NotImplementedError

    def check_properties(self, exp_od, exp_length, exp_inhibited, exp_mesh):
        actual = grain.Grain3D(exp_od, exp_length, exp_inhibited, exp_mesh)
        self.assertEqual(exp_od, actual.outer_diameter)
        self.assertEqual(exp_length, actual.length)
        self.assertEqual(exp_inhibited, actual.inhibited_ends)
        self.assertEqual(exp_mesh, actual.mesh)


if __name__ == "__main__":
    unittest.main()
