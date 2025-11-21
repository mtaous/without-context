# User Activity Analyzer - Implementation Documentation

## Overview

This project implements a User Activity Analyzer module that categorizes users based on their login activity and generates summary statistics.

## Context Analysis

**Repository State:** Empty repository with no existing code or project structure.

**Conclusion:** No project context available - using generic best practices.

## Technology Stack

- **Language:** Python 3.7+
- **Database:** SQLite (for demonstration, easily adaptable to PostgreSQL, MySQL, etc.)
- **Dependencies:** Python standard library only (no external dependencies)

## Implementation Approach

### A. Constants (Requirement)

All constants are defined in `src/user_activity_analyzer/constants.py`:

- **Category Labels:**
  - `CATEGORY_ACTIVE = "ACTIVE"`
  - `CATEGORY_DORMANT = "DORMANT"`
  - `CATEGORY_INACTIVE = "INACTIVE"`

- **Time Thresholds:**
  - `THRESHOLD_ACTIVE_DAYS = 7` (logged in within last 7 days)
  - `THRESHOLD_DORMANT_DAYS = 30` (no login for 7–30 days)

- **SQL Table Names:**
  - `TABLE_USERS = "users"`
  - `TABLE_INACTIVE_LOG = "inactive_log"`

- **Error Codes:**
  - `ERROR_CODE_DATABASE_ERROR = "DB_001"`
  - `ERROR_CODE_VALIDATION_ERROR = "VAL_001"`
  - `ERROR_CODE_INVALID_DATE = "DATE_001"`
  - `ERROR_CODE_USER_NOT_FOUND = "USER_001"`

**Naming Convention:** UPPER_CASE_WITH_UNDERSCORES (standard Python constant naming)

### B. Global Variables (Requirement)

**Decision:** No global variables used.

**Rationale:** 
- No existing project style to follow
- Global variables are generally discouraged in Python best practices
- Using dependency injection instead (passing database connections as parameters)
- This makes the code more testable, maintainable, and thread-safe

**Note:** If the project context had shown globals usage (e.g., for database connections), we would have followed that pattern.

### C. Helper Functions (Requirement)

All helper functions are in `src/user_activity_analyzer/helpers.py`:

1. **`validate_user_id(user_id)`** - Validates input user IDs
2. **`validate_timestamp(timestamp)`** - Validates timestamp data
3. **`parse_timestamp(timestamp_str)`** - Parses timestamp strings to datetime objects
4. **`convert_datetime_to_days_difference(last_login, reference_time)`** - Converts datetime to days difference
5. **`categorize_user(days_since_login)`** - Categorizes a user based on days since login
6. **`build_summary_statistics(user_categories)`** - Builds summary statistics

**Naming Convention:** lowercase_with_underscores (standard Python function naming)

### D. SQL Requirements (Requirement)

**SQL Formatting:**
- Multi-line SQL statements for readability
- Proper indentation
- No dynamic SQL (all queries use parameterized statements)

**Bind Variables:**
- All user inputs are bound using parameterized queries (? placeholders)
- Example: `cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))`

**SQL Exception Handling:**
- All database operations wrapped in try/except blocks
- Custom exceptions (`ActivityLoaderError`, `DatabaseWriterError`) with error codes
- Proper error messages with context

**Transactions:**
- Used for batch operations (logging multiple inactive users)
- Proper rollback on errors
- Configurable via `use_transaction` parameter

**Table Scanning:**
- Single query to fetch all users: `SELECT user_id, last_login FROM users`
- Avoids N+1 query problem
- Efficient batch processing

### E. File Separation Requirements (Requirement)

The solution is split into appropriate modules:

```
src/user_activity_analyzer/
├── __init__.py           # Package exports
├── constants.py          # All constants
├── helpers.py            # Helper functions
├── activity_loader.py    # Database loading operations
├── user_classifier.py    # User categorization logic
├── db_writer.py          # Database writing operations
├── activity_summary.py   # Summary statistics building
└── analyzer.py           # Main orchestrator
```

**Naming Convention:** lowercase_with_underscores (standard Python module naming)

**Separation of Concerns:**
- Each module has a single, well-defined responsibility
- Clear interfaces between modules
- Easy to test and maintain

## Module Details

### 1. `constants.py`
Defines all constants used throughout the application.

### 2. `helpers.py`
Pure utility functions with no side effects. Easy to test and reuse.

### 3. `activity_loader.py`
- **Class:** `ActivityLoader`
- **Responsibility:** Load user data from the database
- **Methods:**
  - `load_user_ids()` - Load all user IDs
  - `load_user_last_login(user_id)` - Load single user's last login
  - `load_all_users_with_login()` - Efficient batch loading

### 4. `user_classifier.py`
- **Class:** `UserClassifier`
- **Responsibility:** Classify users into categories
- **Methods:**
  - `classify_user(user_id, last_login)` - Classify single user
  - `classify_users(users)` - Classify multiple users

