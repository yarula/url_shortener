CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- store new urls here
CREATE TABLE links (
  id SERIAL PRIMARY KEY,
  orig_url VARCHAR(255) NOT NULL DEFAULT '',
  short_code VARCHAR(8) NOT NULL DEFAULT '',
  hashsum VARCHAR(64) NOT NULL DEFAULT '',
  is_deleted BOOLEAN DEFAULT FALSE
);

-- the bank of pre-generated unique symbol permutations to implement really short unique codes
CREATE TABLE permutations (
  value VARCHAR(8) PRIMARY KEY,
  used BOOLEAN DEFAULT FALSE
);

-- primitive event stor for stat reports needs ( and not only )
CREATE TABLE event_log (
    id UUID PRIMARY KEY,
    type VARCHAR(16) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
