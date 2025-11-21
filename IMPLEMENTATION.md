# User Activity Analyzer - Genero BDL Implementation

## Overview

This project implements a User Activity Analyzer module in **Genero BDL (4GL)** from Four Js. The module categorizes users based on their login activity and generates summary statistics.

## Context Analysis

**Repository State:** Empty repository with no existing Genero BDL code or project structure.

**Language Required:** Genero BDL (Business Development Language) from 4js

**Conclusion:** No project context available - using Genero BDL best practices and conventions.

## Technology Stack

- **Language:** Genero BDL (4GL) - Four Js Business Development Language
- **Database:** Informix (default for Genero, can be adapted to other databases)
- **File Extension:** .4gl (Genero source files)

## Implementation Approach

### A. Constants (Requirement)

All constants are defined in `constants.4gl`:

- **Category Labels:**
  - `CONSTANT CATEGORY_ACTIVE = "ACTIVE"`
  - `CONSTANT CATEGORY_DORMANT = "DORMANT"`
  - `CONSTANT CATEGORY_INACTIVE = "INACTIVE"`

- **Time Thresholds:**
  - `CONSTANT THRESHOLD_ACTIVE_DAYS = 7`
  - `CONSTANT THRESHOLD_DORMANT_DAYS = 30`

- **SQL Table Names:**
  - `CONSTANT TABLE_USERS = "users"`
  - `CONSTANT TABLE_INACTIVE_LOG = "inactive_log"`

- **Error Codes:**
  - `CONSTANT ERROR_CODE_DATABASE_ERROR = "DB_001"`
  - `CONSTANT ERROR_CODE_VALIDATION_ERROR = "VAL_001"`
  - `CONSTANT ERROR_CODE_INVALID_DATE = "DATE_001"`
  - `CONSTANT ERROR_CODE_USER_NOT_FOUND = "USER_001"`

**Naming Convention:** UPPER_CASE_WITH_UNDERSCORES (Genero BDL constant convention)

### B. Global Variables (Requirement)

**Decision:** No global variables used.

**Rationale:**
- No existing project style to follow
- Genero BDL best practices support modular programming without globals
- Using parameter passing and local variables instead
- More maintainable and follows structured programming principles

**Note:** Genero BDL supports globals (DEFINE GLOBAL), but they are not used here as there's no project context requiring them.

### C. Helper Functions (Requirement)

All helper functions are in `helpers.4gl`:

1. **`validate_user_id(p_user_id)`** - Validates input user IDs
2. **`validate_timestamp(p_timestamp)`** - Validates timestamp data
3. **`convert_datetime_to_days_difference(p_last_login)`** - Converts datetime to days difference
4. **`categorize_user(p_days_since_login)`** - Categorizes a user based on days since login
5. **`build_summary_statistics(p_classified_users, p_summary)`** - Builds summary statistics

**Naming Convention:** lowercase_with_underscores for functions (Genero BDL convention)
**Parameter Convention:** p_ prefix for parameters, l_ prefix for local variables

### D. SQL Requirements (Requirement)

**SQL Formatting:**
- Embedded SQL statements in Genero BDL code
- Proper indentation and multi-line for readability
- Uses WHENEVER ERROR for exception handling

**Bind Variables:**
- All user inputs are bound using Genero BDL's implicit binding
- Example: `WHERE user_id = p_user_id` (no explicit placeholders needed)

**SQL Exception Handling:**
- Uses `WHENEVER ERROR CONTINUE` for controlled error handling
- Checks `SQLCA.SQLCODE` for error detection
- Proper error messages with context
- Uses `WHENEVER ERROR STOP` to restore default behavior

**Transactions:**
- Used for batch operations (logging multiple inactive users)
- `BEGIN WORK` / `COMMIT WORK` / `ROLLBACK WORK`
- Proper rollback on errors
- Configurable via `p_use_transaction` parameter

**Table Scanning:**
- Single query with cursor to fetch all users efficiently
- Avoids N+1 query problem
- Uses `DECLARE CURSOR` with `FOREACH` loop

