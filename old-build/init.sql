-- init.sql

-- Run this as a superuser to create the pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Optionally, grant usage to a regular user (replace 'skill_forge' with your username)
GRANT USAGE ON SCHEMA cron TO skill_forge;

-- Create a scheduled job that runs every minute and deletes old Reset Password Tokens
SELECT cron.schedule('* * * * *', $$DELETE FROM reset_tokens WHERE expiration_time < now()$$);