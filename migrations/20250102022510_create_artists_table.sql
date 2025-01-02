-- migrate:up
CREATE TABLE artists (
    id UUID PRIMARY KEY,
    display_name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_artists_slug ON artists(slug);

-- migrate:down
DROP TABLE IF EXISTS artists;