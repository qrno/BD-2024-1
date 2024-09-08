DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS repost;
DROP TABLE IF EXISTS follow;
DROP TABLE IF EXISTS [like];
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS [group];
DROP TABLE IF EXISTS membership;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS message;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Primeira forma normal -- 
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

-- Talvez fosse melhor essa tabela só ter um id próprio -- 
CREATE TABLE repost (
  id_post INTEGER,
  id_user INTEGER,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY (id_post, id_user, created),
  FOREIGN KEY (id_post) REFERENCES post(id),
  FOREIGN KEY (id_user) REFERENCES user(id)
);

CREATE TABLE follow (
  id_follower INTEGER,
  id_followed INTEGER,
  PRIMARY KEY (id_follower, id_followed),
  FOREIGN KEY (id_follower) REFERENCES user(id),
  FOREIGN KEY (id_followed) REFERENCES user(id)
);

CREATE TABLE [like] (
  id_user INTEGER,
  id_post INTEGER,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_user, id_post),
  FOREIGN KEY (id_user) REFERENCES user(id),
  FOREIGN KEY (id_post) REFERENCES post(id)
);

-- Deixei o id como única chave, caso contrário ele não pode ser autoincremento -- 
CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_user INTEGER,
  id_post INTEGER,
  content TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_post) REFERENCES post(id),
  FOREIGN KEY (id_user) REFERENCES user(id)
);

CREATE TABLE [group] (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Primeira forma normal --
CREATE TABLE membership (
  id_user INTEGER,
  id_group INTEGER,
  PRIMARY KEY (id_user, id_group),
  FOREIGN KEY (id_user) REFERENCES user(id),
  FOREIGN KEY (id_group) REFERENCES [group](id)
);

CREATE TABLE chat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_user1 INTEGER,
  id_user2 INTEGER,
  FOREIGN KEY (id_user1) REFERENCES user(id),
  FOREIGN KEY (id_user2) REFERENCES user(id)

);

-- Mesma ideia da tabela comment. Ou id é autoincremento ou usamos os outros id's como PK's --
CREATE TABLE message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_chat INTEGER,
  id_user INTEGER,
  body TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_chat) REFERENCES chat(id),
  FOREIGN KEY (id_user) REFERENCES user(id)
);