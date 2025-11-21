"""
Tests for the constants module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_activity_analyzer.constants import (
    CATEGORY_ACTIVE,
    CATEGORY_DORMANT,
    CATEGORY_INACTIVE,
    THRESHOLD_ACTIVE_DAYS,
    THRESHOLD_DORMANT_DAYS,
    TABLE_USERS,
    TABLE_INACTIVE_LOG,
    ERROR_CODE_DATABASE_ERROR,
    ERROR_CODE_VALIDATION_ERROR,
)


def test_category_constants():
    """Test that category constants are defined correctly."""
    assert CATEGORY_ACTIVE == "ACTIVE"
    assert CATEGORY_DORMANT == "DORMANT"
    assert CATEGORY_INACTIVE == "INACTIVE"


def test_threshold_constants():
    """Test that threshold constants are defined correctly."""
    assert THRESHOLD_ACTIVE_DAYS == 7
    assert THRESHOLD_DORMANT_DAYS == 30


def test_table_name_constants():
    """Test that table name constants are defined correctly."""
    assert TABLE_USERS == "users"
    assert TABLE_INACTIVE_LOG == "inactive_log"


def test_error_code_constants():
    """Test that error code constants are defined correctly."""
    assert ERROR_CODE_DATABASE_ERROR == "DB_001"
    assert ERROR_CODE_VALIDATION_ERROR == "VAL_001"


if __name__ == "__main__":
    test_category_constants()
    test_threshold_constants()
    test_table_name_constants()
    test_error_code_constants()
    print("All constants tests passed!")
