-- activity_summary.4gl
-- Activity Summary module for User Activity Analyzer
-- Handles building and formatting summary statistics

IMPORT FGL helpers

--------------------------------------------------------------------------------
-- FUNCTION: display_summary
-- Display the summary statistics in a formatted manner
-- @param p_summary: The summary record
--------------------------------------------------------------------------------
FUNCTION display_summary(p_summary)
    DEFINE p_summary RECORD
        total_users INTEGER,
        active_count INTEGER,
        dormant_count INTEGER,
        inactive_count INTEGER,
        oldest_last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_active_pct DECIMAL(5,1)
    DEFINE l_dormant_pct DECIMAL(5,1)
    DEFINE l_inactive_pct DECIMAL(5,1)
    
    DISPLAY "="
    DISPLAY "User Activity Summary"
    DISPLAY "=================================================="
    DISPLAY "Total Users: ", p_summary.total_users
    
    -- Calculate percentages
    IF p_summary.total_users > 0 THEN
        LET l_active_pct = (p_summary.active_count * 100.0) / p_summary.total_users
        LET l_dormant_pct = (p_summary.dormant_count * 100.0) / p_summary.total_users
        LET l_inactive_pct = (p_summary.inactive_count * 100.0) / p_summary.total_users
    ELSE
        LET l_active_pct = 0
        LET l_dormant_pct = 0
        LET l_inactive_pct = 0
    END IF
    
    DISPLAY "Active Users: ", p_summary.active_count, " (", l_active_pct USING "###.#", "%)"
    DISPLAY "Dormant Users: ", p_summary.dormant_count, " (", l_dormant_pct USING "###.#", "%)"
    DISPLAY "Inactive Users: ", p_summary.inactive_count, " (", l_inactive_pct USING "###.#", "%)"
    
    IF p_summary.oldest_last_login IS NOT NULL THEN
        DISPLAY "Oldest Last Login: ", p_summary.oldest_last_login
    ELSE
        DISPLAY "Oldest Last Login: N/A"
    END IF
    
    DISPLAY "=================================================="
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: get_summary_statistics
-- Get summary statistics from classified users
-- @param p_classified_users: Array of classified user records
-- @param p_summary: Output record with summary statistics
--------------------------------------------------------------------------------
FUNCTION get_summary_statistics(p_classified_users, p_summary)
    DEFINE p_classified_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE p_summary RECORD
        total_users INTEGER,
        active_count INTEGER,
        dormant_count INTEGER,
        inactive_count INTEGER,
        oldest_last_login DATETIME YEAR TO SECOND
    END RECORD
    
    -- Use helper function to build statistics
    CALL build_summary_statistics(p_classified_users, p_summary)
END FUNCTION
