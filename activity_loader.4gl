-- activity_loader.4gl
-- Activity Loader module for User Activity Analyzer
-- Handles loading user IDs and login timestamps from the database

IMPORT FGL constants

--------------------------------------------------------------------------------
-- FUNCTION: load_user_ids
-- Load all user IDs from the database
-- @param p_user_ids: Dynamic array to store user IDs
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION load_user_ids(p_user_ids)
    DEFINE p_user_ids DYNAMIC ARRAY OF INTEGER
    DEFINE l_user_id INTEGER
    DEFINE l_idx INTEGER
    
    LET l_idx = 1
    
    WHENEVER ERROR CONTINUE
    
    DECLARE user_cursor CURSOR FOR
        SELECT user_id 
        FROM users 
        ORDER BY user_id
    
    FOREACH user_cursor INTO l_user_id
        LET p_user_ids[l_idx] = l_user_id
        LET l_idx = l_idx + 1
    END FOREACH
    
    CLOSE user_cursor
    FREE user_cursor
    
    WHENEVER ERROR STOP
    
    IF SQLCA.SQLCODE < 0 THEN
        DISPLAY "Error loading user IDs: ", SQLCA.SQLCODE
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: load_user_last_login
-- Load the last login timestamp for a specific user
-- @param p_user_id: The user ID to look up
-- @param p_last_login: Output parameter for last login timestamp
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION load_user_last_login(p_user_id, p_last_login)
    DEFINE p_user_id INTEGER
    DEFINE p_last_login DATETIME YEAR TO SECOND
    
    WHENEVER ERROR CONTINUE
    
    SELECT last_login 
    INTO p_last_login
    FROM users
    WHERE user_id = p_user_id
    
    WHENEVER ERROR STOP
    
    IF SQLCA.SQLCODE < 0 THEN
        DISPLAY "Error loading last login for user ", p_user_id, ": ", SQLCA.SQLCODE
        RETURN FALSE
    END IF
    
    IF SQLCA.SQLCODE = NOTFOUND THEN
        DISPLAY "User ID ", p_user_id, " not found"
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION

--------------------------------------------------------------------------------
-- FUNCTION: load_all_users_with_login
-- Load all users with their last login timestamps in a single query
-- @param p_users: Dynamic array to store user data
-- @return: TRUE if successful, FALSE otherwise
--------------------------------------------------------------------------------
FUNCTION load_all_users_with_login(p_users)
    DEFINE p_users DYNAMIC ARRAY OF RECORD
        user_id INTEGER,
        last_login DATETIME YEAR TO SECOND
    END RECORD
    
    DEFINE l_user_id INTEGER
    DEFINE l_last_login DATETIME YEAR TO SECOND
    DEFINE l_idx INTEGER
    
    LET l_idx = 1
    
    WHENEVER ERROR CONTINUE
    
    DECLARE all_users_cursor CURSOR FOR
        SELECT user_id, last_login
        FROM users
        ORDER BY user_id
    
    FOREACH all_users_cursor INTO l_user_id, l_last_login
        LET p_users[l_idx].user_id = l_user_id
        LET p_users[l_idx].last_login = l_last_login
        LET l_idx = l_idx + 1
    END FOREACH
    
    CLOSE all_users_cursor
    FREE all_users_cursor
    
    WHENEVER ERROR STOP
    
    IF SQLCA.SQLCODE < 0 THEN
        DISPLAY "Error loading users with login data: ", SQLCA.SQLCODE
        RETURN FALSE
    END IF
    
    RETURN TRUE
END FUNCTION
