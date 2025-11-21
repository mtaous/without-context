"""
Constants for User Activity Analyzer module.

This module defines all constants used throughout the application including
category labels, time thresholds, SQL table names, and error codes.
"""

# Category labels for user activity status
CATEGORY_ACTIVE = "ACTIVE"
CATEGORY_DORMANT = "DORMANT"
CATEGORY_INACTIVE = "INACTIVE"

# Time thresholds in days
THRESHOLD_ACTIVE_DAYS = 7
THRESHOLD_DORMANT_DAYS = 30

# SQL table names
TABLE_USERS = "users"
TABLE_INACTIVE_LOG = "inactive_log"

# Error codes
ERROR_CODE_DATABASE_ERROR = "DB_001"
ERROR_CODE_VALIDATION_ERROR = "VAL_001"
ERROR_CODE_INVALID_DATE = "DATE_001"
ERROR_CODE_USER_NOT_FOUND = "USER_001"
