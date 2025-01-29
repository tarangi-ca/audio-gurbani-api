-- migrate:up
CREATE TABLE hukamnamas (
    id UUID PRIMARY KEY,
    melody TEXT NOT NULL,
    writer TEXT NOT NULL,
    page SMALLINT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down
DROP TABLE IF EXISTS hukamnamas;
