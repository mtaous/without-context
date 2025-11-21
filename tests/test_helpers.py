"""
Tests for the helpers module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import datetime, timedelta, timezone
from user_activity_analyzer.helpers import (
    validate_user_id,
    validate_timestamp,
    parse_timestamp,
    convert_datetime_to_days_difference,
    categorize_user,
    build_summary_statistics,
)
from user_activity_analyzer.constants import (
    CATEGORY_ACTIVE,
    CATEGORY_DORMANT,
    CATEGORY_INACTIVE,
)


def test_validate_user_id():
    """Test user ID validation."""
    # Valid user IDs
    assert validate_user_id(1) is True
    assert validate_user_id(100) is True
    assert validate_user_id("5") is True
    
    # Invalid user IDs
    assert validate_user_id(0) is False
    assert validate_user_id(-1) is False
    assert validate_user_id(None) is False
    assert validate_user_id("abc") is False
    assert validate_user_id("") is False


def test_validate_timestamp():
    """Test timestamp validation."""
    now = datetime.now(timezone.utc)
    
    # Valid timestamps
    assert validate_timestamp(now) is True
    assert validate_timestamp("2025-01-01T12:00:00") is True
    assert validate_timestamp("2025-01-01 12:00:00") is True
    
    # Invalid timestamps
    assert validate_timestamp(None) is False
    assert validate_timestamp("invalid") is False
    assert validate_timestamp(123) is False


def test_parse_timestamp():
    """Test timestamp parsing."""
    # ISO format with timezone
    dt1 = parse_timestamp("2025-01-01T12:00:00+00:00")
    assert dt1.year == 2025
    assert dt1.month == 1
    assert dt1.day == 1
    
    # ISO format with Z
    dt2 = parse_timestamp("2025-01-01T12:00:00Z")
    assert dt2.year == 2025
    
    # Standard format
    dt3 = parse_timestamp("2025-01-01 12:00:00")
    assert dt3.year == 2025
    
    # Invalid format should raise ValueError
    try:
        parse_timestamp("invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_convert_datetime_to_days_difference():
    """Test datetime to days difference conversion."""
    now = datetime.now(timezone.utc)
    
    # 5 days ago
    five_days_ago = now - timedelta(days=5)
    assert convert_datetime_to_days_difference(five_days_ago, now) == 5
    
    # 30 days ago
    thirty_days_ago = now - timedelta(days=30)
    assert convert_datetime_to_days_difference(thirty_days_ago, now) == 30
    
    # Same time
    assert convert_datetime_to_days_difference(now, now) == 0


def test_categorize_user():
    """Test user categorization."""
    # Active: 0-7 days
    assert categorize_user(0) == CATEGORY_ACTIVE
    assert categorize_user(5) == CATEGORY_ACTIVE
    assert categorize_user(7) == CATEGORY_ACTIVE
    
    # Dormant: 8-30 days
    assert categorize_user(8) == CATEGORY_DORMANT
    assert categorize_user(15) == CATEGORY_DORMANT
    assert categorize_user(30) == CATEGORY_DORMANT
    
    # Inactive: 31+ days
    assert categorize_user(31) == CATEGORY_INACTIVE
    assert categorize_user(100) == CATEGORY_INACTIVE
    
    # Future date (negative days)
    assert categorize_user(-1) == CATEGORY_ACTIVE


def test_build_summary_statistics():
    """Test summary statistics building."""
    now = datetime.now(timezone.utc)
    
    users = [
        {"category": CATEGORY_ACTIVE, "last_login": now - timedelta(days=1)},
        {"category": CATEGORY_ACTIVE, "last_login": now - timedelta(days=5)},
        {"category": CATEGORY_DORMANT, "last_login": now - timedelta(days=15)},
        {"category": CATEGORY_INACTIVE, "last_login": now - timedelta(days=60)},
        {"category": CATEGORY_INACTIVE, "last_login": now - timedelta(days=90)},
    ]
    
    summary = build_summary_statistics(users)
    
    assert summary["total_users"] == 5
    assert summary["active_count"] == 2
    assert summary["dormant_count"] == 1
    assert summary["inactive_count"] == 2
    assert summary["oldest_last_login"] == now - timedelta(days=90)
    
    # Empty list
    empty_summary = build_summary_statistics([])
    assert empty_summary["total_users"] == 0
    assert empty_summary["oldest_last_login"] is None


if __name__ == "__main__":
    test_validate_user_id()
    test_validate_timestamp()
    test_parse_timestamp()
    test_convert_datetime_to_days_difference()
    test_categorize_user()
    test_build_summary_statistics()
    print("All helper tests passed!")
