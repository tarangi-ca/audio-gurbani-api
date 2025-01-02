-- migrate:up
CREATE TABLE collections (
    id UUID PRIMARY KEY,
    display_name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_collections_slug ON collections(slug);
CREATE INDEX idx_collections_artist_id ON collections(artist_id);

-- migrate:down
DROP TABLE IF EXISTS collections;