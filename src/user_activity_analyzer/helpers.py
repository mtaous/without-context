"""
Helper functions for User Activity Analyzer module.

This module provides utility functions for validation, date conversion,
categorization, logging, and statistics building.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from .constants import (
    CATEGORY_ACTIVE,
    CATEGORY_DORMANT,
    CATEGORY_INACTIVE,
    THRESHOLD_ACTIVE_DAYS,
    THRESHOLD_DORMANT_DAYS,
    ERROR_CODE_VALIDATION_ERROR,
    ERROR_CODE_INVALID_DATE,
)


def validate_user_id(user_id: Any) -> bool:
    """
    Validate that a user ID is valid.
    
    Args:
        user_id: The user ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if user_id is None:
        return False
    
    # Accept integers and strings that can be converted to integers
    if isinstance(user_id, int):
        return user_id > 0
    
    if isinstance(user_id, str):
        try:
            return int(user_id) > 0
        except (ValueError, TypeError):
            return False
    
    return False


def validate_timestamp(timestamp: Any) -> bool:
    """
    Validate that a timestamp is valid.
    
    Args:
        timestamp: The timestamp to validate (datetime object or ISO format string)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if timestamp is None:
        return False
    
    if isinstance(timestamp, datetime):
        return True
    
    if isinstance(timestamp, str):
        try:
            parse_timestamp(timestamp)
            return True
        except (ValueError, TypeError):
            return False
    
    return False


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse a timestamp string to a datetime object.
    
    Args:
        timestamp_str: ISO format timestamp string
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If timestamp cannot be parsed
    """
    try:
        # Try parsing ISO format with timezone
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        # Try parsing without timezone
        try:
            return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"Invalid timestamp format: {timestamp_str}")


def convert_datetime_to_days_difference(last_login: datetime, reference_time: Optional[datetime] = None) -> int:
    """
    Convert a datetime to the number of days difference from now or a reference time.
    
    Args:
        last_login: The last login datetime
        reference_time: Optional reference time (defaults to current UTC time)
        
    Returns:
        int: Number of days difference
        
    Raises:
        ValueError: If last_login is invalid
    """
    if not isinstance(last_login, datetime):
        raise ValueError(f"Invalid datetime object: {last_login}")
    
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    
    # Ensure both datetimes are timezone-aware
    if last_login.tzinfo is None:
        last_login = last_login.replace(tzinfo=timezone.utc)
    
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)
    
    difference = reference_time - last_login
    return difference.days


def categorize_user(days_since_login: int) -> str:
    """
    Categorize a user based on days since last login.
    
    Args:
        days_since_login: Number of days since last login
        
    Returns:
        str: Category label (ACTIVE, DORMANT, or INACTIVE)
    """
    if days_since_login < 0:
        # Future date, treat as active
        return CATEGORY_ACTIVE
    
    if days_since_login <= THRESHOLD_ACTIVE_DAYS:
        return CATEGORY_ACTIVE
    elif days_since_login <= THRESHOLD_DORMANT_DAYS:
        return CATEGORY_DORMANT
    else:
        return CATEGORY_INACTIVE


def build_summary_statistics(user_categories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build summary statistics from categorized users.
    
    Args:
        user_categories: List of user data dictionaries with 'category' and 'last_login'
        
    Returns:
        dict: Summary statistics including total users, category counts, and oldest login
    """
    if not user_categories:
        return {
            "total_users": 0,
            "active_count": 0,
            "dormant_count": 0,
            "inactive_count": 0,
            "oldest_last_login": None,
        }
    
    active_count = sum(1 for u in user_categories if u.get("category") == CATEGORY_ACTIVE)
    dormant_count = sum(1 for u in user_categories if u.get("category") == CATEGORY_DORMANT)
    inactive_count = sum(1 for u in user_categories if u.get("category") == CATEGORY_INACTIVE)
    
    # Find oldest last login
    oldest_login = None
    for user in user_categories:
        last_login = user.get("last_login")
        if last_login:
            if oldest_login is None or last_login < oldest_login:
                oldest_login = last_login
    
    return {
        "total_users": len(user_categories),
        "active_count": active_count,
        "dormant_count": dormant_count,
        "inactive_count": inactive_count,
        "oldest_last_login": oldest_login,
    }
