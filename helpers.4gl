-- helpers.4gl
-- Helper functions for User Activity Analyzer module
-- Provides utility functions for validation, date conversion, and categorization

IMPORT FGL constants

--------------------------------------------------------------------------------
-- FUNCTION: validate_user_id
-- Validates that a user ID is valid
-- @param p_user_id: The user ID to validate
-- @return: TRUE if valid, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION validate_user_id(p_user_id)
    DEFINE p_user_id INTEGER
    
    IF p_user_id IS NULL THEN
        RETURN FALSE
    END IF
    
    IF p_user_id <= 0 THEN
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: validate_timestamp
-- Validates that a timestamp is valid
-- @param p_timestamp: The timestamp to validate
-- @return: TRUE if valid, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION validate_timestamp(p_timestamp)
    DEFINE p_timestamp DATETIME YEAR TO SECOND
    
    IF p_timestamp IS NULL THEN
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: convert_datetime_to_days_difference
-- Convert a datetime to the number of days difference from current time
-- @param p_last_login: The last login datetime
-- @return: Number of days difference
--------------------------------------------------------------------------------
FUNCTION convert_datetime_to_days_difference(p_last_login)
    DEFINE p_last_login DATETIME YEAR TO SECOND
    DEFINE l_current_time DATETIME YEAR TO SECOND
    DEFINE l_difference INTERVAL DAY(9) TO DAY
    DEFINE l_days INTEGER
    
    LET l_current_time = CURRENT YEAR TO SECOND
    
    IF p_last_login IS NULL THEN
        RETURN NULL
    END IF
    
    LET l_difference = l_current_time - p_last_login
    LET l_days = l_difference
    
    RETURN l_days
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: categorize_user
-- Categorize a user based on days since last login
-- @param p_days_since_login: Number of days since last login
-- @return: Category label (ACTIVE, DORMANT, or INACTIVE)
--------------------------------------------------------------------------------
FUNCTION categorize_user(p_days_since_login)
    DEFINE p_days_since_login INTEGER
    DEFINE l_category VARCHAR(20)
    
    IF p_days_since_login IS NULL THEN
        LET l_category = CATEGORY_INACTIVE
    ELSE IF p_days_since_login < 0 THEN
        -- Future date, treat as active
        LET l_category = CATEGORY_ACTIVE
    ELSE IF p_days_since_login <= THRESHOLD_ACTIVE_DAYS THEN
        LET l_category = CATEGORY_ACTIVE
    ELSE IF p_days_since_login <= THRESHOLD_DORMANT_DAYS THEN
        LET l_category = CATEGORY_DORMANT
    ELSE
        LET l_category = CATEGORY_INACTIVE
    END IF
    
    RETURN l_category
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: build_summary_statistics
-- Build summary statistics from categorized users
-- @param p_classified_users: Dynamic array of classified user records
-- @param p_summary: Output record with summary statistics
--------------------------------------------------------------------------------
FUNCTION build_summary_statistics(p_classified_users, p_summary)
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
    
    DEFINE l_idx INTEGER
    
    -- Initialize counters
    LET p_summary.total_users = 0
    LET p_summary.active_count = 0
    LET p_summary.dormant_count = 0
    LET p_summary.inactive_count = 0
    LET p_summary.oldest_last_login = NULL
    
    -- Count total users
    LET p_summary.total_users = p_classified_users.getLength()
    
    IF p_summary.total_users = 0 THEN
        RETURN
    END IF
    
    -- Iterate through users to count categories and find oldest login
    FOR l_idx = 1 TO p_summary.total_users
        -- Count by category
        CASE p_classified_users[l_idx].category
            WHEN CATEGORY_ACTIVE
                LET p_summary.active_count = p_summary.active_count + 1
            WHEN CATEGORY_DORMANT
                LET p_summary.dormant_count = p_summary.dormant_count + 1
            WHEN CATEGORY_INACTIVE
                LET p_summary.inactive_count = p_summary.inactive_count + 1
        END CASE
        
        -- Find oldest last login
        IF p_classified_users[l_idx].last_login IS NOT NULL THEN
            IF p_summary.oldest_last_login IS NULL OR 
               p_classified_users[l_idx].last_login < p_summary.oldest_last_login THEN
                LET p_summary.oldest_last_login = p_classified_users[l_idx].last_login
            END IF
        END IF
    END FOR
END FUNCTION
