CREATE TABLE passwords (
  idpassword int(11) NOT NULL AUTO_INCREMENT,
  userid int(11) NOT NULL,
  passwordhash text NOT NULL,
  sitename text NOT NULL,
  PRIMARY KEY (idpassword),
  KEY userid(userid),
  CONSTRAINT passwords_ibfk_1FOREIGN KEY (userid) REFERENCES users (idusers)
)
