"""
User Activity Analyzer Package

This package provides functionality for analyzing user activity based on login timestamps.
"""

from .analyzer import UserActivityAnalyzer
from .constants import (
    CATEGORY_ACTIVE,
    CATEGORY_DORMANT,
    CATEGORY_INACTIVE,
    THRESHOLD_ACTIVE_DAYS,
    THRESHOLD_DORMANT_DAYS,
)

__version__ = "1.0.0"

__all__ = [
    "UserActivityAnalyzer",
    "CATEGORY_ACTIVE",
    "CATEGORY_DORMANT",
    "CATEGORY_INACTIVE",
    "THRESHOLD_ACTIVE_DAYS",
    "THRESHOLD_DORMANT_DAYS",
]
