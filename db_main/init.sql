DROP TABLE IF EXISTS Knihi;
DROP TABLE IF EXISTS Authors;

CREATE TABLE IF NOT EXISTS Authors (
    ID INTEGER PRIMARY KEY,
    Deleted INTEGER,
    AuthorName TEXT NOT NULL CHECK (AuthorName NOT LIKE ''),
    BirthDate TEXT NOT NULL CONSTRAINT valid_date CHECK (BirthDate == strftime('%Y-%m-%d', BirthDate) AND BirthDate IS date(BirthDate,'+0 days')),
    Salary REAL NOT NULL CHECK (Salary >= 0 AND (round(Salary, 2) - Salary == 0)),
    Num_cats INTEGER NOT NULL CHECK (Num_cats >= 0 AND typeof(Num_cats) == 'integer')
);

CREATE TABLE IF NOT EXISTS Knihi (
    ID INTEGER PRIMARY KEY,
    Deleted INTEGER,

    AuthorID INTEGER NOT NULL,
    Title TEXT NOT NULL CHECK (Title NOT LIKE ''),
    ReleaseDate TEXT NOT NULL CONSTRAINT valid_date CHECK (ReleaseDate == strftime('%Y-%m-%d', ReleaseDate) AND ReleaseDate IS date(ReleaseDate,'+0 days')),

    Cost REAL NOT NULL CHECK (Cost >= 0 AND (round(Cost, 2) - Cost == 0)),
    Copys INTEGER NOT NULL CHECK (Copys > 0 AND typeof(Copys) == 'integer'),
	FOREIGN KEY (AuthorID)  REFERENCES Authors (id)
);

CREATE TRIGGER validate_birth_date 
   BEFORE INSERT ON Authors
BEGIN
	SELECT
	CASE WHEN (date('now', '-16 years') < date(NEW.BirthDate)) THEN
		 RAISE(ABORT, 'This person is too small to be the author in this publishing agency :(')
	END;
END;

CREATE TRIGGER validate_release_date
   BEFORE INSERT ON Knihi
BEGIN
	SELECT
	CASE WHEN (date('now', '+1 months') < date(NEW.ReleaseDate)) THEN
		 RAISE(ABORT, "This publishing agency doesn't set release dates more then 1 month prior")
	END;
END;

INSERT INTO Authors (AuthorName, BirthDate, Salary, Num_cats) VALUES ('Lina', '2002-10-14', 220.75, 0);
INSERT INTO Authors (AuthorName, BirthDate, Salary, Num_cats) VALUES ('Biba', '1985-08-12', 1000.01, 2);
INSERT INTO Authors (AuthorName, BirthDate, Salary, Num_cats) VALUES ('Biba', '1989-05-04', 1111.11, 1);
INSERT INTO Authors (AuthorName, BirthDate, Salary, Num_cats) VALUES ('Some random dude', '1973-12-08', 1795.25, 3);
INSERT INTO Authors (AuthorName, BirthDate, Salary, Num_cats) VALUES ('Famous Author', '1980-12-08', 2897.12, 0);


INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (1, 'Kursach', '2023-12-12', 11.57, 1);
INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (4, 'How to cook like a pro', '2018-09-12', 15.90, 1000);
INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (5, 'Medieval fantasy: part one', '2000-03-18', 10.43, 1000);
INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (5, 'Medieval fantasy: part two', '2002-08-20', 8.43, 2000);
INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (5, 'Medieval fantasy: part three', '2003-03-21', 15.90, 5000);
INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (5, 'Medieval fantasy: the big finale', '2004-12-01', 21.85, 10000);
-- INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (2, 'The big response from the oldest one!', '2020-09-07', 11.57, 1);
-- INSERT INTO Knihi (AuthorID, Title, ReleaseDate, Cost, Copys) VALUES (3, 'It is though to be youngest!', '2018-08-12', 11.57, 1);