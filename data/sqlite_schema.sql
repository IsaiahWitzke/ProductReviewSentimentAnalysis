

CREATE TABLE user_reviews (
	id				INTEGER		UNIQUE PRIMARY KEY,
	overall			INTEGER,
	verified		INTEGER,
	vote			INTEGER,
	asin			INTEGER,
	reviewerID		TEXT,
	reviewerName	TEXT,
	reviewText		TEXT,
	datetime		INTEGER DEFAULT(datetime('now')),
	summary			TEXT	
);


CREATE TABLE aws_sentiment (
	id						INTEGER		UNIQUE PRIMARY KEY,
	sentiment				TEXT,
	sentimentScorePositive	REAL,
	sentimentScoreNegative	REAL,
	sentimentScoreNeutral	REAL,
	sentimentScoreMixed		REAL,
	datetime				INTEGER 	DEFAULT(datetime('now')),
	userReview				INTEGER 	NOT NULL,
	
	FOREIGN KEY(userReview) REFERENCES user_reviews(id)
);

CREATE TABLE aws_key_phrases (
	id			INTEGER		UNIQUE PRIMARY KEY,
	text		TEXT,
	score		REAL,
	beginOffset	INTEGER,
	endOffset	INTEGER,
	userReview	INTEGER 	NOT NULL,
	
	FOREIGN KEY(userReview) REFERENCES user_reviews(id)
);