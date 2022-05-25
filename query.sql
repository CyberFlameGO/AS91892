CREATE TABLE IF NOT EXISTS Tags
(
    'id'                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'type'              VARCHAR(10) NOT NULL,
    'tag'               BLOB NOT NULL,
    'description'       TEXT NOT NULL
);
