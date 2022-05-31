CREATE TABLE IF NOT EXISTS Game
(
    'id'                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'rank'              INTEGER UNIQUE NOT NULL,
    'game'              BLOB UNIQUE NOT NULL,
    'platform'          TEXT NOT NULL,
    'year'              INTEGER NOT NULL,
    'genre'             TEXT NOT NULL,
    'publisher'         BLOB NOT NULL,
    'na'                REAL,
    'eu'                REAL,
    'jp'                REAL,
    'other'             REAL,
    'global'            REAL
);
