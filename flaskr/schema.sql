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
    groupe_explain TEXT NOT NULL,
    groupe_code TEXT NOT NULL
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    groupe_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    state INTEGER NOT NULL DEFAULT (0),
    username TEXT,
    FOREIGN KEY (groupe_id) REFERENCES groupe (id)
);

CREATE TABLE conection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    groupe_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (groupe_id) REFERENCES groupe (id)
);

INSERT INTO user (username, password) VALUES ('yamato', '1111'), ('sakata', '1111'), ('山田', '1111'), ('田中', '1111');
INSERT INTO groupe (groupe_name, groupe_explain, groupe_code) VALUES ('初めてのハッカソン', '5月21日〜5月22日 @オンライン', '1'), ('プロジェクトA', '6月までに完成目標', '2'), ('プロジェクトB', '8月までに完成目標', '3'), ('送別会', 'サークルの先輩たちへの色紙づくり', '4');
INSERT INTO task (groupe_id, title, body) VALUES (1, 'ログイン機能', 'メールアドレスは不要'), (1, 'ログアウト機能', 'ポップアップによる確認必須'), (1, 'スライド作成', '最終日の16時までに完成'), (4, '佐藤先輩の写真集め', 'これだけなる早でよろしく');
INSERT INTO conection (user_id, groupe_id) VALUES (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 4), (4, 1), (4, 2);
