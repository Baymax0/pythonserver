
CREATE TABLE user_table (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER UNIQUE NOT NULL,
  password TEXT NOT NULL,
  lover_userid INTEGER DEFAULT -1,
  wallet INTEGER DEFAULT 0
);

CREATE TABLE wallet_record_table (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  apply_userid INTEGER NOT NULL,
  status INTEGER DEFAULT 0,
  apply_time INTEGER DEFAULT 0
);
