-- db_writer.4gl
-- Database Writer module for User Activity Analyzer
-- Handles writing inactive user logs to the database

IMPORT FGL constants

--------------------------------------------------------------------------------
-- FUNCTION: ensure_inactive_log_table
-- Ensure the inactive_log table exists
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION ensure_inactive_log_table()
    WHENEVER ERROR CONTINUE
    
    -- Create table if it doesn't exist
    -- Note: Exact syntax may vary by database (Informix shown here)
    EXECUTE IMMEDIATE "CREATE TABLE IF NOT EXISTS inactive_log (" ||
        "log_id SERIAL PRIMARY KEY, " ||
        "user_id INTEGER NOT NULL, " ||
        "last_login DATETIME YEAR TO SECOND, " ||
        "days_since_login INTEGER, " ||
        "logged_at DATETIME YEAR TO SECOND NOT NULL, " ||
        "FOREIGN KEY (user_id) REFERENCES users(user_id)" ||
        ")"
    
    WHENEVER ERROR STOP
    
    IF SQLCA.SQLCODE < 0 AND SQLCA.SQLCODE != -310 THEN
        -- -310 is "table already exists" in Informix
        DISPLAY "Error creating inactive_log table: ", SQLCA.SQLCODE
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: log_inactive_user
-- Log a single inactive user to the database
-- @param p_user_id: The user ID
-- @param p_last_login: The last login timestamp (optional)
-- @param p_days_since_login: Days since last login (optional)
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION log_inactive_user(p_user_id, p_last_login, p_days_since_login)
    DEFINE p_user_id INTEGER
    DEFINE p_last_login DATETIME YEAR TO SECOND
    DEFINE p_days_since_login INTEGER
    DEFINE l_logged_at DATETIME YEAR TO SECOND
    
    LET l_logged_at = CURRENT YEAR TO SECOND
    
    WHENEVER ERROR CONTINUE
    
    INSERT INTO inactive_log (
        user_id,
        last_login,
        days_since_login,
        logged_at
    ) VALUES (
        p_user_id,
        p_last_login,
        p_days_since_login,
        l_logged_at
    )
    
    WHENEVER ERROR STOP
    
    IF SQLCA.SQLCODE < 0 THEN
        DISPLAY "Error logging inactive user ", p_user_id, ": ", SQLCA.SQLCODE
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: log_inactive_users
-- Log all inactive users to the database
-- @param p_classified_users: Array of classified user records
-- @param p_use_transaction: Whether to use a transaction
-- @return: Number of inactive users logged, -1 on error
--------------------------------------------------------------------------------
FUNCTION log_inactive_users(p_classified_users, p_use_transaction)
    DEFINE p_classified_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND,
        days_since_login INTEGER,
        category VARCHAR(20)
    END RECORD
    
    DEFINE p_use_transaction BOOLEAN
    DEFINE l_idx INTEGER
    DEFINE l_count INTEGER
    DEFINE l_success BOOLEAN
    
    -- Ensure table exists
    CALL ensure_inactive_log_table() RETURNING l_success
    IF NOT l_success THEN
        RETURN -1
    END IF
    
    LET l_count = 0
    
    -- Begin transaction if requested
    IF p_use_transaction THEN
        BEGIN WORK
    END IF
    
    WHENEVER ERROR CONTINUE
    
    -- Log each inactive user
    FOR l_idx = 1 TO p_classified_users.getLength()
        IF p_classified_users[l_idx].category = CATEGORY_INACTIVE THEN
            CALL log_inactive_user(
                p_classified_users[l_idx].user_id,
                p_classified_users[l_idx].last_login,
                p_classified_users[l_idx].days_since_login
            ) RETURNING l_success
            
            IF NOT l_success THEN
                IF p_use_transaction THEN
                    ROLLBACK WORK
                END IF
                WHENEVER ERROR STOP
                RETURN -1
            END IF
            
            LET l_count = l_count + 1
        END IF
    END FOR
    
    -- Commit transaction if requested
    IF p_use_transaction THEN
        COMMIT WORK
    END IF
    
    WHENEVER ERROR STOP
    
    RETURN l_count
END FUNCTION
