-- user_classifier.4gl
-- User Classifier module for User Activity Analyzer
-- Handles the categorization of users based on their login activity

IMPORT FGL helpers

--------------------------------------------------------------------------------
-- FUNCTION: classify_user
-- Classify a single user based on their last login
-- @param p_user_id: The user ID
-- @param p_last_login: The last login timestamp (NULL if never logged in)
-- @param p_classified_user: Output record with classification data
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION classify_user(p_user_id, p_last_login, p_classified_user)
    DEFINE p_user_id INTEGER
    DEFINE p_last_login DATETIME YEAR TO SECOND
    DEFINE p_classified_user RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE l_days_since_login INTEGER
    
    -- Validate user ID
    IF NOT validate_user_id(p_user_id) THEN
        DISPLAY "Invalid user ID: ", p_user_id
        RETURN FALSE
    END IF
    
    -- Set user ID
    LET p_classified_user.user_id = p_user_id
    LET p_classified_user.last_login = p_last_login
    
    -- If user has never logged in, treat as inactive
    IF p_last_login IS NULL THEN
        LET p_classified_user.days_since_login = NULL
        LET p_classified_user.category = CATEGORY_INACTIVE
        RETURN TRUE
    END IF
    
    -- Calculate days since login
    LET l_days_since_login = convert_datetime_to_days_difference(p_last_login)
    LET p_classified_user.days_since_login = l_days_since_login
    
    -- Categorize user
    LET p_classified_user.category = categorize_user(l_days_since_login)
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: classify_users
-- Classify multiple users
-- @param p_users: Input array of user records
-- @param p_classified_users: Output array of classified user records
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION classify_users(p_users, p_classified_users)
    DEFINE p_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE p_classified_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE l_idx INTEGER
    DEFINE l_success BOOLEAN
    
    FOR l_idx = 1 TO p_users.getLength()
        CALL classify_user(
            p_users[l_idx].user_id,
            p_users[l_idx].last_login,
            p_classified_users[l_idx]
        ) RETURNING l_success
        
        IF NOT l_success THEN
            DISPLAY "Failed to classify user ", p_users[l_idx].user_id
            RETURN FALSE
        END IF
    END FOR
    
    RETURN TRUE
END FUNCTION
