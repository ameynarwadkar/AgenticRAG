-- Create an append-only audit ledger table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id TEXT,
    user_id TEXT,
    tool_name TEXT NOT NULL,
    input_params JSONB NOT NULL,
    output_results JSONB,
    status TEXT NOT NULL, -- e.g., 'SUCCESS', 'ERROR'
    model_used TEXT,
    execution_duration_ms INTEGER
);

-- Ensure append-only by restricting UPDATE and DELETE
-- 1. Revoke default update/delete permissions
REVOKE UPDATE, DELETE ON audit_logs FROM authenticated, anon, public;

-- 2. Optional (but recommended) - create a trigger to absolutely block any updates/deletes even from service roles if desired
CREATE OR REPLACE FUNCTION prevent_modifications()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit logs are append-only. Updates and Deletes are forbidden.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_append_only
BEFORE UPDATE OR DELETE ON audit_logs
FOR EACH ROW
EXECUTE FUNCTION prevent_modifications();

-- Create an index for faster querying by timestamp and tool
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_tool ON audit_logs(tool_name);
