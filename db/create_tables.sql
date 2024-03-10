create table user (
  id INTEGER PRIMARY KEY,
  name VARCHAR(40) UNIQUE,
  password VARCHAR(40),
  api_key VARCHAR(40)
);

create table channel (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40) UNIQUE
);

create table message (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  channel_id INTEGER,
  body TEXT,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(channel_id) REFERENCES channel(id)
);

create table reply (
  id INTEGER PRIMARY KEY,
  author_id INTEGER,
  body TEXT,
  message_id INTEGER,
  FOREIGN KEY(author_id) REFERENCES user(id),
  FOREIGN KEY(message_id) REFERENCES message(id)
);