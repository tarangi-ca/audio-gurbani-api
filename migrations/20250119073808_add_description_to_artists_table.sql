-- migrate:up
ALTER TABLE artists
ADD COLUMN description TEXT NOT NULL;

-- migrate:down
ALTER TABLE artists
DROP COLUMN description;
