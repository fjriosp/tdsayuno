.bail ON

ALTER TABLE "user" ADD COLUMN pref_food INTEGER;
ALTER TABLE "user" ADD COLUMN pref_drink INTEGER;

CREATE TABLE food (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	price FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE drink (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	price FLOAT, 
	PRIMARY KEY (id)
);

UPDATE "version" SET "version" = '0.2';