### E. File Separation Requirements (Requirement)

The solution is split into appropriate modules:

```
Genero BDL Files (.4gl):
├── constants.4gl         # All constants
├── helpers.4gl           # Helper functions
├── activity_loader.4gl   # Database loading operations
├── user_classifier.4gl   # User categorization logic
├── db_writer.4gl         # Database writing operations
├── activity_summary.4gl  # Summary statistics building
└── analyzer.4gl          # Main orchestrator
```

**Naming Convention:** lowercase_with_underscores.4gl (Genero BDL module naming)

**Module Imports:** Uses `IMPORT FGL modulename` for module dependencies

## Module Details

### 1. `constants.4gl`
Defines all constants using `CONSTANT` keyword (Genero BDL compile-time constants).

### 2. `helpers.4gl`
Pure utility functions with clear parameter passing. Uses Genero BDL data types:
- `INTEGER` for numeric values
- `DATETIME YEAR TO SECOND` for timestamps
- `VARCHAR(n)` for strings
- `BOOLEAN` for true/false values
- `INTERVAL DAY(9) TO DAY` for date differences

### 3. `activity_loader.4gl`
- **Functions:**
  - `load_user_ids(p_user_ids)` - Load all user IDs
  - `load_user_last_login(p_user_id, p_last_login)` - Load single user's last login
  - `load_all_users_with_login(p_users)` - Efficient batch loading
- Uses cursor-based fetching with `DECLARE CURSOR` and `FOREACH`

### 4. `user_classifier.4gl`
- **Functions:**
  - `classify_user(...)` - Classify single user
  - `classify_users(...)` - Classify multiple users
- Uses dynamic arrays with records for data structures

### 5. `db_writer.4gl`
- **Functions:**
  - `ensure_inactive_log_table()` - Create table if needed
  - `log_inactive_user(...)` - Log single user
  - `log_inactive_users(...)` - Log multiple users with transaction
- Uses `BEGIN WORK`/`COMMIT WORK` for transaction control

### 6. `activity_summary.4gl`
- **Functions:**
  - `display_summary(p_summary)` - Display formatted summary
  - `get_summary_statistics(...)` - Get summary statistics
- Uses formatted output with `DISPLAY` and `USING` format strings

### 7. `analyzer.4gl`
- **Main Program:** Entry point with `MAIN` block
- **Function:** `analyze_user_activity(p_summary)` - Reusable analysis function
- Orchestrates the entire workflow

## Genero BDL-Specific Features Used

1. **DYNAMIC ARRAY OF RECORD** - Flexible data structures for user collections
2. **DATETIME YEAR TO SECOND** - Precise timestamp handling
3. **WHENEVER ERROR** - SQL exception handling
4. **SQLCA.SQLCODE** - Error code checking
5. **CURSOR / FOREACH** - Efficient database iteration
6. **BEGIN WORK / COMMIT WORK** - Transaction support
7. **IMPORT FGL** - Module importing
8. **CONSTANT** - Compile-time constants
9. **INTERVAL** - Date/time arithmetic
10. **USING format** - Formatted numeric output

## Workflow

The `analyzer.4gl` main program orchestrates these steps:

1. **Load Users** - Fetch all user IDs and last login timestamps from database
2. **Classify Users** - Apply categorization rules to each user
3. **Store Results** - Keep classified users in dynamic array (in-memory structure)
4. **Log Inactive Users** - Write inactive users to `inactive_log` table
5. **Build Summary** - Calculate and display summary statistics

## Summary Statistics

The returned record contains:
- `total_users` (INTEGER) - Total number of users analyzed
- `active_count` (INTEGER) - Count of ACTIVE users
- `dormant_count` (INTEGER) - Count of DORMANT users
- `inactive_count` (INTEGER) - Count of INACTIVE users
- `oldest_last_login` (DATETIME) - Oldest login timestamp found

## Database Schema

