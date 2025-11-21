"""
Database Writer module for User Activity Analyzer.

This module handles writing inactive user logs to the database.
"""

import sqlite3
from typing import List, Dict, Any
from datetime import datetime, timezone
from .constants import TABLE_INACTIVE_LOG, TABLE_USERS, CATEGORY_INACTIVE, ERROR_CODE_DATABASE_ERROR


class DatabaseWriterError(Exception):
    """Exception raised for errors in the DatabaseWriter."""
    
    def __init__(self, message: str, error_code: str = ERROR_CODE_DATABASE_ERROR):
        self.error_code = error_code
        super().__init__(f"[{error_code}] {message}")


class DatabaseWriter:
    """
    Writes inactive user data to the database.
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initialize the DatabaseWriter.
        
        Args:
            db_connection: SQLite database connection
        """
        self.db_connection = db_connection
    
    def ensure_inactive_log_table(self) -> None:
        """
        Ensure the inactive_log table exists.
        
        Raises:
            DatabaseWriterError: If table creation fails
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_INACTIVE_LOG} (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    last_login TEXT,
                    days_since_login INTEGER,
                    logged_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(user_id)
                )
            """)
            self.db_connection.commit()
        except sqlite3.Error as e:
            raise DatabaseWriterError(f"Failed to create inactive_log table: {str(e)}")
    
    def log_inactive_user(self, user_id: int, last_login: datetime = None, 
                         days_since_login: int = None) -> None:
        """
        Log a single inactive user to the database.
        
        Args:
            user_id: The user ID
            last_login: The last login timestamp (optional)
            days_since_login: Days since last login (optional)
            
        Raises:
            DatabaseWriterError: If database operation fails
        """
        try:
            cursor = self.db_connection.cursor()
            logged_at = datetime.now(timezone.utc).isoformat()
            
            last_login_str = last_login.isoformat() if last_login else None
            
            cursor.execute(
                f"""
                INSERT INTO {TABLE_INACTIVE_LOG} 
                (user_id, last_login, days_since_login, logged_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, last_login_str, days_since_login, logged_at)
            )
            
        except sqlite3.Error as e:
            raise DatabaseWriterError(f"Failed to log inactive user {user_id}: {str(e)}")
    
    def log_inactive_users(self, classified_users: List[Dict[str, Any]], 
                          use_transaction: bool = True) -> int:
        """
        Log all inactive users to the database.
        
        Args:
            classified_users: List of classified user dictionaries
            use_transaction: Whether to use a transaction (default True)
            
        Returns:
            int: Number of inactive users logged
            
        Raises:
            DatabaseWriterError: If database operation fails
        """
        # Ensure table exists
        self.ensure_inactive_log_table()
        
        inactive_users = [
            user for user in classified_users 
            if user.get("category") == CATEGORY_INACTIVE
        ]
        
        if not inactive_users:
            return 0
        
        try:
            if use_transaction:
                self.db_connection.execute("BEGIN TRANSACTION")
            
            for user in inactive_users:
                self.log_inactive_user(
                    user_id=user["user_id"],
                    last_login=user.get("last_login"),
                    days_since_login=user.get("days_since_login")
                )
            
            if use_transaction:
                self.db_connection.commit()
            
            return len(inactive_users)
            
        except sqlite3.Error as e:
            if use_transaction:
                self.db_connection.rollback()
            raise DatabaseWriterError(f"Failed to log inactive users: {str(e)}")
