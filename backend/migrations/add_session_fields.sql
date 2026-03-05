-- Migration: Add session management fields to users table
-- Purpose: Support single session per user (multi-tab synchronization)
-- Date: 2024

ALTER TABLE users ADD COLUMN IF NOT EXISTS last_valid_token VARCHAR(500) DEFAULT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_token_issued_at DateTime DEFAULT NULL;

-- Create index for token lookup if needed for performance
-- CREATE INDEX idx_users_last_valid_token ON users(last_valid_token);
