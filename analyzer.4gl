-- analyzer.4gl
-- User Activity Analyzer - Main Module
-- Orchestrates the user activity analysis process

IMPORT FGL activity_loader
IMPORT FGL user_classifier
IMPORT FGL db_writer
IMPORT FGL activity_summary

--------------------------------------------------------------------------------
-- MAIN: User Activity Analyzer
-- Main entry point for the user activity analysis
--------------------------------------------------------------------------------
MAIN
    DEFINE l_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_classified_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE l_summary RECORD
        total_users INTEGER,
        active_count INTEGER,
        dormant_count INTEGER,
        inactive_count INTEGER,
        oldest_last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_success BOOLEAN
    DEFINE l_inactive_count INTEGER
    
    DISPLAY "User Activity Analyzer"
    DISPLAY "======================"
    DISPLAY ""
    
    -- Step 1: Load users with their last login timestamps
    DISPLAY "Loading user data from database..."
    CALL load_all_users_with_login(l_users) RETURNING l_success
    
    IF NOT l_success THEN
        DISPLAY "Error: Failed to load user data"
        EXIT PROGRAM 1
    END IF
    
    DISPLAY "Loaded ", l_users.getLength(), " users"
    DISPLAY ""
    
    -- Step 2: Classify each user
    DISPLAY "Classifying users..."
    CALL classify_users(l_users, l_classified_users) RETURNING l_success
    
    IF NOT l_success THEN
        DISPLAY "Error: Failed to classify users"
        EXIT PROGRAM 1
    END IF
    
    DISPLAY "Classification complete"
    DISPLAY ""
    
    -- Step 3: Log inactive users to the database
    DISPLAY "Logging inactive users to database..."
    CALL log_inactive_users(l_classified_users, TRUE) RETURNING l_inactive_count
    
    IF l_inactive_count < 0 THEN
        DISPLAY "Error: Failed to log inactive users"
        EXIT PROGRAM 1
    END IF
    
    DISPLAY "Logged ", l_inactive_count, " inactive users"
    DISPLAY ""
    
    -- Step 4: Build and display summary statistics
    CALL get_summary_statistics(l_classified_users, l_summary)
    CALL display_summary(l_summary)
    
    DISPLAY ""
    DISPLAY "Analysis complete!"
    
END MAIN

--------------------------------------------------------------------------------
-- FUNCTION: analyze_user_activity
-- Reusable function to execute the full user activity analysis
-- @param p_summary: Output record with summary statistics
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION analyze_user_activity(p_summary)
    DEFINE p_summary RECORD
        total_users INTEGER,
        active_count INTEGER,
        dormant_count INTEGER,
        inactive_count INTEGER,
        oldest_last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_classified_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE l_success BOOLEAN
    DEFINE l_inactive_count INTEGER
    
    -- Step 1: Load users
    CALL load_all_users_with_login(l_users) RETURNING l_success
    IF NOT l_success THEN
        RETURN FALSE
    END IF
    
    -- Step 2: Classify users
    CALL classify_users(l_users, l_classified_users) RETURNING l_success
    IF NOT l_success THEN
        RETURN FALSE
    END IF
    
    -- Step 3: Log inactive users
    CALL log_inactive_users(l_classified_users, TRUE) RETURNING l_inactive_count
    IF l_inactive_count < 0 THEN
        RETURN FALSE
    END IF
    
    -- Step 4: Build summary
    CALL get_summary_statistics(l_classified_users, p_summary)
    
    RETURN TRUE
END FUNCTION
