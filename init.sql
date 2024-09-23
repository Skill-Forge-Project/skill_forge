-- init.sql

-- Run this as a superuser to create the pg_cron extension
CREATE EXTENSION pg_cron;

-- Optionally, grant usage to a regular user (replace 'skill_forge' with your username)
GRANT USAGE ON SCHEMA cron TO skill_forge;

-- Create a scheduled job that runs every minute and deletes old Reset Password Tokens
SELECT cron.schedule(
  '* * * * *', 
  $$
  DO $$ 
  BEGIN
    -- Check if the reset_token table exists
    IF EXISTS (
      SELECT 1 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_name = 'reset_tokens'
    ) THEN
      -- Delete expired tokens if the table exists
      DELETE FROM "reset_tokens" WHERE expiration_time < now();
    END IF;
  END; 
  $$;
);