### users table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    last_login DATETIME YEAR TO SECOND
)
```

### inactive_log table
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

### Compile modules:
```bash
fglcomp constants.4gl
fglcomp helpers.4gl
fglcomp activity_loader.4gl
fglcomp user_classifier.4gl
fglcomp db_writer.4gl
fglcomp activity_summary.4gl
fglcomp analyzer.4gl
```

### Link program:
```bash
fgllink analyzer
```

### Run program:
```bash
fglrun analyzer
```

## Design Decisions Explained

### 1. Why Genero BDL?
- **Requirement:** User specifically requested "in genero bdl from 4js"
- **Choice:** Genero BDL (Business Development Language) from Four Js
- **Context:** Enterprise business application language, commonly used with Informix

### 2. Why .4gl files?
- **Reason:** Standard Genero BDL source file extension
- **Convention:** One logical module per .4gl file

### 3. Why No Globals?
- **Reason:** No project context showing globals usage
- **Best Practice:** Genero BDL supports modular programming with parameters
- **Would Change If:** Project context showed global cursors or connection handles

### 4. Why Dynamic Arrays with Records?
- **Reason:** Genero BDL's primary data structure for collections
- **Benefit:** Type-safe, flexible, and efficient
- **Alternative:** Could use static arrays if size is known

### 5. Why WHENEVER ERROR pattern?
- **Reason:** Standard Genero BDL error handling mechanism
- **Benefit:** Clean error detection and recovery
- **Pattern:** CONTINUE for controlled handling, check SQLCODE, restore with STOP

### 6. Why Cursors?
- **Reason:** Standard Genero BDL pattern for result set iteration
- **Benefit:** Memory efficient, works with any result set size
- **Pattern:** DECLARE, FOREACH, CLOSE, FREE

### 7. Why Parameter Prefixes (p_, l_)?
- **Reason:** Common Genero BDL convention for clarity
- **Benefit:** Easy to distinguish parameters from local variables
- **Convention:** p_ = parameter, l_ = local

### 8. Why IMPORT FGL?
- **Reason:** Genero BDL module system
- **Benefit:** Proper dependency management and namespace control
- **Pattern:** Each module imports what it needs

## What Was Ambiguous

Without project context, the following were ambiguous and decided using Genero BDL best practices:

1. **Database Type** - Chose Informix (standard for Genero, syntax shown is Informix)
2. **Error Handling Style** - Chose WHENEVER ERROR pattern (standard Genero)
3. **Module Organization** - Chose one module per file (common practice)
4. **Naming Conventions** - Chose lowercase_with_underscores (Genero standard)
5. **Parameter Prefixes** - Chose p_/l_ convention (common in Genero)
6. **Data Structures** - Chose DYNAMIC ARRAY OF RECORD (flexible, type-safe)
7. **Transaction Usage** - Chose explicit BEGIN WORK/COMMIT (best practice)
8. **Display Format** - Chose simple text output (can be adapted to GUI)

## Genero BDL Best Practices Followed

1. **Explicit Type Definitions** - All variables explicitly typed
2. **Structured Programming** - Clear function boundaries, no GOTO usage
3. **Error Handling** - Consistent WHENEVER ERROR pattern
4. **Resource Management** - Proper cursor cleanup (CLOSE, FREE)
5. **Transaction Safety** - Rollback on errors
6. **Modular Design** - Clear separation of concerns
7. **Documentation** - Comprehensive function headers
8. **Naming Conventions** - Consistent naming throughout

## Future Enhancements

If project context becomes available, consider:

1. Adapting to project's actual database (Oracle, DB2, etc.)
2. Following project's specific naming conventions
3. Matching project's error handling patterns
4. Integrating with project's existing modules
5. Adding GUI forms (.per files) if needed
6. Using project's logging framework
7. Following project-specific coding standards

## Conclusion

This implementation provides a complete, production-ready User Activity Analyzer in Genero BDL that:
- ✓ Meets all requirements (constants, helpers, file separation, SQL best practices)
- ✓ Uses Genero BDL best practices in absence of project context
- ✓ Is well-documented with clear function headers
- ✓ Is easily adaptable to specific project requirements
- ✓ Is maintainable and follows structured programming principles
- ✓ Uses standard Genero BDL features and patterns
