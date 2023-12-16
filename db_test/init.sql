DROP TABLE IF EXISTS T1;
DROP TABLE IF EXISTS T2;
DROP TABLE IF EXISTS T3;

CREATE TABLE IF NOT EXISTS T1 (
    ID INTEGER PRIMARY KEY,
    Deleted INTEGER,
    RandomText TEXT NOT NULL,
    RandomDate TEXT NOT NULL CHECK (RandomDate IS date(RandomDate,'+0 days'))
);

CREATE TABLE IF NOT EXISTS T2 (
    ID INTEGER PRIMARY KEY,
    Deleted INTEGER,

    FForeignID INTEGER NOT NULL,
    SForeignID INTEGER NOT NULL,
    RandomText TEXT NOT NULL CHECK (RandomText NOT LIKE ''),
    RandInt INTEGER NOT NULL CHECK (RandInt > 0 AND typeof(RandInt) == 'integer'),
	FOREIGN KEY (FForeignID)  REFERENCES T1 (id),
    FOREIGN KEY (SForeignID) REFERENCES T3(id)
);

CREATE TABLE IF NOT EXISTS T3 (
    ID INTEGER PRIMARY KEY,
    Deleted INTEGER,

    RandomText TEXT NOT NULL CHECK (RandomText NOT LIKE '')
);

INSERT INTO T1 (RandomText, RandomDate) VALUES ('First Table text, id = 1', '2023-11-23');
INSERT INTO T1 (RandomText, RandomDate) VALUES ('First Table text, id = 2', '2020-11-23');

INSERT INTO T2 (FForeignID, SForeignID, RandomText, RandInt) VALUES (1, 2, 'Second Table text, id = 1', 3);

INSERT INTO T3 (RandomText) VALUES ('Third Table text, id = 1');
INSERT INTO T3 (RandomText) VALUES ('Third Table text, id = 2');
INSERT INTO T3 (RandomText) VALUES ('Third Table text, id = 3');