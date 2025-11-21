"""
Activity Loader module for User Activity Analyzer.

This module handles loading user IDs and login timestamps from the database.
"""

import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
from .constants import TABLE_USERS, ERROR_CODE_DATABASE_ERROR
from .helpers import parse_timestamp


class ActivityLoaderError(Exception):
    """Exception raised for errors in the ActivityLoader."""
    
    def __init__(self, message: str, error_code: str = ERROR_CODE_DATABASE_ERROR):
        self.error_code = error_code
        super().__init__(f"[{error_code}] {message}")


class ActivityLoader:
    """
    Loads user activity data from the database.
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initialize the ActivityLoader.
        
        Args:
            db_connection: SQLite database connection
        """
        self.db_connection = db_connection
    
    def load_user_ids(self) -> List[int]:
        """
        Load all user IDs from the database.
        
        Returns:
            List[int]: List of user IDs
            
        Raises:
            ActivityLoaderError: If database operation fails
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f"SELECT user_id FROM {TABLE_USERS} ORDER BY user_id")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            raise ActivityLoaderError(f"Failed to load user IDs: {str(e)}")
    
    def load_user_last_login(self, user_id: int) -> Optional[datetime]:
        """
        Load the last login timestamp for a specific user.
        
        Args:
            user_id: The user ID to look up
            
        Returns:
            datetime: Last login timestamp, or None if user has never logged in
            
        Raises:
            ActivityLoaderError: If database operation fails
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                f"SELECT last_login FROM {TABLE_USERS} WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            
            if row is None:
                raise ActivityLoaderError(f"User ID {user_id} not found")
            
            last_login_str = row[0]
            if last_login_str is None:
                return None
            
            # Parse the timestamp string to datetime
            if isinstance(last_login_str, str):
                return parse_timestamp(last_login_str)
            elif isinstance(last_login_str, datetime):
                return last_login_str
            else:
                return None
                
        except sqlite3.Error as e:
            raise ActivityLoaderError(f"Failed to load last login for user {user_id}: {str(e)}")
    
    def load_all_users_with_login(self) -> List[Tuple[int, Optional[datetime]]]:
        """
        Load all users with their last login timestamps in a single query.
        
        Returns:
            List[Tuple[int, Optional[datetime]]]: List of (user_id, last_login) tuples
            
        Raises:
            ActivityLoaderError: If database operation fails
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                f"SELECT user_id, last_login FROM {TABLE_USERS} ORDER BY user_id"
            )
            rows = cursor.fetchall()
            
            result = []
            for user_id, last_login_str in rows:
                last_login = None
                if last_login_str is not None:
                    if isinstance(last_login_str, str):
                        last_login = parse_timestamp(last_login_str)
                    elif isinstance(last_login_str, datetime):
                        last_login = last_login_str
                
                result.append((user_id, last_login))
            
            return result
            
        except sqlite3.Error as e:
            raise ActivityLoaderError(f"Failed to load users with login data: {str(e)}")
