"""
User Classifier module for User Activity Analyzer.

This module handles the categorization of users based on their login activity.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from .helpers import (
    validate_user_id,
    validate_timestamp,
    convert_datetime_to_days_difference,
    categorize_user,
)


class UserClassifier:
    """
    Classifies users based on their last login activity.
    """
    
    def __init__(self, reference_time: Optional[datetime] = None):
        """
        Initialize the UserClassifier.
        
        Args:
            reference_time: Optional reference time for calculating days difference
                          (defaults to current UTC time)
        """
        self.reference_time = reference_time or datetime.now(timezone.utc)
    
    def classify_user(self, user_id: int, last_login: Optional[datetime]) -> Dict[str, Any]:
        """
        Classify a single user based on their last login.
        
        Args:
            user_id: The user ID
            last_login: The last login timestamp (None if never logged in)
            
        Returns:
            dict: User classification data with keys:
                - user_id: int
                - last_login: datetime or None
                - days_since_login: int or None
                - category: str
        """
        # Validate user ID
        if not validate_user_id(user_id):
            raise ValueError(f"Invalid user ID: {user_id}")
        
        # If user has never logged in, treat as inactive
        if last_login is None:
            return {
                "user_id": user_id,
                "last_login": None,
                "days_since_login": None,
                "category": "INACTIVE",  # Never logged in = inactive
            }
        
        # Validate timestamp
        if not validate_timestamp(last_login):
            raise ValueError(f"Invalid timestamp for user {user_id}: {last_login}")
        
        # Calculate days since login
        days_since_login = convert_datetime_to_days_difference(
            last_login, self.reference_time
        )
        
        # Categorize user
        category = categorize_user(days_since_login)
        
        return {
            "user_id": user_id,
            "last_login": last_login,
            "days_since_login": days_since_login,
            "category": category,
        }
    
    def classify_users(self, users: List[tuple]) -> List[Dict[str, Any]]:
        """
        Classify multiple users.
        
        Args:
            users: List of (user_id, last_login) tuples
            
        Returns:
            List[dict]: List of user classification dictionaries
        """
        classified_users = []
        
        for user_id, last_login in users:
            classified_user = self.classify_user(user_id, last_login)
            classified_users.append(classified_user)
        
        return classified_users
