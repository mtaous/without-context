# User Activity Analyzer

A Python module for analyzing user activity based on login timestamps and categorizing users into ACTIVE, DORMANT, or INACTIVE groups.

## Features

- Load user IDs and login timestamps from database
- Categorize users based on login activity:
  - **ACTIVE**: Logged in within last 7 days
  - **DORMANT**: No login for 7-30 days
  - **INACTIVE**: No login for 30+ days
- Store results in temporary in-memory structure
- Log inactive users to database table
- Generate comprehensive summary statistics

## Installation

No external dependencies required - uses Python standard library only.

```bash
# Optional: Install testing dependencies
pip install -r requirements.txt
```

## Quick Start

```python
import sqlite3
from user_activity_analyzer import UserActivityAnalyzer

# Connect to your database
conn = sqlite3.connect("your_database.db")

# Create analyzer and run analysis
analyzer = UserActivityAnalyzer(conn)
summary = analyzer.analyze()

# View results
print(analyzer.get_formatted_summary())
```

## Example

Run the provided example script:

```bash
python example.py
```

## Testing

Run the test suite:

```bash
python tests/test_constants.py
python tests/test_helpers.py
python tests/test_integration.py
```

Or with pytest:

```bash
pytest tests/
```

## Documentation

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed documentation including:
- Architecture and design decisions
- Module descriptions
- SQL requirements and best practices
- File separation strategy
- Usage of constants, helpers, and proper error handling

## Project Structure

```
src/user_activity_analyzer/
├── __init__.py           # Package exports
├── constants.py          # Constants (categories, thresholds, table names)
├── helpers.py            # Helper functions (validation, conversion, categorization)
├── activity_loader.py    # Database loading operations
├── user_classifier.py    # User categorization logic
├── db_writer.py          # Database writing operations
├── activity_summary.py   # Summary statistics
└── analyzer.py           # Main orchestrator

tests/
├── test_constants.py     # Constants tests
├── test_helpers.py       # Helper function tests
└── test_integration.py   # Integration tests

example.py                # Example usage script
IMPLEMENTATION.md         # Detailed documentation
```

## Requirements Met

This implementation fulfills all specified requirements:

- ✅ **Constants**: Category labels, time thresholds, SQL table names, error codes
- ✅ **Helper Functions**: Validation, date conversion, categorization, logging, statistics
- ✅ **SQL Best Practices**: Parameterized queries, proper formatting, exception handling, transactions
- ✅ **File Separation**: Clear module separation by responsibility
- ✅ **No Globals**: Uses dependency injection instead (best practice in absence of project context)

## Context

This implementation was created for an empty repository with no existing project context. All design decisions follow Python best practices and industry standards. See IMPLEMENTATION.md for details on what was inferred vs. assumed.

## License

MIT 
