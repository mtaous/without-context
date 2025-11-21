"""
Example usage of the User Activity Analyzer module.

This script demonstrates how to use the UserActivityAnalyzer with a sample database.
"""

import sqlite3
from datetime import datetime, timedelta, timezone
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from user_activity_analyzer import UserActivityAnalyzer
from user_activity_analyzer.constants import TABLE_USERS


def setup_sample_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """
    Create a sample database with test users.
    
    Args:
        db_path: Path to database file (default: in-memory)
        
    Returns:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            last_login TEXT
        )
    """)
    
    # Current time for reference
    now = datetime.now(timezone.utc)
    
    # Sample users with different activity levels
    sample_users = [
        # Active users (within 7 days)
        (1, "alice", (now - timedelta(days=1)).isoformat()),
        (2, "bob", (now - timedelta(days=5)).isoformat()),
        (3, "charlie", (now - timedelta(days=7)).isoformat()),
        
        # Dormant users (7-30 days)
        (4, "diana", (now - timedelta(days=10)).isoformat()),
        (5, "eve", (now - timedelta(days=20)).isoformat()),
        (6, "frank", (now - timedelta(days=30)).isoformat()),
        
        # Inactive users (30+ days)
        (7, "grace", (now - timedelta(days=45)).isoformat()),
        (8, "henry", (now - timedelta(days=90)).isoformat()),
        (9, "iris", (now - timedelta(days=180)).isoformat()),
        
        # Never logged in
        (10, "john", None),
    ]
    
    cursor.executemany(
        f"INSERT INTO {TABLE_USERS} (user_id, username, last_login) VALUES (?, ?, ?)",
        sample_users
    )
    
    conn.commit()
    print(f"✓ Created sample database with {len(sample_users)} users")
    
    return conn


def main():
    """
    Main function to demonstrate the User Activity Analyzer.
    """
    print("User Activity Analyzer - Example Usage")
    print("=" * 60)
    print()
    
    # Setup sample database
    db_connection = setup_sample_database()
    
    try:
        # Create analyzer instance
        analyzer = UserActivityAnalyzer(db_connection)
        
        print("Analyzing user activity...")
        print()
        
        # Run the analysis
        summary = analyzer.analyze()
        
        # Display formatted summary
        print(analyzer.get_formatted_summary())
        print()
        
        # Display detailed results
        print("Detailed User Classifications:")
        print("-" * 60)
        
        classified_users = analyzer.get_classified_users()
        for user in classified_users:
            user_id = user['user_id']
            category = user['category']
            last_login = user.get('last_login')
            days_since = user.get('days_since_login')
            
            if last_login:
                login_str = last_login.strftime("%Y-%m-%d %H:%M:%S")
            else:
                login_str = "Never"
            
            if days_since is not None:
                days_str = f"{days_since} days ago"
            else:
                days_str = "N/A"
            
            print(f"User {user_id:3d}: {category:10s} | Last Login: {login_str:20s} | {days_str}")
        
        print()
        
        # Verify inactive log
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM inactive_log")
        inactive_logged = cursor.fetchone()[0]
        print(f"✓ Logged {inactive_logged} inactive users to database")
        
    finally:
        db_connection.close()


if __name__ == "__main__":
    main()
