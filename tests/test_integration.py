"""
Integration tests for the User Activity Analyzer.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sqlite3
from datetime import datetime, timedelta, timezone

from user_activity_analyzer import UserActivityAnalyzer
from user_activity_analyzer.constants import (
    TABLE_USERS,
    TABLE_INACTIVE_LOG,
    CATEGORY_ACTIVE,
    CATEGORY_DORMANT,
    CATEGORY_INACTIVE,
)


def setup_test_database():
    """Create a test database with sample users."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute(f"""
        CREATE TABLE {TABLE_USERS} (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            last_login TEXT
        )
    """)
    
    now = datetime.now(timezone.utc)
    
    # Insert test users
    test_users = [
        (1, "active_user1", (now - timedelta(days=1)).isoformat()),
        (2, "active_user2", (now - timedelta(days=5)).isoformat()),
        (3, "dormant_user1", (now - timedelta(days=15)).isoformat()),
        (4, "dormant_user2", (now - timedelta(days=25)).isoformat()),
        (5, "inactive_user1", (now - timedelta(days=45)).isoformat()),
        (6, "inactive_user2", (now - timedelta(days=90)).isoformat()),
        (7, "never_logged_in", None),
    ]
    
    cursor.executemany(
        f"INSERT INTO {TABLE_USERS} (user_id, username, last_login) VALUES (?, ?, ?)",
        test_users
    )
    
    conn.commit()
    return conn


def test_full_analysis():
    """Test the complete analysis workflow."""
    conn = setup_test_database()
    
    try:
        analyzer = UserActivityAnalyzer(conn)
        
        # Run analysis
        summary = analyzer.analyze()
        
        # Verify summary statistics
        assert summary["total_users"] == 7
        assert summary["active_count"] == 2
        assert summary["dormant_count"] == 2
        assert summary["inactive_count"] == 3  # 2 old logins + 1 never logged in
        assert summary["oldest_last_login"] is not None
        
        # Verify classified users
        classified = analyzer.get_classified_users()
        assert len(classified) == 7
        
        # Count by category
        active = sum(1 for u in classified if u["category"] == CATEGORY_ACTIVE)
        dormant = sum(1 for u in classified if u["category"] == CATEGORY_DORMANT)
        inactive = sum(1 for u in classified if u["category"] == CATEGORY_INACTIVE)
        
        assert active == 2
        assert dormant == 2
        assert inactive == 3
        
        # Verify inactive users were logged
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_INACTIVE_LOG}")
        inactive_count = cursor.fetchone()[0]
        assert inactive_count == 3
        
        # Verify inactive log contains correct users
        cursor.execute(f"SELECT user_id FROM {TABLE_INACTIVE_LOG} ORDER BY user_id")
        inactive_user_ids = [row[0] for row in cursor.fetchall()]
        assert 5 in inactive_user_ids  # inactive_user1
        assert 6 in inactive_user_ids  # inactive_user2
        assert 7 in inactive_user_ids  # never_logged_in
        
        print("✓ Full analysis test passed")
        
    finally:
        conn.close()


def test_empty_database():
    """Test analysis with empty database."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create empty users table
    cursor.execute(f"""
        CREATE TABLE {TABLE_USERS} (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            last_login TEXT
        )
    """)
    conn.commit()
    
    try:
        analyzer = UserActivityAnalyzer(conn)
        summary = analyzer.analyze()
        
        assert summary["total_users"] == 0
        assert summary["active_count"] == 0
        assert summary["dormant_count"] == 0
        assert summary["inactive_count"] == 0
        assert summary["oldest_last_login"] is None
        
        print("✓ Empty database test passed")
        
    finally:
        conn.close()


def test_formatted_summary():
    """Test formatted summary output."""
    conn = setup_test_database()
    
    try:
        analyzer = UserActivityAnalyzer(conn)
        analyzer.analyze()
        
        formatted = analyzer.get_formatted_summary()
        
        # Verify output contains expected elements
        assert "User Activity Summary" in formatted
        assert "Total Users: 7" in formatted
        assert "Active Users: 2" in formatted
        assert "Dormant Users: 2" in formatted
        assert "Inactive Users: 3" in formatted
        assert "Oldest Last Login:" in formatted
        
        print("✓ Formatted summary test passed")
        
    finally:
        conn.close()


if __name__ == "__main__":
    test_full_analysis()
    test_empty_database()
    test_formatted_summary()
    print("\nAll integration tests passed!")
