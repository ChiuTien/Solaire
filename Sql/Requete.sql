SELECT session_id, login_name, status
FROM sys.dm_exec_sessions
WHERE database_id = DB_ID('model');
GO

KILL 55;
GO