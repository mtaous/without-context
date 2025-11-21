# User Activity Analyzer - Genero BDL

A Genero BDL (4GL) module for analyzing user activity based on login timestamps and categorizing users into ACTIVE, DORMANT, or INACTIVE groups.

## Overview

This implementation is written in **Genero BDL** (Business Development Language) from Four Js Development Tools. It demonstrates a complete user activity analysis system with proper modular design, SQL handling, and business logic.

## Features

- Load user IDs and login timestamps from database
- Categorize users based on login activity:
  - **ACTIVE**: Logged in within last 7 days
  - **DORMANT**: No login for 7-30 days
  - **INACTIVE**: No login for 30+ days
- Store results in dynamic arrays (in-memory structure)
- Log inactive users to database table
- Generate comprehensive summary statistics

## File Structure

```
Genero BDL Modules (.4gl):
├── constants.4gl         # Constants (categories, thresholds, table names, error codes)
├── helpers.4gl           # Helper functions (validation, conversion, categorization)
├── activity_loader.4gl   # Database loading operations
├── user_classifier.4gl   # User categorization logic
├── db_writer.4gl         # Database writing operations
├── activity_summary.4gl  # Summary statistics
└── analyzer.4gl          # Main orchestrator
```

## Requirements

- Genero BDL development environment (Four Js Genero)
- Database (Informix, Oracle, DB2, PostgreSQL, etc.)
- Tables: `users`, `inactive_log` (created automatically)

## Database Schema

### users table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    last_login DATETIME YEAR TO SECOND
)
```

### inactive_log table (created automatically)
```sql
CREATE TABLE inactive_log (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    last_login DATETIME YEAR TO SECOND,
    days_since_login INTEGER,
    logged_at DATETIME YEAR TO SECOND NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

## Compilation and Execution

### Compile all modules:
```bash
fglcomp constants.4gl
fglcomp helpers.4gl
fglcomp activity_loader.4gl
fglcomp user_classifier.4gl
fglcomp db_writer.4gl
fglcomp activity_summary.4gl
fglcomp analyzer.4gl
```

### Link the program:
```bash
fgllink analyzer
```

### Run the program:
```bash
fglrun analyzer
```

## Usage

The `analyzer.4gl` module provides two ways to use the analyzer:

### 1. As a standalone program (MAIN)
Simply run the compiled program:
```bash
fglrun analyzer
```

### 2. As a reusable function
Import and call from your own code:
```4gl
IMPORT FGL analyzer

DEFINE l_summary RECORD
    total_users INTEGER,
    active_count INTEGER,
    dormant_count INTEGER,
    inactive_count INTEGER,
    oldest_last_login DATETIME YEAR TO SECOND
END RECORD

DEFINE l_success BOOLEAN

CALL analyze_user_activity(l_summary) RETURNING l_success

IF l_success THEN
    DISPLAY "Total users: ", l_summary.total_users
    DISPLAY "Active: ", l_summary.active_count
    DISPLAY "Dormant: ", l_summary.dormant_count
    DISPLAY "Inactive: ", l_summary.inactive_count
END IF
```

## Requirements Met

This implementation fulfills all specified requirements:

### ✅ **Constants (Requirement A)**
- Category labels: ACTIVE, DORMANT, INACTIVE
- Time thresholds: 7 days, 30 days
- SQL table names: users, inactive_log
- Error codes: DB_001, VAL_001, DATE_001, USER_001
- Follows Genero BDL constant naming (UPPER_CASE)

### ✅ **Helper Functions (Requirement C)**
- `validate_user_id()` - Input validation
- `validate_timestamp()` - Timestamp validation
- `convert_datetime_to_days_difference()` - Date conversion
- `categorize_user()` - User categorization
- `build_summary_statistics()` - Statistics building
- Follows Genero BDL naming (lowercase_with_underscores)

### ✅ **SQL Requirements (Requirement D)**
- Embedded SQL with implicit binding (Genero BDL style)
- Proper exception handling with WHENEVER ERROR
- Transaction support (BEGIN WORK / COMMIT WORK)
- Efficient cursor-based iteration
- Proper resource cleanup (CLOSE/FREE cursors)

### ✅ **File Separation (Requirement E)**
- constants.4gl - All constants
- helpers.4gl - Pure utility functions
- activity_loader.4gl - Database loading
- user_classifier.4gl - Categorization logic
- db_writer.4gl - Database writing
- activity_summary.4gl - Statistics
- analyzer.4gl - Main orchestrator

### ✅ **No Globals (Requirement B)**
- No DEFINE GLOBAL used
- Using parameter passing instead
- Following Genero BDL best practices

## Genero BDL Features Used

- `CONSTANT` - Compile-time constants
- `DYNAMIC ARRAY OF RECORD` - Flexible data structures
- `DATETIME YEAR TO SECOND` - Timestamp handling
- `INTERVAL DAY(9) TO DAY` - Date arithmetic
- `WHENEVER ERROR` - SQL exception handling
- `SQLCA.SQLCODE` - Error code checking
- `DECLARE CURSOR / FOREACH` - Result set iteration
- `BEGIN WORK / COMMIT WORK` - Transaction control
- `IMPORT FGL` - Module importing

## Documentation

See documentation files for detailed information:
- **IMPLEMENTATION.md** - Complete implementation guide, design decisions, and Genero BDL features
- **EXPLANATION.md** - Detailed explanation of what was inferred vs. assumed, with Genero BDL specifics

## Context

This implementation was created for an empty repository with no existing project context. All design decisions follow **Genero BDL best practices and language conventions**. See EXPLANATION.md for details on what was inferred vs. assumed.

## License

MIT

