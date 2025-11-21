"""
User Activity Analyzer - Main Module

This module orchestrates the user activity analysis process by:
1. Loading user IDs and login timestamps from the database
2. Classifying users into ACTIVE, DORMANT, or INACTIVE categories
3. Logging inactive users to the database
4. Building and returning summary statistics
"""

import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime

from .activity_loader import ActivityLoader
from .user_classifier import UserClassifier
from .db_writer import DatabaseWriter
from .activity_summary import ActivitySummary


class UserActivityAnalyzer:
    """
    Main orchestrator for user activity analysis.
    """
    
    def __init__(self, db_connection: sqlite3.Connection, 
                 reference_time: Optional[datetime] = None):
        """
        Initialize the UserActivityAnalyzer.
        
        Args:
            db_connection: SQLite database connection
            reference_time: Optional reference time for classification (defaults to now)
        """
        self.db_connection = db_connection
        self.loader = ActivityLoader(db_connection)
        self.classifier = UserClassifier(reference_time)
        self.writer = DatabaseWriter(db_connection)
        
        # Temporary in-memory structure to store results
        self.classified_users: List[Dict[str, Any]] = []
    
    def analyze(self) -> Dict[str, Any]:
        """
        Execute the full user activity analysis process.
        
        Returns:
            dict: Summary statistics with keys:
                - total_users: int
                - active_count: int
                - dormant_count: int
                - inactive_count: int
                - oldest_last_login: datetime or None
        
        Raises:
            Exception: If any step of the analysis fails
        """
        # Step 1: Load users with their last login timestamps
        users = self.loader.load_all_users_with_login()
        
        # Step 2: Classify each user
        self.classified_users = self.classifier.classify_users(users)
        
        # Step 3: Log inactive users to the database
        inactive_count = self.writer.log_inactive_users(self.classified_users)
        
        # Step 4: Build and return summary statistics
        summary = ActivitySummary(self.classified_users)
        
        return summary.get_summary()
    
    def get_classified_users(self) -> List[Dict[str, Any]]:
        """
        Get the classified users from the in-memory structure.
        
        Returns:
            List[Dict[str, Any]]: List of classified user dictionaries
        """
        return self.classified_users
    
    def get_formatted_summary(self) -> str:
        """
        Get a formatted summary of the analysis results.
        
        Returns:
            str: Formatted summary text
        """
        summary = ActivitySummary(self.classified_users)
        return summary.get_formatted_summary()
