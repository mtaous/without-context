"""
Activity Summary module for User Activity Analyzer.

This module handles building and formatting summary statistics.
"""

from typing import List, Dict, Any
from .helpers import build_summary_statistics


class ActivitySummary:
    """
    Builds summary statistics from classified user data.
    """
    
    def __init__(self, classified_users: List[Dict[str, Any]]):
        """
        Initialize the ActivitySummary.
        
        Args:
            classified_users: List of classified user dictionaries
        """
        self.classified_users = classified_users
        self.summary = build_summary_statistics(classified_users)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get the summary statistics.
        
        Returns:
            dict: Summary statistics with keys:
                - total_users: int
                - active_count: int
                - dormant_count: int
                - inactive_count: int
                - oldest_last_login: datetime or None
        """
        return self.summary
    
    def get_formatted_summary(self) -> str:
        """
        Get a formatted string representation of the summary.
        
        Returns:
            str: Formatted summary text
        """
        summary = self.summary
        
        lines = [
            "User Activity Summary",
            "=" * 50,
            f"Total Users: {summary['total_users']}",
            f"Active Users: {summary['active_count']} ({self._percentage(summary['active_count'], summary['total_users'])}%)",
            f"Dormant Users: {summary['dormant_count']} ({self._percentage(summary['dormant_count'], summary['total_users'])}%)",
            f"Inactive Users: {summary['inactive_count']} ({self._percentage(summary['inactive_count'], summary['total_users'])}%)",
        ]
        
        if summary['oldest_last_login']:
            lines.append(f"Oldest Last Login: {summary['oldest_last_login'].isoformat()}")
        else:
            lines.append("Oldest Last Login: N/A")
        
        return "\n".join(lines)
    
    def _percentage(self, count: int, total: int) -> str:
        """
        Calculate percentage and format to 1 decimal place.
        
        Args:
            count: The count
            total: The total
            
        Returns:
            str: Formatted percentage
        """
        if total == 0:
            return "0.0"
        return f"{(count / total * 100):.1f}"
