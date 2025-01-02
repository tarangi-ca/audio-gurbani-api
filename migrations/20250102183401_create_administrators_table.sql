-- migrate:up
CREATE TABLE administrators (
    id UUID PRIMARY KEY,
    email_address TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_administrators_email_address ON administrators(email_address);

-- migrate:down
DROP TABLE IF EXISTS administrators;
