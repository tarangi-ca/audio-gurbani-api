-- migrate:up
ALTER TABLE artists
ALTER COLUMN description DROP NOT NULL;

-- migrate:down
ALTER TABLE artists
ALTER COLUMN description SET NOT NULL;
