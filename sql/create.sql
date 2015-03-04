.bail ON

CREATE TABLE user (
	id INTEGER NOT NULL, 
	user VARCHAR, 
	name VARCHAR, 
	mail VARCHAR, 
	passwd VARCHAR, 
	session VARCHAR, 
	seed INTEGER, 
	karma INTEGER, 
	food INTEGER, 
	drink INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE version (
	id INTEGER NOT NULL, 
	version VARCHAR, 
	PRIMARY KEY (id)
);

INSERT INTO "user" VALUES(1,'admin','Administrador','fjriosp@gmail.com','5af89cf75f3c3fbeaa7da4cca37b9a7f',NULL,1425374633722,0,NULL,NULL);
INSERT INTO "version" VALUES(1,'0.1');
