-- migrate:up
CREATE TABLE audios (
    id UUID PRIMARY KEY,
    display_name TEXT NOT NULL,
    collection_id UUID NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audios_collection_id ON audios(collection_id);

-- migrate:down
DROP TABLE IF EXISTS audios;