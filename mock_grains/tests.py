"""Tests for mock_grains module"""
import unittest

import grain
from constants import InhibitedEnds
from typedefs import *

TRIANGLE_NET: Net = [(0, 0), (1, 0), (1, 1)]
SQUARE_NET: Net = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


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

    def test_make_invalid_length(self):
        self.assertRaises(
            ValueError, lambda: grain.Grain2D(3, 0, InhibitedEnds.TOP, TRIANGLE_NET)
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
            for j in range(2):  # check x and y co-ordinates
                self.assertAlmostEqual(expected[i][j], actual[i][j])


if __name__ == "__main__":
    unittest.main()
