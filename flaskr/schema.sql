DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS groupe;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS conection;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE groupe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    groupe_name TEXT NOT NULL,
    groupe_code TEXT NOT NULL
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    groupe_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (groupe_id) REFERENCES groupe (id)
);

CREATE TABLE conection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    groupe_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (groupe_id) REFERENCES groupe (id)
);

INSERT INTO user (username, password) VALUES ('yamato', '1015');
INSERT INTO groupe (groupe_name, groupe_code) VALUES ('NMB', '1');
INSERT INTO groupe (groupe_name, groupe_code) VALUES ('ベリーグッドマン', '3');
INSERT INTO task (groupe_id, title, body) VALUES (1, '柵運ぶ', '100本');
INSERT INTO conection (user_id, groupe_id) VALUES (1, 1);