### 5. `db_writer.py`
- **Class:** `DatabaseWriter`
- **Responsibility:** Write inactive users to database
- **Methods:**
  - `ensure_inactive_log_table()` - Create table if needed
  - `log_inactive_user(...)` - Log single user
  - `log_inactive_users(...)` - Log multiple users with transaction

### 6. `activity_summary.py`
- **Class:** `ActivitySummary`
- **Responsibility:** Build and format summary statistics
- **Methods:**
  - `get_summary()` - Get raw summary dict
  - `get_formatted_summary()` - Get formatted text output

### 7. `analyzer.py`
- **Class:** `UserActivityAnalyzer`
- **Responsibility:** Orchestrate the entire analysis process
- **Methods:**
  - `analyze()` - Execute full analysis workflow
  - `get_classified_users()` - Access in-memory results
  - `get_formatted_summary()` - Get formatted output

## Workflow

The `UserActivityAnalyzer.analyze()` method orchestrates the following steps:

1. **Load Users** - Fetch all user IDs and last login timestamps from database
2. **Classify Users** - Apply categorization rules to each user
3. **Store Results** - Keep classified users in temporary in-memory structure
4. **Log Inactive Users** - Write inactive users to `inactive_log` table
5. **Build Summary** - Calculate and return summary statistics

## Summary Statistics

The returned dictionary contains:
- `total_users` (int) - Total number of users analyzed
- `active_count` (int) - Count of ACTIVE users
- `dormant_count` (int) - Count of DORMANT users
- `inactive_count` (int) - Count of INACTIVE users
- `oldest_last_login` (datetime or None) - Oldest login timestamp found

## Usage Example

```python
import sqlite3
from user_activity_analyzer import UserActivityAnalyzer

# Connect to database
conn = sqlite3.connect("your_database.db")

# Create analyzer
analyzer = UserActivityAnalyzer(conn)

# Run analysis
summary = analyzer.analyze()

# Print results
print(f"Total users: {summary['total_users']}")
print(f"Active: {summary['active_count']}")
print(f"Dormant: {summary['dormant_count']}")
print(f"Inactive: {summary['inactive_count']}")

# Or get formatted summary
print(analyzer.get_formatted_summary())

conn.close()
```

## Design Decisions Explained

### 1. Why Python?
- **Reason:** No project context to dictate language
- **Choice:** Python for its excellent database support, readability, and widespread use
- **Alternative:** Could easily adapt to Java, JavaScript, Go, etc.

### 2. Why SQLite?
- **Reason:** Easy to demonstrate and test
- **Flexibility:** Code is designed to work with any DB-API 2.0 compatible database
- **Adaptation:** Just change connection string and minor SQL syntax differences

### 3. Why No Globals?
- **Reason:** No project context showing globals usage
- **Best Practice:** Dependency injection is more maintainable and testable
- **Would Change If:** Project context showed global connection pools, cursors, etc.

### 4. Why Class-Based Architecture?
- **Reason:** Encapsulation of related functionality
- **Benefit:** Easy to initialize with different configurations (e.g., different reference times)
- **Alternative:** Could use functional approach if project context showed that pattern

### 5. Why Separate Modules?
- **Reason:** Single Responsibility Principle
- **Benefit:** Each module can be tested independently
- **Maintenance:** Easy to modify one aspect without affecting others

## What Was Ambiguous

Without project context, the following were ambiguous and decided using best practices:

1. **Programming Language** - Chose Python (popular, good for DB work)
2. **Database Type** - Chose SQLite (easy demo, adaptable)
3. **Error Handling Style** - Chose custom exceptions with error codes
4. **Logging Strategy** - Chose simple database logging (could add file/console logging)
5. **Testing Framework** - Chose simple assertions (can add pytest)
6. **Documentation Style** - Chose detailed docstrings
7. **Code Style** - Chose PEP 8 (standard Python style)
8. **Module Organization** - Chose class-based with clear separation

## Testing

Tests are provided in the `tests/` directory:

- `test_constants.py` - Verify all constants are defined correctly
- `test_helpers.py` - Test all helper functions
- `test_integration.py` - End-to-end integration tests

Run tests with:
```bash
python tests/test_constants.py
python tests/test_helpers.py
python tests/test_integration.py
```

Or with pytest:
```bash
pip install pytest
pytest tests/
```

## Future Enhancements

If project context becomes available, consider:

1. Adapting to project's actual database (PostgreSQL, MySQL, etc.)
2. Following project's logging conventions
3. Matching project's error handling patterns
4. Integrating with project's existing user management system
5. Adding project-specific authentication/authorization
6. Following project's specific code style guide
7. Using project's existing testing framework

## Conclusion

This implementation provides a complete, production-ready User Activity Analyzer that:
- ✓ Meets all requirements (constants, helpers, file separation, SQL best practices)
- ✓ Uses best practices in absence of project context
- ✓ Is well-documented and tested
- ✓ Is easily adaptable to specific project requirements
- ✓ Is maintainable and extensible
