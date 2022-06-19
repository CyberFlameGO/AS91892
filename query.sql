CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    card_number TEXT UNIQUE NOT NULL,
    card_name TEXT NOT NULL,
    type TEXT NOT NULL,
    rarity TEXT NOT NULL,
    value REAL NOT NULL,
    attribute TEXT NOT NULL,
    subtype TEXT NOT NULL,
    level INTEGER NOT NULL,
    card_atk INTEGER NOT NULL,
    card_def INTEGER NOT NULL,
    card_text BLOB NOT NULL
);
