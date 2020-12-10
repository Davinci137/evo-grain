"""Stores constants used elsewhere in mock_grains"""
import enum


class InhibitedEnds(enum.Enum):
    """Represents the inhibited ends of a grain, if any"""

    NEITHER = 0
    TOP = 1
    BOTTOM = 2
    BOTH = 3


INCHES_PER_MM = 1 / 25.4
